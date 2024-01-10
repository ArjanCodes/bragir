from typing import Any
from anyio import Path
from pydub import AudioSegment  # type:ignore
from pydub.silence import split_on_silence  # type:ignore
from openai import OpenAI

from bragir.timer import timing_decorator


def chunk_audio(file_path: str, format: str = "mp4") -> list[Any]:
    sound: AudioSegment = AudioSegment.from_file( # type:ignore
        file_path, format=format
    )  

    chunks: list[Any] = split_on_silence(
        sound,
        min_silence_len=1000,
        silence_thresh=-40,
        keep_silence=True
    )

    return chunks

@timing_decorator
def transcribe_audio_files(transcriber: OpenAI, audio_paths: list[str]) -> list[str]:
    return [transcribe_audio(transcriber, path) for path in audio_paths]


def transcribe_audio(client: OpenAI, audio_path: str) -> str:
    transcript = client.audio.transcriptions.create(
        model="whisper-1", file=Path(audio_path), response_format="srt"
    )
    return transcript  # type:ignore
