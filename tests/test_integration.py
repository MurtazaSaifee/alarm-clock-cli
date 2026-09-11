import io
import unittest
from unittest.mock import patch, MagicMock

from alarm_clock.engine import AlarmState
from alarm_clock.terminal import TerminalController
from main import parse_cli_args, main, run_alarm


class MockTerminalController(TerminalController):
    def __init__(self, key_sequence):
        super().__init__(stdin=io.StringIO(), stdout=io.StringIO())
        self.key_sequence = list(key_sequence)
        self.rendered_states = []

    def enter_cbreak(self):
        pass

    def restore(self):
        pass

    def read_key(self, timeout=0.1):
        import time
        time.sleep(timeout)
        if self.key_sequence:
            return self.key_sequence.pop(0)
        return None

    def render(self, state, remaining_seconds):
        self.rendered_states.append(state)


class TestIntegration(unittest.TestCase):
    def test_cli_arg_parsing(self):
        args = parse_cli_args(["10s"])
        self.assertEqual(args.time, "10s")

        empty_args = parse_cli_args([])
        self.assertIsNone(empty_args.time)

    def test_main_with_valid_args(self):
        with patch("main.run_alarm") as mock_run:
            ret = main(["5s"])
            self.assertEqual(ret, 0)
            mock_run.assert_called_once_with(5)

    def test_main_with_invalid_args(self):
        stderr_buf = io.StringIO()
        with patch("sys.stderr", stderr_buf):
            ret = main(["invalid-format"])
            self.assertEqual(ret, 1)
            self.assertIn("Error: Invalid duration or time format", stderr_buf.getvalue())

    def test_run_alarm_reaches_ringing_and_dismisses(self):
        # A 0.05s alarm: ticks will quickly exceed duration and trigger ringing,
        # then first key press 's' dismisses the ringing alarm.
        mock_ctrl = MockTerminalController(key_sequence=[None, "s"])
        run_alarm(0.05, controller=mock_ctrl)

        self.assertIn(AlarmState.RUNNING, mock_ctrl.rendered_states)
        self.assertIn(AlarmState.RINGING, mock_ctrl.rendered_states)
        self.assertIn(AlarmState.STOPPED, mock_ctrl.rendered_states)

    def test_run_alarm_pause_and_stop(self):
        # Key 'p' to pause, then 's' to stop
        mock_ctrl = MockTerminalController(key_sequence=["p", "s"])
        run_alarm(10.0, controller=mock_ctrl)

        self.assertIn(AlarmState.RUNNING, mock_ctrl.rendered_states)
        self.assertIn(AlarmState.PAUSED, mock_ctrl.rendered_states)
        self.assertIn(AlarmState.STOPPED, mock_ctrl.rendered_states)


if __name__ == "__main__":
    unittest.main()
