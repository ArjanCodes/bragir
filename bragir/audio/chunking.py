from venv import logger
from pydub import AudioSegment
from pydub.silence import split_on_silence  # type:ignore

from bragir import config
from bragir.audio.grouping import group_audio_segments
from bragir.constants import DURATION_SECONDS_25MB
from bragir.types import Config


def chunk_audio(
    file_path: str,
    format: str = "mp4",
    config: Config = config,
) -> list[AudioSegment]:
    sound: AudioSegment = AudioSegment.from_file(  # type:ignore
        file=file_path
    )

    logger.info(f"Spliting {file_path} on silence")

    chunks: list[AudioSegment] = split_on_silence(
        sound,
        min_silence_len=int(config["audio"]["min_silence_len"]),
        silence_thresh=int(config["audio"]["silence_thresh"]),
        keep_silence=bool(config["audio"]["keep_silence"]),
    )  # type: ignore

    logger.info(f"Number of chunks {len(chunks)} when splitted on silence")

    limit = DURATION_SECONDS_25MB[format] * 0.9

    logger.info(f"Limit {limit} seconds for {format}")

    audio_segments = group_audio_segments(chunks, limit)

    logger.info(f"Number of audio segments {len(audio_segments)}")

    return audio_segments
