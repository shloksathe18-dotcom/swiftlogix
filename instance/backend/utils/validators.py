def require_fields(data: dict, fields: list[str]):
    missing = [f for f in fields if f not in data or data.get(f) in (None, "")]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    return True, None


def validate_lat_lng(lat, lng):
    try:
        lat = float(lat)
        lng = float(lng)
        if not (-90 <= lat <= 90 and -180 <= lng <= 180):
            return False
        return True
    except Exception:
        return False
