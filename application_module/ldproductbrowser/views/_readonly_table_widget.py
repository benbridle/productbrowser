from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView
from PyQt5.QtCore import Qt


class _ReadOnlyTableWidget(QTableWidget):
    def __init__(self, width, height):
        super().__init__()
        self.setColumnCount(width)
        self.setRowCount(height)

        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # self.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
        # self.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")

        self.verticalHeader().hide()
        self.horizontalHeader().hide()

        self.setFocusPolicy(Qt.NoFocus)

        self.setFixedHeight(height * 30)

        self.setStyleSheet(
            "QTableView {gridline-color: #94b4e0; border: 1px solid #94b4e0; border-right: none; border-bottom: none;}"
        )

    def setItem(self, column, row, cell):
        super().setItem(row, column, cell)

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass
