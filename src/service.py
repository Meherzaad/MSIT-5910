"""Reusable detector service fitted only on the development partition."""
import csv
import hashlib
import json
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from baseline import predict
from telemetry import FEATURES, RULE_FEATURES, validate, split_rows

class DetectionService:
    def __init__(self, root):
        root = Path(root)
        raw = (root / 'config/thresholds.json').read_bytes()
        self.thresholds = json.loads(raw)
        self.config_version = hashlib.sha256(raw).hexdigest()[:12]
        with (root / 'data/synthetic_telemetry.csv').open() as stream:
            rows = list(csv.DictReader(stream))
        train, test = split_rows(rows)
        prepared = [[validate(r)[k] for k in FEATURES] for r in train]
        self.scaler = StandardScaler().fit(prepared)
        self.model = IsolationForest(n_estimators=200, contamination=0.08,
                                     random_state=5910).fit(self.scaler.transform(prepared))
        self.model_version = 'iforest-200-0.08-seed5910'
        self.evaluation = {name: json.loads((root / f'results/{name}_metrics.json').read_text())
                           for name in ['baseline', 'isolation_forest']}

    def analyze(self, row):
        values = validate(row)
        baseline = predict(values, self.thresholds)
        prepared = self.scaler.transform([[values[k] for k in FEATURES]])
        experimental = int(self.model.predict(prepared)[0] == -1)
        reasons = [f'{k}: {values[k]:g} >= {self.thresholds[k]:g}'
                   for k in RULE_FEATURES if values[k] >= self.thresholds[k]]
        return dict(telemetry=values, baseline_anomaly=baseline,
                    experimental_forest_anomaly=experimental, reasons=reasons,
                    config_version=self.config_version, model_version=self.model_version,
                    status='open' if baseline else 'normal')
