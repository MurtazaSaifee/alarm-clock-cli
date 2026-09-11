import atexit
import select
import sys
from typing import Optional

try:
    import termios
    import tty
except ImportError:
    termios = None
    tty = None

from alarm_clock.engine import AlarmState


def format_seconds(seconds: float) -> str:
    """Format seconds into HH:MM:SS string."""
    total = max(0, int(seconds))
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


class TerminalController:
    """Controls terminal input (cbreak mode) and ANSI live rendering."""

    def __init__(self, stdin=None, stdout=None):
        self.stdin = stdin or sys.stdin
        self.stdout = stdout or sys.stdout
        self._orig_attrs = None
        self._is_cbreak = False

    def enter_cbreak(self) -> None:
        """Enable cbreak mode for single-keystroke inputs without pressing Enter."""
        if termios and tty and hasattr(self.stdin, "fileno"):
            try:
                if self.stdin.isatty():
                    self._orig_attrs = termios.tcgetattr(self.stdin)
                    tty.setcbreak(self.stdin.fileno())
                    self._is_cbreak = True
                    atexit.register(self.restore)
            except Exception:
                # Graceful fallback if stdin is redirected or unsupported
                pass

    def restore(self) -> None:
        """Restore original terminal mode."""
        if self._is_cbreak and self._orig_attrs and termios:
            try:
                termios.tcsetattr(self.stdin, termios.TCSADRAIN, self._orig_attrs)
            except Exception:
                pass
            finally:
                self._is_cbreak = False

    def read_key(self, timeout: float = 0.1) -> Optional[str]:
        """Poll stdin for a single character keypress within timeout seconds."""
        if not hasattr(self.stdin, "fileno"):
            return None

        try:
            rlist, _, _ = select.select([self.stdin], [], [], timeout)
            if rlist:
                return self.stdin.read(1)
        except (ValueError, OSError):
            return None
        return None

    def render(self, state: AlarmState, remaining_seconds: float) -> None:
        """Render the current alarm state and countdown in-place on the terminal."""
        formatted = format_seconds(remaining_seconds)
        if state == AlarmState.RUNNING:
            text = f"\r\033[K⏳ [RUNNING] Remaining: {formatted}  |  [Space/p] Pause  [s/q] Stop"
        elif state == AlarmState.PAUSED:
            text = f"\r\033[K⏸️  [PAUSED]  Remaining: {formatted}  |  [Space/p] Resume [s/q] Stop"
        elif state == AlarmState.RINGING:
            text = f"\r\033[K🔔 *** ALARM RINGING! *** Press [s/q/Enter] to dismiss 🔔\a"
        elif state == AlarmState.STOPPED:
            text = f"\r\033[K🛑 [STOPPED] Alarm finished.\n"
        else:
            text = f"\r\033[K[{state.value}] Remaining: {formatted}"

        self.stdout.write(text)
        self.stdout.flush()

    def __enter__(self):
        self.enter_cbreak()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore()
