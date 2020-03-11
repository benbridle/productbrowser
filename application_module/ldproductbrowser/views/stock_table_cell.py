from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class StockTableCell(QTableWidgetItem):
    def __init__(self, text=None, header=False):
        super().__init__(text)
        if header:
            self.foreground_colour = QColor("#182536")
            self.background_colour = QColor("#d2e5f7")
        else:
            self.foreground_colour = QColor("#000000")
            self.background_colour = QColor("#edf1f5")

        self.setText(text)
        self.setTextAlignment(Qt.AlignCenter)
        self.setForeground(self.foreground_colour)
        self.setBackground(self.background_colour)

    def setText(self, new_text, dim_if_zero=True):
        if new_text is None:
            new_text = "?"
        super().setText(str(new_text))
        if str(new_text) == "0" and dim_if_zero:
            self.setFaded(True)
        else:
            self.setFaded(False)

    def setFaded(self, state):
        if state:
            self.setForeground(QColor("#888888"))
        else:
            self.setForeground(self.foreground_colour)
