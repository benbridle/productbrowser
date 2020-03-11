from ldproductbrowser.views import _ReadOnlyTableWidget, StockTableCell


class OneCellTable(_ReadOnlyTableWidget):
    def __init__(self, text=None):
        super().__init__(1, 1)
        self.cell = StockTableCell(text)
        self.setItem(0, 0, self.cell)

    def setText(self, text):
        self.cell.setText(text)

    def setFaded(self, state):
        self.cell.setFaded(state)
