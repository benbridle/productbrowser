from ldproductbrowser.models import _BaseDatabaseModel, SearchQuery, SearchResult, Product, SdocFinder, ProductCache
from ldproductbrowser import globals as ldglobal


class ProductDatabase(_BaseDatabaseModel):
    """
    Model for interacting with a product database at a high level.
    """

    def __init__(self, database_file_path):
        super().__init__(database_file_path)
        results = self.execute("SELECT sku,name FROM products").fetchall()
        self.name_lookup = {result[0]: result[1] for result in results}
        sdoc_folder_path = ldglobal.app_context.get_resource("sdocs")
        self.sdoc_finder = SdocFinder(sdoc_folder_path)
        cache_size = ldglobal.settings["Products"].getint("cache_size")
        self.product_cache = ProductCache(cache_size)

    def _match_barcode_to_sku(self, barcode):
        c = self.db.execute("SELECT sku FROM barcodes WHERE barcode=? LIMIT 1", [barcode])
        result = c.fetchone()
        if result:
            return result[0]
        return None

    def _search_product_names(self, search_terms):
        if not isinstance(search_terms, (list, tuple, set)):
            raise TypeError("search_terms must be a list, tuple, or set")
        if len(search_terms) == 0:
            return []
        query = "SELECT sku FROM products WHERE "
        search_terms = [f"%{term}%" for term in search_terms]
        query += " AND ".join(["name LIKE ?"] * len(search_terms)) + ";"
        c = self.execute(query, search_terms)
        skus = [x[0] for x in c.fetchall()]  # Pull skus out of tuples
        return skus

    def _has_sku(self, sku):
        c = self.execute("SELECT sku FROM products WHERE sku=?", [sku])
        result = c.fetchone()
        if result:
            return True
        return False

    def _get_skus_in_range(self, sku_range):
        if not isinstance(sku_range, range):
            raise TypeError("sku_range must be of type 'range'")
        start = sku_range[0]
        end = sku_range[-1]
        c = self.execute(f"SELECT sku FROM products WHERE sku>=? AND sku<=?", [start, end])
        skus_found = [result[0] for result in c.fetchall()]
        return skus_found

    def _composite_search(self, search_query):
        """
        First find exact barcode matches. If multiple products share the same
         barcode, include both.
        Second, find exact SKU matches.
        Third, find product name matches (matching _all_ search terms)
        Fourth, match against sku ranges
        Keep all barcode matches and exact sku matches.
        If there are name matches AND sku range matches, keep only the INTERSECTION of both sets.
        Otherwise keep both name matches and sku range matches.
        """
        sq = SearchQuery(search_query)

        barcode_search = []
        for number in sq.numbers:
            barcode = self._match_barcode_to_sku(number)
            if barcode:
                barcode_search.append(barcode)

        sku_search = []
        for number in sq.numbers:
            if self._has_sku(number):
                sku_search.append(number)

        name_search = self._search_product_names(sq.search_terms)

        range_search = []
        for sku_range in sq.ranges:
            range_search += self._get_skus_in_range(sku_range)

        matching_skus = barcode_search + sku_search

        if name_search and range_search:
            # The intersection of name_search and range_search
            matching_skus += list(set(name_search) & set(range_search))
        else:
            matching_skus += name_search
            matching_skus += range_search

        return matching_skus

    def search(self, search_query):
        matching_skus = self._composite_search(search_query)
        search_results = [SearchResult(self.name_lookup[sku], sku) for sku in matching_skus]
        return search_results

    def get_product(self, sku):
        cached_product = self.product_cache.get(sku)
        if cached_product:
            return cached_product
        c = self.execute("SELECT * FROM products WHERE sku=?", [sku])
        product = Product.from_cursor(c)
        product.sdoc_path = self.sdoc_finder.get_sdoc_path(product.sku)
        self.product_cache.add(product)
        return product
