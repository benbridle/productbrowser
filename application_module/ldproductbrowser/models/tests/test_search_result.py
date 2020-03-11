import pytest
from ldproductbrowser.models import SearchResult


def test_search_result():
    sr = SearchResult("Light name", 12345)
    assert sr.name == "Light name"
    assert sr.sku == 12345
    with pytest.raises(ValueError):
        sr.sku = -100
    with pytest.raises(ValueError):
        sr.sku = "13456"
    sr.sku = 1000
    assert sr.sku == 1000
    with pytest.raises(TypeError):
        sr.name = 123
    sr.name = "New name"
    assert sr.name == "New name"
