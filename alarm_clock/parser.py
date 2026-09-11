import re
from datetime import datetime, timedelta
from typing import Optional


def parse_target_seconds(input_str: str, now: Optional[datetime] = None) -> int:
    """Parse a duration string or target time into total seconds.

    Supported formats:
      - Raw seconds: "30", "120"
      - Durations: "10s", "5m", "1h", "1h30m", "1m15s"
      - Target time (24-hour): "HH:MM" or "HH:MM:SS" (e.g., "14:30", "08:15:30")
    """
    cleaned = input_str.strip()
    if not cleaned:
        raise ValueError("Input time/duration cannot be empty")

    # 1. Plain numeric seconds
    if cleaned.isdigit():
        val = int(cleaned)
        if val <= 0:
            raise ValueError("Duration must be greater than zero")
        return val

    # 2. Relative duration with units: h, m, s
    duration_match = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", cleaned)
    if duration_match and any(duration_match.groups()):
        h = int(duration_match.group(1) or 0)
        m = int(duration_match.group(2) or 0)
        s = int(duration_match.group(3) or 0)
        total = h * 3600 + m * 60 + s
        if total <= 0:
            raise ValueError("Duration must be greater than zero")
        return total

    # 3. Clock target time (HH:MM or HH:MM:SS)
    clock_match = re.fullmatch(r"(\d{1,2}):(\d{2})(?::(\d{2}))?", cleaned)
    if clock_match:
        h = int(clock_match.group(1))
        m = int(clock_match.group(2))
        s = int(clock_match.group(3) or 0)

        if not (0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60):
            raise ValueError(f"Invalid time format '{cleaned}': hours must be 0-23, minutes/seconds 0-59")

        ref = now if now is not None else datetime.now()
        target = ref.replace(hour=h, minute=m, second=s, microsecond=0)

        # If the target time is already in the past today, target tomorrow
        if target <= ref:
            target += timedelta(days=1)

        diff = int((target - ref).total_seconds())
        if diff <= 0:
            raise ValueError("Target time must be in the future")
        return diff

    raise ValueError(f"Invalid duration or time format: '{input_str}'. Examples: '30s', '5m', '14:30'")
