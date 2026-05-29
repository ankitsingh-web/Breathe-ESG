import pandas as pd

UNIT_CONVERSION = {
    'liters': ('liters', 1),
    'gallons': ('liters', 3.78541),
    'kwh': ('kwh', 1),
    'mwh': ('kwh', 1000),
}

EMISSION_FACTORS = {
    'diesel': 2.68,
    'electricity': 0.82,
    'flight': 0.25,
    'hotel': 15,
}


def normalize_unit(value, unit):
    unit = unit.lower()
    if unit not in UNIT_CONVERSION:
        return value, unit
    normalized_unit, multiplier = UNIT_CONVERSION[unit]
    return value * multiplier, normalized_unit


def calculate_emission(activity_type, normalized_value):
    factor = EMISSION_FACTORS.get(activity_type.lower(), 0)
    return factor, normalized_value * factor


def detect_anomaly(value):
    return value > 100000
