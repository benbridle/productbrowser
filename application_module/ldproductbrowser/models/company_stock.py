from collections import namedtuple
from ldproductbrowser.models import StockLevel, Branch

DeliveryToBranch = namedtuple("DeliveryToBranch", "quantity_requested quantity_delivered date origin")
DeliveryToWarehouse = namedtuple("DeliveryToWarehouse", "quantity status eta notes")


class CompanyStock:
    def __init__(self):
        self.branches = {}
        self.warehouse = StockLevel.none()
        self.third_party_logistics = StockLevel.none()
        self.current_branch = None
        self.eol = False
        self.mrp = None
        self.reorder_point = None
        self.deliveries_to_branch = None
        self.deliveries_to_warehouse = None

    def add_branch_stock(self, branch, stock_level):
        if not isinstance(branch, Branch):
            raise ValueError("branch must be of type Branch")
        if not isinstance(stock_level, StockLevel):
            raise ValueError("stock_level must be of type StockLevel")
        self.branches[branch] = stock_level

    def __getitem__(self, key):
        if key in self.branches:
            return self.branches[key]
        raise KeyError(f"No key '{key}'")

    def get_total_stock(self):
        return self._add_stock_levels(list(self.branches.values()) + [self.warehouse, self.third_party_logistics])

    def get_all_branches_stock(self):
        if len(self.branches) == 0:
            return StockLevel.none()
        return self._add_stock_levels(list(self.branches.values()))

    def get_current_branch_stock(self):
        if self.current_branch is None:
            return StockLevel.none()
        return self.branches[self.current_branch]

    def get_all_warehouse_stock(self):
        return self._add_stock_levels([self.warehouse, self.third_party_logistics])

    def _add_stock_levels(self, stock_levels):
        new_stock_level = StockLevel(0, 0, 0)
        for stock_level in stock_levels:
            if stock_level.gross is not None:
                new_stock_level.gross += stock_level.gross
            else:
                return StockLevel.none()
            if stock_level.held is not None:
                new_stock_level.held += stock_level.held
            else:
                return StockLevel.none()
            if stock_level.available is not None:
                new_stock_level.available += stock_level.available
            else:
                return StockLevel.none()
        return new_stock_level
