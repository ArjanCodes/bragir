from dataclasses import field
from io import BytesIO
import math
import tokenize
from attr import dataclass
from constants import TOKEN_LIMIT

from languages import Languages


@dataclass
class Directory:
    name: str
    root_path: str
    translation_paths: list[str] = field(default_factory=list[str])
    main_translation_path: str = ""

@dataclass
class SRTPart:
    index: int
    start_time: str
    end_time: str
    content: str
    source: str = ""

    @property
    def number_of_tokens(self):
        # Convert the text to bytes
        text_bytes = self.content.encode("utf-8")

        # Create a BytesIO object to simulate a file-like object
        text_io = BytesIO(text_bytes)

        # Tokenize the text using the tokenize module
        tokens = list(tokenize.tokenize(text_io.readline))

        # Get the number of tokens
        return len(tokens)
    
    @property
    def srt_format(self):
        return f"{self.index}\n{self.start_time} --> {self.end_time}\n{self.content}\n\n"


@dataclass
class FileChunk:
    index: int
    content: str

@dataclass
class File:
    name: str
    language: Languages
    source_path: str = ""
    target_path: str = ""
    contents: str = ""
    translated_content: str = ""
    SRTParts: list[SRTPart] = field(default_factory=list[SRTPart])
    breakpoints: list[int] = field(default_factory=list[int])

    @property
    def number_of_tokens(self):
        # Convert the text to bytes
        text_bytes = self.contents.encode("utf-8")

        # Create a BytesIO object to simulate a file-like object
        text_io = BytesIO(text_bytes)

        # Tokenize the text using the tokenize module
        tokens = list(tokenize.tokenize(text_io.readline))

        # Get the number of tokens
        return len(tokens)

    @property
    def number_of_chunks(self):
        return math.ceil(self.number_of_tokens / TOKEN_LIMIT)
