import time
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt


class SearchQueryWidget(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.search_bar = SearchBar()
        self.search_bar.returnPressed.connect(self._clear_search_bar)
        self.queryChanged = self.search_bar.textChanged

        self.clear_button = QPushButton("Clear search")
        self.clear_button.clicked.connect(self._clear_search_bar)

        self.addWidget(QLabel("Type SKU or name:"))
        self.addWidget(self.search_bar)
        self.addWidget(self.clear_button)

        # Give search_bar focus on program launch
        QTimer().singleShot(0, Qt.PreciseTimer, self.search_bar.setFocus)

    def _clear_search_bar(self):
        """Clears the search bar."""
        self.search_bar.setText("")
        self.search_bar.setFocus()


class SearchBar(QLineEdit):
    def __init__(self):
        super().__init__()
        self.last_query_update_time = 0
        self.barcode_scanner_safety_time = 0.1

    def keyPressEvent(self, e):
        if e.text() == "\r":
            if time.time() - self.barcode_scanner_safety_time > self.last_query_update_time:
                self.returnPressed.emit()
            else:
                last_word = self.text().split(" ")[-1]
                self.setText(last_word + " ")
        else:
            self.last_query_update_time = time.time()
            super().keyPressEvent(e)
