import pytest
from pydub import AudioSegment

from bragir.audio.grouping import group_objects


def create_test_segment(duration_ms: int):
    # Helper function to create a test AudioSegment of a given duration
    return AudioSegment.silent(duration=duration_ms)

@pytest.fixture
def audio_segments():
    # Fixture to create a set of test audio segments
    return [create_test_segment(1000), create_test_segment(2000), create_test_segment(2500)]

def test_empty_input():
    assert group_objects([], 1000) == []

def test_empty_limit():
    assert group_objects([], 0) == []

def test_single_object(audio_segments: list[AudioSegment]):
    result = group_objects([audio_segments[0]], 2000)
    assert len(result) == 1
    assert result[0].duration_seconds == 1.0

def test_multiple_objects_within_limit(audio_segments: list[AudioSegment]):
    result = group_objects(audio_segments[:2], 4000)
    assert len(result) == 1
    assert result[0].duration_seconds == 3.0

def test_some_objects_exceeding_limit(audio_segments: list[AudioSegment]):
    result = group_objects(audio_segments, 4000)
    assert len(result) == 2

def test_objects_exceeding_limit(audio_segments: list[AudioSegment]):
    result = group_objects(audio_segments, 2500)
    assert len(result) == 3

def test_at_the_limit(audio_segments: list[AudioSegment]):
    result = group_objects(audio_segments, 6000)
    assert len(result) == 1

def test_durations(audio_segments: list[AudioSegment]):
    duration_limit = 4500
    result = group_objects(audio_segments, duration_limit)
    for group in result:
        assert group.duration_seconds <= duration_limit / 1000
