from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QHeaderView, QSizePolicy, QPushButton, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from ldproductbrowser.views import _ReadOnlyTableWidget, StockTableCell, BetterLabel, OneCellTable, DeliveryLayout
from ldproductbrowser import globals as ldglobal
from ldproductbrowser.models.branch_database import Island


class BranchTable(_ReadOnlyTableWidget):
    def __init__(self, branches, name):
        self.branches = branches

        height = len(branches) + 1
        super().__init__(3, height)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.setItem(0, 0, StockTableCell("Ph.", True))
        self.setItem(1, 0, StockTableCell(f"{name} Island", True))
        self.setItem(2, 0, StockTableCell("Avail.", True))

        self.branch_cells = {}

        for i, branch in enumerate(branches):
            id_cell = StockTableCell("3" + str(branch.branch_id).rjust(2, "0"))
            id_cell.setForeground(QColor("#7f949f"))
            self.setItem(0, i + 1, id_cell)

            name_cell = StockTableCell(" " + branch.name)
            name_cell.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.setItem(1, i + 1, name_cell)

            avail_cell = StockTableCell()
            self.setItem(2, i + 1, avail_cell)
            self.branch_cells[branch] = avail_cell


class StockWidgetFull(QVBoxLayout):
    def __init__(self, product):
        super().__init__()

        self.branch_cells = {}
        self.current_branch_cells = {"gross": StockTableCell(), "held": StockTableCell(), "available": StockTableCell()}
        self.warehouse_cells = {"warehouse": StockTableCell(), "3PL": StockTableCell()}
        self._initialise_widgets()
        self.set_product(product)
        self.update()

    def set_product(self, new_product):
        self.product = new_product
        self.product.stock_enquiry.updated.connect(self.update)
        self.refresh_button.pressed.connect(self.product.stock_enquiry.refresh)
        self.refresh_button.pressed.connect(self.disable_refresh_button)

    def disable_refresh_button(self):
        self.refresh_button.setDisabled(True)

    def update(self):
        self.refresh_button.setDisabled(False)
        self.product_name_label.setText(f"for  {self.product.sku} - {self.product.name}")
        try:
            self.current_branch_label.setText(self.product.stock_enquiry.stock.current_branch.name)
        except AttributeError:
            self.current_branch_label.setText("--")
        stock = self.product.stock_enquiry.stock
        self.current_branch_cells["gross"].setText(stock.get_current_branch_stock().gross)
        self.current_branch_cells["held"].setText(stock.get_current_branch_stock().held)
        self.current_branch_cells["available"].setText(stock.get_current_branch_stock().available)
        self.warehouse_cells["warehouse"].setText(stock.warehouse.available)
        self.warehouse_cells["3PL"].setText(stock.third_party_logistics.available)

        for branch, cell in self.branch_cells.items():
            try:
                cell.setText(self.product.stock_enquiry.stock[branch].available)
            except KeyError:
                pass
        if self.product.stock_enquiry.time_last_updated is not None:
            time_string = self.product.stock_enquiry.time_last_updated.strftime("%H:%M").strip()
            self.last_updated_label.setText(f"last refreshed at {time_string}")

        self.mrp_cell.setText(stock.mrp)
        self.rop_cell.setText(stock.reorder_point)

        if stock.deliveries_to_branch is not None:
            self.delivery_to_branch_layout.set_row_data(stock.deliveries_to_branch)
        if stock.deliveries_to_warehouse is not None:
            self.delivery_to_warehouse_layout.set_row_data(stock.deliveries_to_warehouse)

    def _initialise_widgets(self):
        island_layouts = []
        for name, island in [("North", Island.NORTH), ("South", Island.SOUTH)]:
            island_branches = ldglobal.branchdb.get_sorted_branches(island)
            island_table = BranchTable(island_branches, name)
            island_table.setMinimumWidth(270)
            self.branch_cells = {**self.branch_cells, **island_table.branch_cells}

            island_layout = QVBoxLayout()
            island_layout.addWidget(island_table)
            island_layout.addStretch()
            island_layouts.append(island_layout)

        branch_layout = QHBoxLayout()
        branch_layout.addLayout(island_layouts[0])
        branch_layout.addSpacing(10)
        branch_layout.addLayout(island_layouts[1])
        branch_layout.setAlignment(Qt.AlignTop)

        title_label = BetterLabel("Detailed Stock Report").setFontSize(28).setBold(True)
        title_label.setExpandingWidth().setAlignCenter()

        self.product_name_label = BetterLabel("").setFontSize(18).setBold(True)
        self.product_name_label.setWordWrap(False)
        self.product_name_label.setExpandingWidth().setAlignCenter()

        self.current_branch_label = BetterLabel("").setFontSize(16)
        self.current_branch_label.setExpandingWidth().setAlignCenter()

        current_branch_table = _ReadOnlyTableWidget(3, 2)
        current_branch_table.setFixedWidth(300)
        current_branch_table.setItem(0, 0, StockTableCell("ATP", True))
        current_branch_table.setItem(1, 0, StockTableCell("Held", True))
        current_branch_table.setItem(2, 0, StockTableCell("Available", True))
        current_branch_table.setItem(0, 1, self.current_branch_cells["gross"])
        current_branch_table.setItem(1, 1, self.current_branch_cells["held"])
        current_branch_table.setItem(2, 1, self.current_branch_cells["available"])
        current_branch_layout = QHBoxLayout()
        current_branch_layout.addStretch()
        current_branch_layout.addWidget(current_branch_table)
        current_branch_layout.addStretch()

        warehouses_label = BetterLabel("Warehouse Stock").setFontSize(16)
        warehouses_label.setExpandingWidth().setAlignCenter()

        warehouses_table = _ReadOnlyTableWidget(2, 2)
        warehouses_table.setFixedWidth(240)
        warehouses_table.setItem(0, 0, StockTableCell("Warehouse", True))
        warehouses_table.setItem(1, 0, StockTableCell("3PL*", True))
        warehouses_table.setItem(0, 1, self.warehouse_cells["warehouse"])
        warehouses_table.setItem(1, 1, self.warehouse_cells["3PL"])
        warehouses_layout = QHBoxLayout()
        warehouses_layout.addStretch()
        warehouses_layout.addWidget(warehouses_table)
        warehouses_layout.addStretch()

        threepl_label = BetterLabel("*3PL takes 2 additional days to ship").setFontSize(14)
        threepl_label.setStyleSheet("QLabel {color: #888888;}")
        threepl_label.setExpandingWidth().setAlignCenter()

        all_branches_label = BetterLabel("Available Stock From All Branches").setFontSize(16)
        all_branches_label.setWordWrap(False)
        all_branches_label.setExpandingWidth().setAlignCenter()

        self.last_updated_label = BetterLabel("").setFontSize(14)
        self.last_updated_label.setWordWrap(False)
        self.last_updated_label.setExpandingWidth().setAlignCenter()
        self.last_updated_label.setStyleSheet("QLabel {color: #888888;}")

        mrp_label = BetterLabel("MRP Controller").setFontSize(15)
        mrp_label.setExpandingWidth().setAlignCenter()
        self.mrp_cell = OneCellTable()
        self.mrp_cell.setMaximumWidth(160)
        mrp_layout = QVBoxLayout()
        mrp_layout.addWidget(mrp_label)
        mrp_layout.addWidget(self.mrp_cell)
        mrp_layout.addStretch()

        rop_label = BetterLabel("Reorder Point").setFontSize(15)
        rop_label.setExpandingWidth().setAlignCenter()
        self.rop_cell = OneCellTable()
        self.rop_cell.setMaximumWidth(120)
        rop_layout = QVBoxLayout()
        rop_layout.addWidget(rop_label)
        rop_layout.addWidget(self.rop_cell)
        rop_layout.addStretch()

        mrp_rop_layout = QHBoxLayout()
        mrp_rop_layout.addStretch()
        mrp_rop_layout.addLayout(mrp_layout)
        mrp_rop_layout.addSpacing(10)
        mrp_rop_layout.addLayout(rop_layout)
        mrp_rop_layout.addStretch()

        delivery_to_branch_label = BetterLabel("Deliveries to branch").setFontSize(15)
        delivery_to_branch_label.setExpandingWidth().setAlignCenter()
        self.delivery_to_branch_layout = DeliveryLayout(
            ["Req.", "Qty.", "Del. Date", "Origin"], columns_to_shrink=[0, 1]
        )

        delivery_to_warehouse_label = BetterLabel("Deliveries to warehouse").setFontSize(15)
        delivery_to_warehouse_label.setExpandingWidth().setAlignCenter()
        self.delivery_to_warehouse_layout = DeliveryLayout(["Qty.", "Del. Date", "Notes"], columns_to_shrink=[0, 1])

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setFixedWidth(100)
        refresh_layout = QHBoxLayout()
        refresh_layout.addStretch()
        refresh_layout.addWidget(self.refresh_button)
        refresh_layout.addStretch()

        left_vbox = QVBoxLayout()
        left_vbox.addWidget(self.current_branch_label)
        left_vbox.addLayout(current_branch_layout)
        left_vbox.addSpacing(10)
        left_vbox.addWidget(warehouses_label)
        left_vbox.addLayout(warehouses_layout)
        left_vbox.addWidget(threepl_label)
        left_vbox.addSpacing(20)
        left_vbox.addLayout(mrp_rop_layout)
        left_vbox.addSpacing(20)
        left_vbox.addWidget(delivery_to_branch_label)
        left_vbox.addLayout(self.delivery_to_branch_layout)
        left_vbox.addSpacing(10)
        left_vbox.addWidget(delivery_to_warehouse_label)
        left_vbox.addLayout(self.delivery_to_warehouse_layout)
        left_vbox.addSpacing(10)
        left_vbox.addStretch()
        left_vbox.addLayout(refresh_layout)
        left_vbox.addWidget(self.last_updated_label)
        # left_vbox.addStretch()

        right_vbox = QVBoxLayout()
        right_vbox.addLayout(branch_layout)
        right_vbox.addSpacing(20)
        right_vbox.addStretch()

        main_hbox = QHBoxLayout()
        main_hbox.addSpacing(30)
        main_hbox.addLayout(left_vbox)
        main_hbox.addSpacing(30)

        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Raised)
        main_hbox.addWidget(line)

        main_hbox.addSpacing(30)
        main_hbox.addLayout(right_vbox)
        main_hbox.addSpacing(30)

        self.addWidget(title_label)
        self.addWidget(self.product_name_label)
        self.addSpacing(20)
        self.addLayout(main_hbox)

        self.setContentsMargins(20, 20, 20, 15)
