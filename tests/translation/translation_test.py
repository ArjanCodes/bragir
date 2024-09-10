from bragir.translation import split_by_breakpoints


def test_basic_functionality():
    assert split_by_breakpoints([1, 2, 3, 4, 5], [2, 4]) == [[1, 2], [3, 4], [5]]


def test_empty_list():
    assert split_by_breakpoints([], [1, 3]) == []


def test_single_element_list():
    assert split_by_breakpoints([1], [1]) == [1]


def test_breakpoints_at_start_and_end():
    assert split_by_breakpoints([1, 2, 3], [0, 3]) == [[1, 2, 3]]


def test_no_breakpoints():
    assert split_by_breakpoints([1, 2, 3], []) == [[1, 2, 3]]


def test_repeated_breakpoints():
    assert split_by_breakpoints([1, 2, 3, 4], [2, 2]) == [[1, 2], [3, 4]]


def test_out_of_range_breakpoints():
    assert split_by_breakpoints([1, 2, 3], [4]) == [[1, 2, 3]]
