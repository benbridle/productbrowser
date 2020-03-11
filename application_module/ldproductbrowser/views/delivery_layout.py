from ldproductbrowser.views import _ReadOnlyTableWidget, OneCellTable, StockTableCell
from PyQt5.QtWidgets import QVBoxLayout, QHeaderView, QSizePolicy


class DeliveryTable(_ReadOnlyTableWidget):
    def __init__(self, rows, headers, columns_to_shrink):
        super().__init__(len(headers), 1 + len(rows))

        header = self.horizontalHeader()
        for i, j in enumerate(headers):
            if i in columns_to_shrink:
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
            else:
                header.setSectionResizeMode(i, QHeaderView.Stretch)

        for i, header in enumerate(headers):
            self.setItem(i, 0, StockTableCell(header, True))

        for i, row in enumerate(rows):
            for j, element in enumerate(row):
                self.setItem(j, i + 1, StockTableCell(element))


class DeliveryLayout(QVBoxLayout):
    def __init__(self, table_headers, columns_to_shrink=None):
        super().__init__()
        self.columns_to_shrink = columns_to_shrink or []
        self.table_headers = table_headers
        self.table = OneCellTable("loading...")
        self.table.setFaded(True)
        self.addWidget(self.table)

    def set_row_data(self, rows):
        self._clear_table()
        if len(rows) == 0:
            no_deliveries_table = OneCellTable("No deliveries found")
            no_deliveries_table.setFaded(True)
            self.table = no_deliveries_table
            self.addWidget(self.table)
        else:
            self.table = DeliveryTable(rows, self.table_headers, self.columns_to_shrink)
            self.table.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
            width = 20
            for i, _ in enumerate(self.table_headers):
                width += self.table.sizeHintForColumn(i)
            self.table.setMinimumWidth(width)
            self.addWidget(self.table)

    def _clear_table(self):
        self.table.setParent(None)
        self.removeWidget(self.table)
