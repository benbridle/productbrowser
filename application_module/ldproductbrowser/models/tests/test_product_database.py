from os.path import realpath, dirname, join
import pytest
from ldproductbrowser.models import ProductDatabase, SearchResult


@pytest.fixture
def db():
    test_product_database_path = join(dirname(realpath(__file__)), "data/test_product_database.db")
    database = ProductDatabase(test_product_database_path)
    return database


def test_execute(db):
    c = db.execute("SELECT name FROM products WHERE sku=?;", [1000])
    assert c.fetchone()[0] == "Light 1"


def test_match_barcode_to_sku(db):
    assert db._match_barcode_to_sku(11111111) == 1000
    assert db._match_barcode_to_sku(12345678) == 1000
    assert db._match_barcode_to_sku(8888) is None


def test_search_product_names(db):
    assert set(db._search_product_names(["light"])) == {1000, 2000, 3000, 4000, 5000}
    assert set(db._search_product_names(["four"])) == {4000, 5000}
    assert set(db._search_product_names(["FoUR"])) == {4000, 5000}
    assert set(db._search_product_names(["li", "igh", "1"])) == {1000}
    assert db._search_product_names([]) == []
    with pytest.raises(TypeError):
        db._search_product_names("light")


def test_has_sku(db):
    assert db._has_sku(1000)
    assert not db._has_sku(1005)
    assert not db._has_sku(None)
    assert not db._has_sku(-300)
    assert db._has_sku("1000")
    assert not db._has_sku("a")


def test_get_skus_in_range(db):
    assert set(db._get_skus_in_range(range(500, 1500))) == {1000}
    assert set(db._get_skus_in_range(range(1800, 3500))) == {2000, 3000}
    with pytest.raises(TypeError):
        db._get_skus_in_range([100])


def test_composite_search(db):
    assert db._composite_search("four light") == [4000, 5000]
    assert db._composite_search("11111111 55555555") == [5000, 1000]
    assert db._composite_search("11111111 v2") == [1000]
    assert db._composite_search("4500-1 four") == [4000]
    assert db._composite_search("") == [1000, 2000, 3000, 4000, 5000]


def test_search(db):
    assert db.search("v2 light") == [SearchResult("Light four v2", 5000)]
    assert db.search("v2 light 11111111") == [SearchResult("Light 1", 1000)]


def test_get_product(db):
    product = db.get_product(1000)
    assert product.name == "Light 1"
    assert product.sku == 1000
