import pytest

from autrexs_clock.core import format_duration, get_current_time


def test_format_duration_zero():
    assert format_duration(0) == "00:00.00"


def test_format_duration_seconds_and_centiseconds():
    assert format_duration(12.34) == "00:12.34"


def test_format_duration_minutes():
    assert format_duration(61) == "01:01.00"


def test_format_duration_hours():
    assert format_duration(3661.25) == "01:01:01.25"


def test_format_duration_rejects_negative():
    with pytest.raises(ValueError):
        format_duration(-0.1)


def test_get_current_time_has_expected_shape():
    result = get_current_time()
    assert len(result) == 8
    assert result[2] == ":" and result[5] == ":"
