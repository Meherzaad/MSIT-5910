"""Separate software gates from acceptance of the experimental detector."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
totals=json.loads((ROOT/'results/unit6/coverage.json').read_text())['totals']
baseline=json.loads((ROOT/'results/baseline_metrics.json').read_text())
assert totals['covered_lines']/totals['num_statements']>=0.90, 'Statement coverage gate failed'
assert totals['covered_branches']/totals['num_branches']>=0.90, 'Branch coverage gate failed'
assert [baseline[k] for k in ('tp','fp','fn','tn')]==[174,19,0,2207], 'Seeded regression failed'
assert baseline['recall']>=0.90 and baseline['f1']>=0.90 and baseline['false_positive_rate']<0.02
print('PASS: separate statement/branch coverage >=90%; seeded baseline counts and detection targets preserved.')
print('Experimental forest is not accepted as the primary detector; container staging remains unverified.')
