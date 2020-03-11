from ldproductbrowser.tools.data_validation import is_sku


class SearchResult:
    """
    A basic data structure for holding a product name and SKU.
    """

    def __init__(self, name, sku):
        self.name = name
        self.sku = sku

    def __repr__(self):
        return f"SearchResult('{self._name}', {self.sku})"

    def __eq__(self, other):
        return self._name == other._name and self._sku == other._sku

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, (str, type(None))):
            self._name = new_name
        else:
            raise TypeError("Name must be a str")

    @property
    def sku(self):
        return self._sku

    @sku.setter
    def sku(self, new_sku):
        if is_sku(new_sku) or new_sku is None:
            self._sku = new_sku
        else:
            raise ValueError(f"'{new_sku}' is not a valid SKU")
