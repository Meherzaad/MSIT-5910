import sys
sys.path.insert(0,"src")
from baseline import predict

THRESHOLDS={"cpu_pct":92,"memory_pct":94,"storage_pct":95,"network_mbps":940,"temperature_c":82}

def test_normal():
    row={"cpu_pct":50,"memory_pct":60,"storage_pct":70,"network_mbps":400,"temperature_c":55}
    assert predict(row,THRESHOLDS)==0

def test_hot():
    row={"cpu_pct":50,"memory_pct":60,"storage_pct":70,"network_mbps":400,"temperature_c":90}
    assert predict(row,THRESHOLDS)==1
