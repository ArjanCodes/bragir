import pytest
from datetime import timedelta

from bragir.time import to_timedelta, to_timestamp


def test_to_timestamp_basic():
    assert to_timestamp(timedelta(hours=2, minutes=30, seconds=15)) == "02:30:15.000"


def test_to_timestamp_milliseconds():
    assert (
        to_timestamp(timedelta(hours=1, minutes=22, seconds=33, milliseconds=444))
        == "01:22:33.444"
    )


def test_to_timestamp_edge_cases():
    assert to_timestamp(timedelta(0)) == "00:00:00.000"
    assert to_timestamp(timedelta(days=2)) == "48:00:00.000"


def test_to_timedelta_basic():
    assert to_timedelta("02:30:15.000") == timedelta(hours=2, minutes=30, seconds=15)


def test_to_timedelta_no_milliseconds():
    assert to_timedelta("01:22:33") == timedelta(hours=1, minutes=22, seconds=33)


def test_to_timedelta_invalid_format():
    with pytest.raises(ValueError):
        to_timedelta("invalid_timestamp")
