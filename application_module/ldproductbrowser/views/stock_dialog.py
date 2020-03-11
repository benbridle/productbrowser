from PyQt5.QtWidgets import QDialog
from ldproductbrowser.views import StockWidgetFull


class StockDialog(QDialog):
    def __init__(self, parent, product):
        super().__init__(parent)
        self.setSizeGripEnabled(False)
        self.layout = StockWidgetFull(product)
        self.setLayout(self.layout)
        #self.setFixedSize(self.sizeHint())
