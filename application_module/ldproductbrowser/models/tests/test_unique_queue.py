from ldproductbrowser.models import UniqueQueue


def test_unique_queue():
    uq = UniqueQueue()
    uq.put("number", 1)
    assert uq.get() == 1
    uq.put("number", 2)
    uq.put("number", 3)
    assert uq.get() == 3
    uq.put("number", 4)
    uq.put("number", 5)
    uq.put("letter", "a")
    assert uq.get() == 5
    assert uq.get() == "a"
