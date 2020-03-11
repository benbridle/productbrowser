import datetime
from bs4 import BeautifulSoup
import threading
from PyQt5.QtCore import QObject, pyqtSignal
from ldproductbrowser import globals as ldglobal
from ldproductbrowser.models import StockLevel, BranchDatabase, CompanyStock
from ldproductbrowser.tools import dev_scraper


class StockEnquiry(QObject):

    updated = pyqtSignal()

    def __init__(self, sku):
        super().__init__()
        self.mutex = threading.Lock()
        self.sku = sku
        self.stock = CompanyStock()
        self.time_last_updated = None

    def soft_refresh(self):
        soft_refresh_timer = ldglobal.settings["DevScraper"].getint("refresh_timer")
        if self.time_last_updated is None:
            self.refresh()
        elif datetime.datetime.now() - datetime.timedelta(minutes=soft_refresh_timer) > self.time_last_updated:
            self.refresh()

    def refresh(self):
        ldglobal.task_queue.put("stock_enquiry", self._refresh)

    def _refresh(self):
        self.stock = CompanyStock()
        html = dev_scraper.get_stock_page_html(self.sku)
        if html is not None:
            with self.mutex:
                self._load_from_html(html)
            print(f"{self.sku} updated")
        else:
            print(f"{self.sku} failed to download")
        self.updated.emit()

        delivery_html = dev_scraper.get_deliveries_page_html(self.sku)
        if delivery_html is not None:
            with self.mutex:
                self._load_from_deliveries_html(delivery_html)
            print(f"{self.sku} deliveries updated")
        else:
            print(f"{self.sku} deliveries failed to download")

        self._update_time_last_updated()
        self.updated.emit()

    def _update_time_last_updated(self):
        self.time_last_updated = datetime.datetime.now()

    def _load_from_deliveries_html(self, html):
        soup = BeautifulSoup(html, "html.parser")

        branch_del_table = soup.find(id="MainContent_ASPxRoundPanel1_storeGrid_DXMainTable")
        warehouse_del_table = soup.find(id="MainContent_ASPxRoundPanel1_POGrid_DXMainTable")
        delivery_dict = {}
        for destination, table in [("branch", branch_del_table), ("warehouse", warehouse_del_table)]:
            delivery_rows = []
            if table is not None:
                for table_row in table:
                    if table_row == "\n":
                        continue
                    row = []
                    for element in table_row:
                        if element.string == "\n":
                            continue
                        if element.string == "\xa0":
                            row.append("")
                        else:
                            row.append(element.string)
                    if not None in row:
                        delivery_rows.append(row)
            delivery_dict[destination] = delivery_rows

        branch_deliveries = []
        for row in delivery_dict["branch"]:
            clean_row = (row[1], row[2], row[3], row[4])
            branch_deliveries.append(clean_row)
        self.stock.deliveries_to_branch = branch_deliveries

        month_lookup = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        warehouse_deliveries = []
        for row in delivery_dict["warehouse"]:
            date = row[3]
            if date.count("/") == 2:
                try:
                    day = date.split("/")[0]
                    day = day.lstrip("0")
                    month = date.split("/")[1]
                    month = month_lookup[int(month) - 1]
                    date = day + " " + month
                except:
                    print(f"Date parsing failed in warehouse delivery for {self.sku}")
            if row[2] == "Estimated":
                date += " (est)"
            if row[2] == "Confirmed":
                date += " (con)"
            clean_row = (row[1], date, row[4])
            warehouse_deliveries.append(clean_row)
        self.stock.deliveries_to_warehouse = warehouse_deliveries

    def _load_from_html(self, html):
        soup = BeautifulSoup(html, "html.parser")

        self.stock.mrp = soup.find(id="MainContent_ASPxRoundPanel1_txtMRPController_I")["value"]
        self.stock.eol = self.stock.mrp == "002 End of Line"

        reorder_point_string = soup.find(id="MainContent_ASPxRoundPanel1_txtReorder_I")["value"]
        self.stock.reorder_point = int(float(reorder_point_string))

        current_branch_row = soup.find(id="MainContent_ASPxRoundPanel1_StoresGrid2_DXDataRow0")
        current_branch_row = [int(cell.string) for cell in current_branch_row if cell.string != "\n"]
        current_branch_stock = StockLevel(current_branch_row[0], current_branch_row[2], current_branch_row[-1])

        warehouse_row = soup.find(id="MainContent_ASPxRoundPanel1_wsGrid_DXDataRow0")
        warehouse_row = [int(cell.string) for cell in warehouse_row if cell.string != "\n"]
        warehouse_stock = StockLevel(warehouse_row[0], warehouse_row[1], warehouse_row[2])

        main_table = soup.find(id="MainContent_ASPxRoundPanel1_allStoresGrid_DXMainTable")
        main_table_rows = [[cell.string for cell in row if cell.string != "\n"] for row in main_table if row != "\n"]

        # Convert double-wide table into a double-length single-wide table
        branch_rows = []
        for row in main_table_rows[1:]:  # Ignore header row
            branch_rows.append(row[:7])
            branch_rows.append(row[8:])
        branch_rows = [row for row in branch_rows if row[0] != "\xa0"]  # filter out empty rows

        branch_stock = {}
        for row in branch_rows:
            stock_level = StockLevel(int(row[1]), int(row[3]), int(row[-1]))
            branch_name = row[0]
            if branch_name == "3PL (+ 2 Days)":  # Special case for third party logistics
                third_party_logistics_stock = stock_level
                continue
            branch_stock[branch_name] = stock_level

        self.stock.warehouse = warehouse_stock
        self.stock.third_party_logistics = third_party_logistics_stock

        branch_db = BranchDatabase(ldglobal.app_context.get_resource("databases/BranchDatabase.db"))
        for branch_name, stock_level in branch_stock.items():
            branch = branch_db.get_branch_from_name(branch_name)
            self.stock.add_branch_stock(branch, stock_level)

        all_branch_ids = [branch.branch_id for branch in branch_db.get_all_branches()]
        partial_branch_ids = [branch.branch_id for branch in self.stock.branches]
        try:
            current_branch_id = (set(all_branch_ids) - set(partial_branch_ids)).pop()
            current_branch = branch_db.get_branch(current_branch_id)
            self.stock.current_branch = current_branch
            self.stock.add_branch_stock(current_branch, current_branch_stock)
        except KeyError:
            pass

