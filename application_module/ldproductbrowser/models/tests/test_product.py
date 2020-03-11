from ldproductbrowser.models import Product


def test_product():
    product = Product("Light", 12345)
    assert product.name == "Light"
    assert product.sku == 12345
    assert product.product_page_url == "https://www.lightingdirect.co.nz/print_product.html/x_sku/12345.html"

    assert len(product.barcodes) == 0
    product.add_barcode(12345678)
    assert len(product.barcodes) == 1
    assert 12345678 in product.barcodes
