from os.path import realpath, dirname, join, basename
from ldproductbrowser.models import SdocFinder


def test_sdoc_finder():
    sdoc_folder_path = join(dirname(realpath(__file__)), "data/test_sdocs")
    sdf = SdocFinder(sdoc_folder_path)
    assert basename(sdf.get_sdoc_path(300)) == "1 2 300.pdf"
    assert basename(sdf.get_sdoc_path(2)) == "2 40 50.pdf"
    assert sdf.get_sdoc_path("a") is None
    assert sdf.get_sdoc_path("@#$") is None
