# Tests for check_first_is_quote
from bragir.post_processing import (
    check_first_is_quote,
    check_last_is_quote,
    process_text,
    remove_all_newline_before_first_character,
    remove_newline_in_the_middle,
    remove_quoutes,
    remove_space,
    remove_space_as_first_character,
)


def test_check_first_is_quote_true():
    assert not check_first_is_quote("Hello")


def test_check_first_is_quote_false():
    assert check_first_is_quote('"Hello')


def test_check_first_is_quote_with_space():
    assert not check_first_is_quote(" No quotes")


# Tests for check_last_is_quote
def test_check_last_is_quote_true():
    assert not check_last_is_quote("Hello")


def test_check_last_is_quote_false():
    assert check_last_is_quote('Hello"')


def test_check_last_is_quote_with_space():
    assert not check_last_is_quote("No quotes ")


# Tests for remove_quotes
def test_remove_quotes_both_sides():
    assert remove_quoutes('"Hello"') == "Hello"


def test_remove_quotes_only_start():
    assert remove_quoutes('"Already processed" text') == 'Already processed" text'


def test_remove_quotes_no_quotes():
    assert remove_quoutes("Hello") == "Hello"


# Tests for remove_space
def test_remove_space_beginning():
    assert remove_space(" Hello", 0) == "Hello"


def test_remove_space_end():
    assert remove_space("Hello ", 5) == "Hello"


# Tests for remove_space_as_first_character
def test_remove_space_as_first_character_with_space():
    assert remove_space_as_first_character(" Hello") == "Hello"


def test_remove_space_as_first_character_no_space():
    assert remove_space_as_first_character("Hello") == "Hello"


def test_remove_space_as_first_character_with_multiple_words():
    assert remove_space_as_first_character(" Hello World") == "Hello World"


# Tests for remove_all_newline_before_first_character
def test_remove_all_newline_before_first_character_leading_newlines():
    assert remove_all_newline_before_first_character("\n\nHello") == "Hello"


def test_remove_all_newline_before_first_character_no_newlines():
    assert remove_all_newline_before_first_character("Hello") == "Hello"


def test_remove_all_newline_before_first_character_mixed_newlines():
    assert (
        remove_all_newline_before_first_character("\n\nHello\nWorld") == "Hello\nWorld"
    )


# Tests for remove_newline_in_the_middle
def test_remove_newline_in_the_middle_simple():
    assert remove_newline_in_the_middle("Hello\nWorld") == "Hello World"


def test_remove_newline_in_the_middle_complex():
    assert remove_newline_in_the_middle("\nStart\nMiddle\nEnd") == "\nStart Middle End"


# Tests for process_text
def test_process_text_example_1():
    text1 = "come si traduce in codice reale. E cosa \n\nquesto effettivamente"
    expected1 = "come si traduce in codice reale. E cosa questo effettivamente"
    assert process_text(text1) == expected1


def test_process_text_example_2():
    text2 = "\n\nUn database, puoi memorizzarli come file, puoi fare molte cose con\n"
    expected2 = "Un database, puoi memorizzarli come file, puoi fare molte cose con\n"
    assert process_text(text2) == expected2


def test_process_text_example_3():
    text3 = '"Sicuramente usa un database. Ma qui, lo sto facendo così."'
    expected3 = "Sicuramente usa un database. Ma qui, lo sto facendo così."
    assert process_text(text3) == expected3
