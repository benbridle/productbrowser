from ldproductbrowser.tools.data_validation import is_barcode, is_sku, is_branch_id


def test_is_barcode():
    assert is_barcode(12345678)
    assert not is_barcode("12345678")
    assert not is_barcode(1234)
    assert not is_barcode(None)
    assert not is_barcode("")
    assert not is_barcode(145678612.0)
    assert not is_barcode(-12345678)


def test_is_sku():
    assert is_sku(12345)
    assert not is_sku(-12345)
    assert not is_sku("12345")
    assert not is_sku(None)


def test_is_branch_id():
    assert is_branch_id(1)
    assert is_branch_id(2000)
    assert not is_branch_id(-1)
    assert not is_branch_id(0)
    assert not is_branch_id(-2000)
    assert not is_branch_id("1")
    assert not is_branch_id("13")
    assert not is_branch_id(None)
