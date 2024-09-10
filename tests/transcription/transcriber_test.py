import pytest
from pydub import AudioSegment

from bragir.audio.grouping import group_audio_segments


def create_test_segment(duration_ms: int):
    # Helper function to create a test AudioSegment of a given duration
    return AudioSegment.silent(duration=duration_ms)


@pytest.fixture
def audio_segments():
    # Fixture to create a set of test audio segments
    return [
        create_test_segment(1000000),
        create_test_segment(2000000),
        create_test_segment(2500000),
    ]


def test_empty_input():
    assert group_audio_segments([], 1000) == []


def test_empty_limit():
    assert group_audio_segments([], 0) == []


def test_single_object(audio_segments: list[AudioSegment]):
    result = group_audio_segments([audio_segments[0]], 2000)
    audio_segment = result[0]

    assert len(result) == 1
    assert audio_segment.duration_seconds == 1000.0


def test_multiple_objects_within_limit(audio_segments: list[AudioSegment]):
    result = group_audio_segments(audio_segments[:2], 4000)

    audio_segment = result[0]

    assert len(result) == 1
    assert audio_segment.duration_seconds == 3000.0


def test_some_objects_exceeding_limit(audio_segments: list[AudioSegment]):
    result = group_audio_segments(audio_segments, 4000)
    assert len(result) == 2


def test_objects_exceeding_limit(audio_segments: list[AudioSegment]):
    result = group_audio_segments(audio_segments, 2500)
    assert len(result) == 3


def test_at_the_limit(audio_segments: list[AudioSegment]):
    result = group_audio_segments(audio_segments, 6000)
    assert len(result) == 1


def test_durations(audio_segments: list[AudioSegment]):
    duration_limit = 4500
    result = group_audio_segments(audio_segments, duration_limit)
    for group in result:
        assert group.duration_seconds <= duration_limit
