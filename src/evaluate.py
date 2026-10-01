"""Comparable holdout evaluation; no threshold tuning on test labels."""
import csv
import json
import time
from pathlib import Path
from baseline import predict, metrics
from isolation_forest import detect
from telemetry import validate, split_rows

def run(data_path='data/synthetic_telemetry.csv',
        config_path='config/thresholds.json', output_dir='results'):
    with open(data_path, encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        validate(row)
    training, test = split_rows(rows)
    with open(config_path, encoding='utf-8') as stream:
        thresholds = json.load(stream)
    labels = [int(row['is_anomaly']) for row in test]
    start = time.perf_counter()
    predictions = [predict(row, thresholds) for row in test]
    baseline_latency = (time.perf_counter() - start) * 1000 / len(test)
    baseline_result = metrics(labels, predictions)
    forest_predictions, forest_latency = detect(training, test)
    forest_result = metrics(labels, forest_predictions)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    for name, result, latency in (
        ('baseline', baseline_result, baseline_latency),
        ('isolation_forest', forest_result, forest_latency),
    ):
        result.update(mean_detection_latency_ms=latency,
                      test_observations=len(test),
                      training_observations=len(training))
        with open(destination / f'{name}_metrics.json', 'w', encoding='utf-8') as stream:
            json.dump(result, stream, indent=2)
    return dict(baseline=baseline_result, isolation_forest=forest_result)

if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
