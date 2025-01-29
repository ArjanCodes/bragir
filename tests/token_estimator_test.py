from bragir.token_esitmator import get_number_of_tokens


def test_basic_functionality():
    assert get_number_of_tokens("Hello, world!") == 5  # "Hello", ",", " ", "world", "!"


def test_empty_string():
    assert get_number_of_tokens("") == 0


def test_single_word():
    assert get_number_of_tokens("Hello") == 1


def test_multiple_spaces():
    assert get_number_of_tokens("Hello   world") == 5  # "Hello", " ", " ", " ", "world"


def test_punctuation():
    assert get_number_of_tokens("Hello, world!") == 5  # "Hello", ",", " ", "world", "!"


def test_only_punctuation():
    assert get_number_of_tokens("!.,;") == 4  # "!", ".", ",", ";"


def test_mixed_characters():
    assert get_number_of_tokens("Hello-world") == 3  # "Hello", "-", "world"


def test_unicode_characters():
    assert get_number_of_tokens("你好，世界！") == 4  # "你好", "，", "世界", "！"


def test_whitespace_variations():
    assert get_number_of_tokens("Hello\nworld") == 2  # "Hello", "\n", "world"
