class StockLevel:
    def __init__(self, gross, held, available):
        self.gross = gross
        self.held = held
        self.available = available

    @classmethod
    def none(cls):
        return cls(None, None, None)
