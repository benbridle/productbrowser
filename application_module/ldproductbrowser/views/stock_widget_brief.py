from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView
from ldproductbrowser.views import StockTableCell, _ReadOnlyTableWidget, StockDialog


class StockWidgetBrief(_ReadOnlyTableWidget):

    clicked = pyqtSignal()

    def __init__(self):
        super().__init__(3, 2)
        self.initialise_table()
        self.product = None
        self.update()
        self.clicked.connect(self._on_click)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def update(self):
        self.branch_cell.setText(None)
        self.warehouse_cell.setText(None)
        self.all_branches_cell.setText(None)
        if self.product:
            stock = self.product.stock_enquiry.stock
            self.branch_cell.setText(stock.get_current_branch_stock().available)
            self.warehouse_cell.setText(stock.get_all_warehouse_stock().available)
            self.all_branches_cell.setText(stock.get_all_branches_stock().available)

    def set_product(self, new_product):
        self.product = new_product
        self.product.stock_enquiry.updated.connect(self.update)
        self.update()

    def initialise_table(self):
        self.branch_cell = StockTableCell("")
        self.warehouse_cell = StockTableCell("")
        self.all_branches_cell = StockTableCell("")

        self.setItem(0, 0, StockTableCell("Branch", True))
        self.setItem(1, 0, StockTableCell("Warehouse", True))
        self.setItem(2, 0, StockTableCell("All Branches", True))

        self.setItem(0, 1, self.branch_cell)
        self.setItem(1, 1, self.warehouse_cell)
        self.setItem(2, 1, self.all_branches_cell)

    def mousePressEvent(self, event):
        self.clicked.emit()

    def _on_click(self):
        stock_dialog = StockDialog(self, self.product)
        stock_dialog.exec_()
