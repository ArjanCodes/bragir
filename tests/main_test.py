from main import parse_languages, Languages

def test_parse_languages_valid():
    input_languages = ['Portuguese', 'spanish', 'ITALIAN']
    result = parse_languages(input_languages)
    assert result == [Languages.PORTUGUESE, Languages.SPANISH, Languages.ITALIAN]

def test_parse_languages_invalid():
    input_languages = ['French', 'german', 'UnknownLanguage']
    result = parse_languages(input_languages)
    assert result == [Languages.FRENCH, Languages.GERMAN]

def test_parse_languages_empty():
    input_languages = []
    result = parse_languages(input_languages)
    assert result == []

def test_parse_languages_mixed_valid_invalid():
    input_languages = ['Portuguese', 'French', 'spanish', 'UnknownLanguage', 'german']
    result = parse_languages(input_languages)
    assert result == [Languages.PORTUGUESE, Languages.FRENCH, Languages.SPANISH, Languages.GERMAN]
