from pydub import AudioSegment
from pydub.silence import split_on_silence # type:ignore
from bragir.audio.grouping import group_objects 

from bragir.constants import DURATION_SECONDS_25MB  # type:ignore

def chunk_audio(file_path: str, format: str = "mp4") -> list[AudioSegment]:
    sound: AudioSegment = AudioSegment.from_file(  # type:ignore
        file=file_path, format=format
    )

    chunks: list[AudioSegment] = split_on_silence(
        sound, min_silence_len=1000, silence_thresh=-40, keep_silence=True
    )  # type:ignore

    limit = DURATION_SECONDS_25MB[format]

    return group_objects(chunks, limit)