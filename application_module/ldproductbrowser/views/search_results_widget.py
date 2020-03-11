from PyQt5.QtWidgets import QTreeView, QAbstractItemView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QStandardItemModel

from ldproductbrowser.models import SearchResult


class Column:
    SKU = 0
    NAME = 1


class SearchResultsWidget(QTreeView):

    resultSelected = pyqtSignal(SearchResult)
    returnPressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.search_results = None
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def selectionChanged(self, *args, **kwargs):
        """
        Overridden to emit a rowSelected(row_index) signal when a search result is selected.
        """
        try:
            row_index = args[0].indexes()[0].row()
        except IndexError:
            row_index = 0
        if self.search_results is not None and self.search_results != []:
            self.resultSelected.emit(self.search_results[::-1][row_index])
        else:
            self.resultSelected.emit(SearchResult(None, None))
        return super().selectionChanged(*args, **kwargs)

    def populate(self, search_results):
        """
        Receives a list of SearchResults, and puts them all into the search results widget.
        If search_results is None, the displayed list will be empty. This is for before the user has started typing.
        If search_results is an empty list, a "No results" error will be shown. This is to communicate to the user that no product has matched their search.
        Otherwise, populate the view as normal.
        """
        self.search_results = search_results

        search_results_model = self.get_search_results_model()
        # To display an empty list
        if search_results is None:
            self.setModel(search_results_model)
            return

        if len(search_results) == 0:
            search_results_model.insertRow(0)
            search_results_model.setData(search_results_model.index(0, Column.SKU), "")
            search_results_model.setData(search_results_model.index(0, Column.NAME), "No products found")
            search_results_model.insertRow(0)

        else:
            # to reverse the list, slice here with [::-1]
            for product in search_results:
                search_results_model.insertRow(0)
                search_results_model.setData(search_results_model.index(0, Column.SKU), product.sku)  # .sku)
                search_results_model.setData(search_results_model.index(0, Column.NAME), product.name)  # .name)
        self.setModel(search_results_model)

    def get_search_results_model(self):
        """
        Sets up and returns an empty model that will be used to hold search result information.
        """
        search_results_model = QStandardItemModel(0, 2, self)
        search_results_model.setHeaderData(Column.SKU, Qt.Horizontal, "SKU")
        search_results_model.setHeaderData(Column.NAME, Qt.Horizontal, "Product Name")
        return search_results_model

    def keyPressEvent(self, e):
        if e.text() == "\r":
            self.returnPressed.emit()
        else:
            super().keyPressEvent(e)
