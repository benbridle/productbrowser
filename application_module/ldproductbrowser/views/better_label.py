from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor


class BetterLabel(QLabel):
    """
    A QLabel with a nicer API
    """

    clicked = pyqtSignal()

    def __init__(self, text):
        super().__init__(text)
        self.setWordWrap(True)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setCursor(QCursor(Qt.IBeamCursor))

    def setBold(self, bold):
        font = self.font()
        font.setBold(bold)
        self.setFont(font)
        return self

    def setFontSize(self, font_size):
        font = self.font()
        font.setPixelSize(font_size)
        self.setFont(font)
        return self

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

    def setColour(self, hex_code):
        self.setStyleSheet(f"color: {hex_code};")
        return self

    def setExpandingWidth(self):
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred))
        return self

    def setAlignCenter(self):
        self.setAlignment(Qt.AlignCenter)
        return self
