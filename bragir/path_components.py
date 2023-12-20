import math
import re
from dataclasses import field, dataclass

from bragir.constants import TOKEN_LIMIT

from bragir.languages import Languages


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
    def number_of_tokens(self) -> int:
        words = re.findall(r"\w+|[^\w\s]", self.content, re.UNICODE)
        return len(words) + self.content.count(' ') 

    @property
    def srt_format(self) -> str:
        return (
            f"{self.index}\n{self.start_time} --> {self.end_time}\n{self.content}\n\n"
        )


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
    def number_of_tokens(self) -> int:
        words = re.findall(r"\w+|[^\w\s]", self.contents, re.UNICODE)
        return len(words) + self.contents.count(' ') 

    @property
    def number_of_chunks(self) -> int:
        return math.ceil(self.number_of_tokens / TOKEN_LIMIT)
