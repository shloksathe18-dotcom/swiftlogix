from math import radians, sin, cos, asin, sqrt

BASE_FARE = 30
PER_KM = 10
PER_KG = 5
COMMISSION_RATE = 0.10


def haversine_km(lat1, lon1, lat2, lon2):
    # Earth radius in km
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c


def compute_fare(distance_km: float, weight_kg: float):
    total = BASE_FARE + (distance_km * PER_KM) + (weight_kg * PER_KG)
    commission = round(total * COMMISSION_RATE, 2)
    driver_share = round(total - commission, 2)
    return round(total, 2), driver_share, commission
