import math
import unittest

from orbit import circular_orbit


class CircularOrbitTests(unittest.TestCase):
    def test_reference_values(self):
        # Reference values rounded to six decimals, independently checked.
        for altitude, speed, period in (
            (400, 7.668558, 92.560405),
            (800, 7.451831, 100.873559),
        ):
            with self.subTest(altitude=altitude):
                actual_speed, actual_period = circular_orbit(altitude)
                self.assertAlmostEqual(actual_speed, speed, delta=0.000001)
                self.assertAlmostEqual(actual_period, period, delta=0.000001)

    def test_higher_orbit_is_slower_and_takes_longer(self):
        low_speed, low_period = circular_orbit(400)
        high_speed, high_period = circular_orbit(800)
        self.assertLess(high_speed, low_speed)
        self.assertGreater(high_period, low_period)

    def test_invalid_altitude(self):
        for altitude in (-1, math.nan, math.inf, -math.inf):
            with self.subTest(altitude=altitude):
                with self.assertRaises(ValueError):
                    circular_orbit(altitude)

    def test_zero_altitude_is_a_finite_mathematical_case(self):
        speed, period = circular_orbit(0)
        self.assertTrue(math.isfinite(speed) and speed > 0)
        self.assertTrue(math.isfinite(period) and period > 0)


if __name__ == "__main__":
    unittest.main()
