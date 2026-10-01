import pytest
from baseline import predict, metrics
T = {'cpu_pct':92,'memory_pct':94,'storage_pct':95,'network_mbps':940,'temperature_c':82}
R = {'cpu_pct':50,'memory_pct':60,'storage_pct':70,'network_mbps':400,'temperature_c':55,'environment_temp_c':24}

def test_nan_rejected():
    with pytest.raises(ValueError):
        predict(dict(R, cpu_pct=float('nan')), T)

def test_missing_field_rejected_even_after_alert():
    row = dict(R, cpu_pct=99)
    del row['temperature_c']
    with pytest.raises(ValueError):
        predict(row, T)

def test_mismatched_labels_rejected():
    with pytest.raises(ValueError):
        metrics([1,0], [1])
