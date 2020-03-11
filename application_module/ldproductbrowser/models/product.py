from ldproductbrowser.tools.data_validation import is_barcode
from ldproductbrowser.models import StockEnquiry


class Product:
    """
    Represents a single Lighting Direct product.
    """

    def __init__(self, name, sku):
        self.name = name
        self.sku = sku
        self.barcodes = []
        self.website_url = None
        self.sdoc_path = None
        self.image = None

        self.description = None
        self.specifications = None
        self.features = None
        self.applications = None

        self.stock_enquiry = StockEnquiry(sku)

    @classmethod
    def from_cursor(cls, cursor):
        product_row = cursor.fetchone()
        headers = [description[0] for description in cursor.description]  # pull column headers from cursor
        product_attributes = dict(zip(headers, product_row))
        product = cls(product_attributes["name"], product_attributes["sku"])
        product.image = product_attributes["image"]
        product.website_url = product_attributes["website_url"]
        product.description = product_attributes["description"]
        product.specifications = product_attributes["specifications"]
        product.features = product_attributes["features"]
        product.applications = product_attributes["applications"]
        return product

    def add_barcode(self, new_barcode):
        if is_barcode(new_barcode):
            self.barcodes.append(new_barcode)
        else:
            raise ValueError(f"'{new_barcode}' is not a valid barcode")

    @property
    def product_page_url(self):
        return f"https://www.lightingdirect.co.nz/print_product.html/x_sku/{self.sku}.html"
