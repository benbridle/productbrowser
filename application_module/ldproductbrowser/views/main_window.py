from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QAction
from ldproductbrowser.models import ProductDatabase
from ldproductbrowser.views import SearchPane, ProductPane, AboutDialog, SearchHelpDialog
from ldproductbrowser.views.bottom_bar import BottomBar
from ldproductbrowser import globals as ldglobal


class ProductBrowserWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self):
        super().__init__()
        self.resize(1000, 800)
        self._initialise_menu_bar()
        self._initialise_widgets()
        self.search_pane.resultSelected.connect(self._on_search_result_selected)
        self.product_pane.returnPressed.connect(self.search_pane.search_query_widget._clear_search_bar)

    def _show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def _show_search_help_dialog(self):
        search_help_dialog = SearchHelpDialog(self)
        search_help_dialog.exec_()

    def _initialise_menu_bar(self):
        search_help_action = QAction("Hints", self)
        search_help_action.triggered.connect(self._show_search_help_dialog)
        self.menuBar().addAction(search_help_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about_dialog)
        self.menuBar().addAction(about_action)

    def _initialise_widgets(self):
        panes_layout = QHBoxLayout()
        self.product_pane = ProductPane(width=300)
        self.search_pane = SearchPane(database=ldglobal.productdb)

        panes_layout.addLayout(self.search_pane)
        panes_layout.addWidget(self.product_pane)

        main_layout = QVBoxLayout()
        main_layout.addLayout(panes_layout)
        main_layout.addLayout(BottomBar(database=ldglobal.productdb))

        w = QWidget()
        w.setLayout(main_layout)
        self.setCentralWidget(w)

    def _on_search_result_selected(self, search_result):
        if search_result.name is None:
            self.product_pane.setProduct(None)
            return
        product = ldglobal.productdb.get_product(search_result.sku)
        self.product_pane.setProduct(product)
