"""Teaching example: circular two-body orbit; km, seconds, and km/s."""

import math

MU_KM3_S2 = 398600.4418
EARTH_RADIUS_KM = 6378.137


def circular_orbit(altitude_km: float) -> tuple[float, float]:
    """Return speed (km/s) and period (minutes) for a finite altitude >= 0."""
    if not math.isfinite(altitude_km) or altitude_km < 0:
        raise ValueError("altitude_km must be finite and non-negative")
    radius_km = EARTH_RADIUS_KM + altitude_km
    speed_km_s = math.sqrt(MU_KM3_S2 / radius_km)
    period_min = 2 * math.pi * math.sqrt(radius_km**3 / MU_KM3_S2) / 60
    return speed_km_s, period_min


if __name__ == "__main__":
    for altitude in (400, 800):
        speed, period = circular_orbit(altitude)
        print(f"h={altitude} km | v={speed:.6f} km/s | T={period:.6f} min")
