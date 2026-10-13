def validate_waypoint(lat, lon, alt_m):
    """Lab 2 style (EP + BVA). lat -90..90, lon -180..180, altitude 10..120 m."""
    for v in (lat, lon, alt_m):
        if isinstance(v, bool) or not isinstance(v, (int, float)) or v != v:
            return "INVALID_TYPE"
    if not (-90 <= lat <= 90):
        return "INVALID_LAT"
    if not (-180 <= lon <= 180):
        return "INVALID_LON"
    if not (10 <= alt_m <= 120):
        return "INVALID_ALT"
    return "VALID"


def failsafe_action(battery_pct, gps_locked, link_ok):
    """Lab 4 style decision table.
    Battery: CRITICAL < 15 | LOW 15..30 | OK > 30."""
    if battery_pct < 15:                      # R1: don't care GPS, link
        return "LAND_NOW"
    if not gps_locked:
        return "LAND_NOW" if not link_ok else "HOLD_ALTITUDE_MANUAL"   # R2, R3
    if not link_ok:                           # R4
        return "RETURN_TO_HOME"
    if battery_pct <= 30:                     # R5
        return "RETURN_TO_HOME"
    return "CONTINUE"                         # R6
