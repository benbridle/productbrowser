from PyQt5.QtWidgets import QDialog, QSizePolicy, QHBoxLayout, QVBoxLayout, QLayout
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QDesktopServices, QCursor
from ldproductbrowser.views import BetterLabel, ImageWidget
from ldproductbrowser import globals as ldglobal


class SearchHelpDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        expanding_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        title_label = BetterLabel("Hints for using the Search Bar").setFontSize(20).setBold(True)
        title_label.setSizePolicy(expanding_policy)
        title_label.setAlignment(Qt.AlignHCenter)

        help_text = (
            "To quickly clear the search bar for a new search, press [ENTER]."
            + "\n\n"
            + "Use the _ character to replace an unknown letter or number.  "
            + "For example, searching cort_d_r_s will correctly match the name CORTADERAS."
            + "\n\n"
            + "Search a SKU number to show that product. Scanning a barcode directly into the search bar works too."
            + "\n\n"
            + "Type two SKU numbers separated by a dash to show all products in that range. For example, typing "
            + "18737-18739 will show the products 18737, 18738, and 18739."
        )
        help_label = BetterLabel(help_text).setFontSize(14)
        help_label.setSizePolicy(expanding_policy)

        vbox = QVBoxLayout()
        vbox.addSpacing(10)
        vbox.addWidget(title_label)
        vbox.addSpacing(10)
        vbox.addWidget(help_label)

        vbox.setAlignment(Qt.AlignHCenter)
        self.setLayout(vbox)

        self.setFixedSize(self.sizeHint())
