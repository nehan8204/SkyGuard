import importlib, os
import pytest

sut = importlib.import_module(f"sut.{os.environ.get('SUT', 'correct')}")

# ---- Waypoint validator (equivalence partitioning + boundary values) ----
WAYPOINT_CASES = [
    # id,                       (lat, lon, alt_m),         expected
    ("W1-typical-valid",        (33.6844, 73.0479, 50),    "VALID"),
    ("W2-lat-below-min",        (-90.5, 73.0, 50),         "INVALID_LAT"),
    ("W3-alt-upper-bound-120",  (33.0, 73.0, 120),         "VALID"),
    ("W4-alt-just-over-120.1",  (33.0, 73.0, 120.1),       "INVALID_ALT"),
]

@pytest.mark.parametrize("case_id,args,expected", WAYPOINT_CASES,
                         ids=[c[0] for c in WAYPOINT_CASES])
def test_waypoint(case_id, args, expected):
    actual = sut.validate_waypoint(*args)
    assert actual == expected, f"{case_id}: {args} -> {actual!r}, expected {expected!r}"

# ---- Failsafe decision table (reduced rules R1-R6 + battery boundaries) ----
FAILSAFE_CASES = [
    # id,                        (battery, gps, link),      expected
    ("F1-battery-critical-14.9", (14.9, True, True),        "LAND_NOW"),
    ("F2-battery-boundary-15",   (15, True, True),          "RETURN_TO_HOME"),
    ("F3-gps-lost-link-ok",      (60, False, True),         "HOLD_ALTITUDE_MANUAL"),
    ("F4-all-healthy",           (80, True, True),          "CONTINUE"),
]

@pytest.mark.parametrize("case_id,args,expected", FAILSAFE_CASES,
                         ids=[c[0] for c in FAILSAFE_CASES])
def test_failsafe(case_id, args, expected):
    actual = sut.failsafe_action(*args)
    assert actual == expected, f"{case_id}: {args} -> {actual!r}, expected {expected!r}"
