from PyQt5.QtWidgets import QVBoxLayout
from ldproductbrowser.views import SearchQueryWidget, SearchResultsWidget


class SearchPane(QVBoxLayout):
    def __init__(self, database):
        super().__init__()

        self.db = database

        self.search_query_widget = SearchQueryWidget()
        self.search_results_widget = SearchResultsWidget()

        self.search_query_widget.queryChanged.connect(self._on_query_changed)
        self.search_results_widget.returnPressed.connect(self.search_query_widget._clear_search_bar)

        self.addLayout(self.search_query_widget)
        self.addWidget(self.search_results_widget)

        self.resultSelected = self.search_results_widget.resultSelected

    def _on_query_changed(self, search_query):
        if len(search_query) >= 2:
            search_results = self.db.search(search_query)
        else:
            search_results = None
        self.search_results_widget.populate(search_results)
