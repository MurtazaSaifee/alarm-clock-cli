import time
from enum import Enum
from typing import Optional


class AlarmState(Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    RINGING = "RINGING"
    STOPPED = "STOPPED"


class AlarmClockEngine:
    """Core state machine and monotonic clock timing engine for alarm clock."""

    def __init__(self, total_seconds: float):
        if total_seconds <= 0:
            raise ValueError("Total seconds must be greater than zero")
        self.total_seconds: float = float(total_seconds)
        self.remaining_seconds: float = float(total_seconds)
        self.state: AlarmState = AlarmState.READY
        self._last_tick: Optional[float] = None

    def start(self, monotonic_time: Optional[float] = None) -> None:
        """Start countdown from READY state."""
        if self.state == AlarmState.STOPPED:
            return
        self._last_tick = monotonic_time if monotonic_time is not None else time.monotonic()
        self.state = AlarmState.RUNNING

    def pause(self) -> None:
        """Pause countdown if running."""
        if self.state == AlarmState.RUNNING:
            self.state = AlarmState.PAUSED
            self._last_tick = None

    def resume(self, monotonic_time: Optional[float] = None) -> None:
        """Resume countdown if paused."""
        if self.state == AlarmState.PAUSED:
            self._last_tick = monotonic_time if monotonic_time is not None else time.monotonic()
            self.state = AlarmState.RUNNING

    def toggle_pause(self, monotonic_time: Optional[float] = None) -> None:
        """Toggle between RUNNING and PAUSED states."""
        if self.state == AlarmState.RUNNING:
            self.pause()
        elif self.state == AlarmState.PAUSED:
            self.resume(monotonic_time=monotonic_time)

    def tick(self, monotonic_time: Optional[float] = None) -> None:
        """Advance time based on monotonic clock delta."""
        if self.state != AlarmState.RUNNING:
            return

        now = monotonic_time if monotonic_time is not None else time.monotonic()
        if self._last_tick is not None:
            delta = now - self._last_tick
            self.remaining_seconds -= delta

        self._last_tick = now

        if self.remaining_seconds <= 0:
            self.remaining_seconds = 0.0
            self.state = AlarmState.RINGING

    def stop(self) -> None:
        """Stop and terminate the alarm."""
        self.state = AlarmState.STOPPED
        self._last_tick = None
