"""Transparent threshold detector and binary classification metrics."""
from telemetry import validate, RULE_FEATURES

def predict(row, thresholds):
    values = validate(row, RULE_FEATURES)
    limits = validate(thresholds, RULE_FEATURES)
    return int(any(values[key] >= limits[key] for key in RULE_FEATURES))

def metrics(y, p):
    y, p = list(y), list(p)
    if len(y) != len(p) or not y:
        raise ValueError('Nonempty labels and predictions must align')
    if any(value not in (0, 1) for value in y + p):
        raise ValueError('Binary labels and predictions required')
    tp = sum(a == 1 and b == 1 for a, b in zip(y, p))
    fp = sum(a == 0 and b == 1 for a, b in zip(y, p))
    fn = sum(a == 1 and b == 0 for a, b in zip(y, p))
    tn = sum(a == 0 and b == 0 for a, b in zip(y, p))
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    fpr = fp / (fp + tn) if fp + tn else 0
    return dict(precision=precision, recall=recall, f1=f1,
                false_positive_rate=fpr, tp=tp, fp=fp, fn=fn, tn=tn)
