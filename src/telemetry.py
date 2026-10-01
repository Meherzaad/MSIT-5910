"""Schema validation for the declared synthetic telemetry envelope."""
import math

BOUNDS = {
    'cpu_pct': (0, 100), 'memory_pct': (0, 100),
    'storage_pct': (0, 100), 'network_mbps': (0, 1000),
    'temperature_c': (0, 100), 'environment_temp_c': (0, 45),
}
FEATURES = list(BOUNDS)
RULE_FEATURES = FEATURES[:-1]

def validate(row, features=FEATURES):
    values = {}
    for key in features:
        try:
            value = float(row[key])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f'Invalid or missing {key}') from exc
        low, high = BOUNDS[key]
        if not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f'{key} outside [{low}, {high}]')
        values[key] = value
    return values

def split_rows(rows):
    if len(rows) < 5:
        raise ValueError('At least five observations required')
    cut = int(len(rows) * 0.8)
    return rows[:cut], rows[cut:]
