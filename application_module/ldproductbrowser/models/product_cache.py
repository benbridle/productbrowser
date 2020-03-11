class ProductCache:
    def __init__(self, cache_size):
        if not isinstance(cache_size, int):
            raise TypeError("cache_size must be an int")
        self._cache = {}
        self._insertion_order = []
        self._cache_size = cache_size

    def __len__(self):
        return len(self._cache)

    def add(self, new_product):
        self._cache[new_product.sku] = new_product
        self._insertion_order.append(new_product.sku)
        while len(self._insertion_order) > self._cache_size:
            del self._cache[self._insertion_order.pop(0)]

    def get(self, sku):
        if not sku in self._cache:
            return None
        return self._cache[sku]
