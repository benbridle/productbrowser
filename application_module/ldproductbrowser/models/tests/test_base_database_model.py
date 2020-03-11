from os.path import realpath, dirname, join
from ldproductbrowser.models import _BaseDatabaseModel


def test_base_database_model():
    test_product_database_path = join(dirname(realpath(__file__)), "data/test_product_database.db")
    db = _BaseDatabaseModel(test_product_database_path)

    c = db.execute("SELECT name FROM products WHERE sku=?;", [1000])
    assert c.fetchone()[0] == "Light 1"

    c = db.execute("SELECT * FROM products;")
    assert len(c.fetchall()) == 5
