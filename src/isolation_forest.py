"""Isolation Forest fitted only on the development partition."""
import time
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from telemetry import FEATURES, validate

def detect(training_rows, test_rows):
    if not training_rows or not test_rows:
        raise ValueError('Training and test partitions must be nonempty')
    train = [[validate(row)[key] for key in FEATURES] for row in training_rows]
    test = [[validate(row)[key] for key in FEATURES] for row in test_rows]
    scaler = StandardScaler().fit(train)
    model = IsolationForest(n_estimators=200, contamination=0.08,
                            random_state=5910)
    model.fit(scaler.transform(train))
    prepared = scaler.transform(test)
    start = time.perf_counter()
    raw = model.predict(prepared)
    latency = (time.perf_counter() - start) * 1000 / len(test)
    return [int(value == -1) for value in raw], latency

if __name__ == '__main__':
    import json
    from evaluate import run
    print(json.dumps(run()['isolation_forest'], indent=2))
