from enum import Enum
from typing import Any, Type


class Languages(Enum):
    PORTUGUESE = "Portuguese"
    SPANISH = "Spanish"
    FRENCH = "French"
    GERMAN = "German"
    ITALIAN = "Italian"


def to_output(enum_class: Type[Enum]) -> str:
    formatted_enum = " ".join([f"{enum.value}" for enum in enum_class])
    return formatted_enum


def parse_languages(input_languages: Any):
    valid_languages: list[Languages] = []
    valid_string_languages = [language.value.lower() for language in Languages]

    for target_language in input_languages:
        if target_language.lower() in valid_string_languages:
            valid_languages.append(Languages[target_language.upper()])

    return valid_languages