import io
import unittest
from alarm_clock.engine import AlarmState
from alarm_clock.terminal import TerminalController, format_seconds


class TestTerminalController(unittest.TestCase):
    def test_format_seconds(self):
        self.assertEqual(format_seconds(0), "00:00:00")
        self.assertEqual(format_seconds(59), "00:00:59")
        self.assertEqual(format_seconds(61), "00:01:01")
        self.assertEqual(format_seconds(3665), "01:01:05")

    def test_render_states(self):
        fake_stdout = io.StringIO()
        ctrl = TerminalController(stdout=fake_stdout)

        ctrl.render(AlarmState.RUNNING, 65)
        self.assertIn("[RUNNING] Remaining: 00:01:05", fake_stdout.getvalue())

        fake_stdout.seek(0)
        fake_stdout.truncate(0)
        ctrl.render(AlarmState.PAUSED, 65)
        self.assertIn("[PAUSED]  Remaining: 00:01:05", fake_stdout.getvalue())

        fake_stdout.seek(0)
        fake_stdout.truncate(0)
        ctrl.render(AlarmState.RINGING, 0)
        self.assertIn("ALARM RINGING!", fake_stdout.getvalue())
        self.assertIn("\a", fake_stdout.getvalue())

        fake_stdout.seek(0)
        fake_stdout.truncate(0)
        ctrl.render(AlarmState.STOPPED, 0)
        self.assertIn("[STOPPED] Alarm finished.", fake_stdout.getvalue())

    def test_context_manager_safety(self):
        # Verify that entering and exiting without real TTY does not crash
        with TerminalController(stdin=io.StringIO(), stdout=io.StringIO()) as ctrl:
            self.assertIsNotNone(ctrl)


if __name__ == "__main__":
    unittest.main()
