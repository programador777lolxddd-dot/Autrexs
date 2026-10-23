"""Small, dependency-free time helpers."""

from datetime import datetime
from time import monotonic


def get_current_time(*, seconds: bool = True, twelve_hour: bool = False) -> str:
    """Return the local system time formatted for display."""
    pattern = "%I:%M:%S %p" if twelve_hour and seconds else (
        "%I:%M %p" if twelve_hour else ("%H:%M:%S" if seconds else "%H:%M")
    )
    return datetime.now().strftime(pattern)


def format_duration(seconds: float, *, centiseconds: bool = True) -> str:
    """Format a non-negative duration as MM:SS.cc or HH:MM:SS.cc."""
    if seconds < 0:
        raise ValueError("seconds must be non-negative")
    total_centiseconds = int(seconds * 100) if centiseconds else int(seconds) * 100
    whole_seconds, fraction = divmod(total_centiseconds, 100)
    secs = whole_seconds % 60
    minutes_total = whole_seconds // 60
    mins = minutes_total % 60
    hours = minutes_total // 60
    suffix = f".{fraction:02d}" if centiseconds else ""
    if hours:
        return f"{hours:02d}:{mins:02d}:{secs:02d}{suffix}"
    return f"{minutes_total:02d}:{secs:02d}{suffix}"


def monotonic_seconds() -> float:
    """Return a monotonic timestamp suitable for measuring elapsed time."""
    return monotonic()
