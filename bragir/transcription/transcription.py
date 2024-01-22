from anyio import Path
from openai import OpenAI

from bragir.timer import timing_decorator

@timing_decorator
def transcribe_audio_files(transcriber: OpenAI, audio_paths: list[str]) -> list[str]:
    return [transcribe_audio(transcriber, path) for path in audio_paths]


def transcribe_audio(client: OpenAI, audio_path: str) -> str:
    transcript = client.audio.transcriptions.create(
        model="whisper-1", file=Path(audio_path), response_format="srt"
    )
    return transcript  # type:ignore
