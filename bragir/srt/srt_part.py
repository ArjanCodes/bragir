import re
from dataclasses import dataclass

from bragir.token_esitmator import TOKEN_REGEX


@dataclass
class SRTPart:
    index: int
    start_time: str
    end_time: str
    content: str
    source: str = ""
    translation: str = ""

    @property
    def number_of_tokens(self) -> int:
        words = re.findall(TOKEN_REGEX, self.content, re.UNICODE)
        return len(words) + self.content.count(" ")

    @property
    def raw_srt_format(self) -> str:
        return (
            f"{self.index}\n{self.start_time} --> {self.end_time}\n{self.content}\n\n"
        )

    @property
    def translated_raw_srt_format(self) -> str:
        return f"{self.index}\n{self.start_time} --> {self.end_time}\n{self.translation}\n\n"
