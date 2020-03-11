from ldproductbrowser.models import SearchQuery
from ldproductbrowser.models.search_query import (
    extract_quoted_strings,
    clean_up_whitespace,
    extract_ranges,
    extract_numbers,
)


def test_clean_up_whitespace():
    assert clean_up_whitespace(" word    other word   ") == "word other word"
    assert clean_up_whitespace("123") == "123"
    assert clean_up_whitespace("Abc          ") == "Abc"


def test_extract_quoted_strings():
    quoted_strings, remaining_query = extract_quoted_strings('text  "two words""123 numbers" 2000')
    assert set(quoted_strings) == {"two words", "123 numbers"}
    assert remaining_query == "text     2000"  # Each quoted string is replaced by a single space


def test_extract_ranges():
    assert set(extract_ranges(" a10-20 100-200  15- 18 400-300 aA ")) == {
        range(100, 201),
        range(300, 401),
    }
    assert set(extract_ranges("10-10")) == {range(10, 11)}


def test_extract_numbers():
    assert set(extract_numbers(" 1  0.2 1000 a  ")) == {1, 1000}


def test_search_query():
    s = SearchQuery('words text "2000 more"    12345 2000-1000 1  ')
    assert set(s.search_terms) == {"words", "text", "2000 more", "12345", "1"}
    assert set(s.numbers) == {12345, 1}
    assert set(s.ranges) == {range(1000, 2001)}
