import unittest
from alarm_clock.engine import AlarmClockEngine, AlarmState


class TestAlarmClockEngine(unittest.TestCase):
    def test_initial_state(self):
        engine = AlarmClockEngine(total_seconds=60)
        self.assertEqual(engine.state, AlarmState.READY)
        self.assertEqual(engine.total_seconds, 60)
        self.assertEqual(engine.remaining_seconds, 60)

    def test_start_and_ticking(self):
        engine = AlarmClockEngine(total_seconds=10)
        engine.start(monotonic_time=100.0)
        self.assertEqual(engine.state, AlarmState.RUNNING)

        engine.tick(monotonic_time=103.0)
        self.assertAlmostEqual(engine.remaining_seconds, 7.0, places=2)
        self.assertEqual(engine.state, AlarmState.RUNNING)

    def test_pause_and_resume(self):
        engine = AlarmClockEngine(total_seconds=10)
        engine.start(monotonic_time=100.0)
        engine.tick(monotonic_time=102.0)
        self.assertAlmostEqual(engine.remaining_seconds, 8.0, places=2)

        # Pause at t=102.0
        engine.pause()
        self.assertEqual(engine.state, AlarmState.PAUSED)

        # Time moves forward while paused; remaining_seconds must not decrease
        engine.tick(monotonic_time=105.0)
        self.assertAlmostEqual(engine.remaining_seconds, 8.0, places=2)

        # Resume at t=106.0
        engine.resume(monotonic_time=106.0)
        self.assertEqual(engine.state, AlarmState.RUNNING)

        # Tick 1 second after resume
        engine.tick(monotonic_time=107.0)
        self.assertAlmostEqual(engine.remaining_seconds, 7.0, places=2)

    def test_toggle_pause(self):
        engine = AlarmClockEngine(total_seconds=10)
        engine.start(monotonic_time=100.0)
        self.assertEqual(engine.state, AlarmState.RUNNING)

        engine.toggle_pause(monotonic_time=101.0)
        self.assertEqual(engine.state, AlarmState.PAUSED)

        engine.toggle_pause(monotonic_time=103.0)
        self.assertEqual(engine.state, AlarmState.RUNNING)

    def test_ringing_on_zero(self):
        engine = AlarmClockEngine(total_seconds=5)
        engine.start(monotonic_time=100.0)
        engine.tick(monotonic_time=105.5)

        self.assertEqual(engine.state, AlarmState.RINGING)
        self.assertLessEqual(engine.remaining_seconds, 0)

    def test_stop_from_any_state(self):
        for initial_action in ["running", "paused", "ringing"]:
            with self.subTest(initial_action=initial_action):
                engine = AlarmClockEngine(total_seconds=5)
                engine.start(monotonic_time=100.0)
                if initial_action == "paused":
                    engine.pause()
                elif initial_action == "ringing":
                    engine.tick(monotonic_time=106.0)

                engine.stop()
                self.assertEqual(engine.state, AlarmState.STOPPED)


if __name__ == "__main__":
    unittest.main()
