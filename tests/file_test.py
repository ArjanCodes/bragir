from bragir.file import group_values


# Mock the number_of_tokens function for testing purposes
def mock_number_of_tokens(value: str) -> int:
    # For simplicity, assume each character is one token
    return len(value)


# Tests for the group_values function
def test_empty_list():
    result = group_values([], 10, mock_number_of_tokens)
    assert result == [], "Expected empty list for empty input"


def test_single_item_below_limit():
    result = group_values(["short"], 10, mock_number_of_tokens)
    assert result == [["short"]], "Expected single chunk with one item"


def test_single_item_exceeds_limit():
    result = group_values(["thisisaverylongword"], 5, mock_number_of_tokens)
    assert result == [
        ["thisisaverylongword"]
    ], "Expected single chunk even if it exceeds limit"


def test_multiple_items_within_limit():
    result = group_values(["a", "bb", "ccc"], 10, mock_number_of_tokens)
    assert result == [
        ["a", "bb", "ccc"]
    ], "Expected single chunk since total tokens are within limit"


def test_multiple_items_exceed_limit():
    result = group_values(["a", "bb", "ccc", "dddd"], 5, mock_number_of_tokens)
    assert result == [["a", "bb"], ["ccc", "dddd"]], "Expected chunks to respect limit"


def test_items_split_at_limit_boundary():
    result = group_values(["a", "bb", "ccc", "d"], 4, mock_number_of_tokens)
    assert result == [
        ["a", "bb"],
        ["ccc", "d"],
    ], "Expected chunks to split at exact boundary"


def test_limit_reached_multiple_times():
    result = group_values(
        ["one", "two", "three", "four", "five", "six"], 8, mock_number_of_tokens
    )
    assert result == [
        ["one", "two"],
        ["three", "four"],
        ["five", "six"],
    ], "Expected balanced chunks with respect to limit"


def test_longer_token_count_than_limit():
    result = group_values(
        ["supercalifragilisticexpialidocious"], 5, mock_number_of_tokens
    )
    assert result == [
        ["supercalifragilisticexpialidocious"]
    ], "Expected single chunk with long item that exceeds limit"


def test_limit_boundary_not_exceeded():
    result = group_values(["a", "bb", "ccc", "dd"], 5, mock_number_of_tokens)
    assert result == [
        ["a", "bb"],
        ["ccc", "dd"],
    ], "Expected chunks to split when adding a token exceeds the limit"
