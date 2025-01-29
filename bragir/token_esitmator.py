import re

TOKEN_REGEX = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def get_number_of_tokens(content: str) -> int:
    words = re.findall(TOKEN_REGEX, content, re.UNICODE)
    return len(words) + content.count(" ")
