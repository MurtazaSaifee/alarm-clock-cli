import unittest
from datetime import datetime
from alarm_clock.parser import parse_target_seconds


class TestParser(unittest.TestCase):
    def test_plain_seconds(self):
        self.assertEqual(parse_target_seconds("30"), 30)
        self.assertEqual(parse_target_seconds("120"), 120)

    def test_unit_durations(self):
        self.assertEqual(parse_target_seconds("10s"), 10)
        self.assertEqual(parse_target_seconds("5m"), 300)
        self.assertEqual(parse_target_seconds("1h"), 3600)

    def test_combined_durations(self):
        self.assertEqual(parse_target_seconds("1m15s"), 75)
        self.assertEqual(parse_target_seconds("1h30m"), 5400)
        self.assertEqual(parse_target_seconds("1h2m3s"), 3723)

    def test_clock_target_future_same_day(self):
        ref_time = datetime(2026, 9, 11, 14, 0, 0)
        self.assertEqual(parse_target_seconds("14:05", now=ref_time), 300)
        self.assertEqual(parse_target_seconds("14:00:30", now=ref_time), 30)

    def test_clock_target_next_day(self):
        ref_time = datetime(2026, 9, 11, 14, 0, 0)
        # 13:00 has already passed today, so it should target 13:00 tomorrow (23 hours = 82800 seconds)
        self.assertEqual(parse_target_seconds("13:00", now=ref_time), 82800)

    def test_invalid_inputs(self):
        invalid_inputs = [
            "",
            "   ",
            "abc",
            "-10s",
            "0s",
            "0",
            "25:00",
            "12:60",
            "10x",
        ]
        for item in invalid_inputs:
            with self.subTest(item=item):
                with self.assertRaises(ValueError):
                    parse_target_seconds(item)


if __name__ == "__main__":
    unittest.main()
