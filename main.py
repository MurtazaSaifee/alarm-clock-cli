import argparse
import sys
import time
from typing import Optional

from alarm_clock.engine import AlarmClockEngine, AlarmState
from alarm_clock.parser import parse_target_seconds
from alarm_clock.terminal import TerminalController


def run_alarm(seconds: float, controller: Optional[TerminalController] = None) -> None:
    """Run the non-blocking interactive alarm event loop until completion or stopped."""
    engine = AlarmClockEngine(seconds)
    ctrl = controller or TerminalController()

    with ctrl:
        engine.start()
        ctrl.render(engine.state, engine.remaining_seconds)

        while engine.state != AlarmState.STOPPED:
            # 1. Poll for interactive keypress (0.1s slice)
            key = ctrl.read_key(timeout=0.1)
            if key:
                if engine.state == AlarmState.RINGING:
                    # Any key dismisses alarm once ringing
                    engine.stop()
                elif key in (" ", "p", "P"):
                    engine.toggle_pause()
                elif key in ("s", "S", "q", "Q", "\x1b"):
                    engine.stop()

            # 2. Advance time
            engine.tick()

            # 3. Render updated display
            ctrl.render(engine.state, engine.remaining_seconds)

            # 4. Handle ringing cadence
            if engine.state == AlarmState.RINGING:
                time.sleep(0.4)


def parse_cli_args(args=None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="alarm-clock",
        description="Lightweight interactive CLI alarm clock and countdown timer.",
    )
    parser.add_argument(
        "time",
        nargs="?",
        help="Alarm duration (e.g., '30s', '5m', '1h30m', '120') or target time ('14:30', '08:00:00')",
    )
    return parser.parse_args(args)


def main(argv=None) -> int:
    """Entry point for CLI alarm application."""
    args = parse_cli_args(argv)
    time_input = args.time

    if not time_input:
        try:
            time_input = input("Enter alarm duration or target time (e.g., '10s', '5m', '14:30'): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            return 0

    try:
        total_seconds = parse_target_seconds(time_input)
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    try:
        run_alarm(total_seconds)
    except KeyboardInterrupt:
        print("\nAlarm cancelled.")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
