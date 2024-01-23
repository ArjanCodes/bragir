from pydub import AudioSegment
from pydub.silence import split_on_silence  # type:ignore
from bragir.audio.grouping import group_audio_segments
from bragir.constants import DURATION_SECONDS_25MB


def chunk_audio(file_path: str, format: str = "mp4") -> list[AudioSegment]:
    sound: AudioSegment = AudioSegment.from_file(  # type:ignore
        file=file_path
    )

    chunks: list[AudioSegment] = split_on_silence(
        sound, min_silence_len=1000, silence_thresh=-40, keep_silence=True
    )  # type:ignore

    limit = DURATION_SECONDS_25MB[format] * 0.9

    return group_audio_segments(chunks, limit)
