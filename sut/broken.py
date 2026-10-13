"""Deliberately broken build - proves the oracle detects defects."""

def validate_waypoint(lat, lon, alt_m):
    for v in (lat, lon, alt_m):
        if isinstance(v, bool) or not isinstance(v, (int, float)) or v != v:
            return "INVALID_TYPE"
    if lat > 90:                              # BUG 1: negative latitude never checked
        return "INVALID_LAT"
    if not (-180 <= lon <= 180):
        return "INVALID_LON"
    if not (10 <= alt_m < 120):               # BUG 2: '<' instead of '<=' (120 rejected)
        return "INVALID_ALT"
    return "VALID"


def failsafe_action(battery_pct, gps_locked, link_ok):
    if battery_pct <= 15:                     # BUG 3: boundary 15 treated as CRITICAL
        return "LAND_NOW"
    if not gps_locked:
        return "LAND_NOW" if not link_ok else "CONTINUE"   # BUG 4: should be HOLD_ALTITUDE_MANUAL
    if not link_ok:
        return "RETURN_TO_HOME"
    if battery_pct <= 30:
        return "RETURN_TO_HOME"
    return "CONTINUE"
