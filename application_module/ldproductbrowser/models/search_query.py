import re

range_regex = re.compile(r"\d+-\d+")


def extract_quoted_strings(query):
    """
    :return:
        quoted_strings:list
        query:str
    """
    quoted_strings = []

    while query.count('"') >= 2:
        opening_index = query.index('"')
        closing_index = query.index('"', opening_index + 1)
        quoted_str = query[opening_index + 1 : closing_index].strip()
        if len(quoted_str) > 0:
            quoted_strings.append(quoted_str)
        query = query[:opening_index] + " " + query[closing_index + 1 :]

    return quoted_strings, query


def clean_up_whitespace(query):
    while "  " in query:
        query = query.replace("  ", " ")
    query = query.strip()
    return query


def extract_ranges(query):
    words = clean_up_whitespace(query).split(" ")
    ranges = []
    for word in words:
        if not range_regex.match(word):
            continue
        lower_bound, upper_bound = word.split("-")
        lower_bound = int(lower_bound)
        upper_bound = int(upper_bound)
        if upper_bound < lower_bound:
            upper_bound, lower_bound = lower_bound, upper_bound
        lower_bound = max(lower_bound, 0)
        upper_bound = max(upper_bound, 0)
        ranges.append(range(lower_bound, upper_bound + 1))
    return ranges


def extract_numbers(query):
    numbers = []
    for word in query.split(" "):
        try:
            num = int(word)
        except ValueError:
            continue
        numbers.append(num)
    numbers = list(set(numbers))
    return numbers


class SearchQuery:
    """
    Parses a search query.
    Access .search_terms, .numbers, and .ranges for parsed data.
    """

    def __init__(self, search_query):
        quoted_strings, remaining_query = extract_quoted_strings(search_query)
        remaining_query = clean_up_whitespace(remaining_query).replace('"', "")

        self.search_terms = []
        unfiltered_search_terms = quoted_strings + remaining_query.split(" ")
        # Remove range terms from search terms
        for term in unfiltered_search_terms:
            if not range_regex.match(term):
                self.search_terms.append(term)

        self.numbers = extract_numbers(remaining_query)
        self.ranges = extract_ranges(remaining_query)
