# Unit 6 integration and report verification

The submitted documents use the required Parts A–C section titles and the
template's Chapters 4–6 structure. Narrative totals, including narrative
headings, are 1,250 and 5,200 whitespace-separated words. Cover information,
references, tables, captions, code listings, and text inside screenshots are
excluded from those totals. The reports omit planning frameworks and revision
commentary.

## Evidence and evaluation

- Source baseline: integration implementation at commit 211add31d02730a4c31c9063e09d9f78723c7d81.
- Fresh verification: 59 tests pass; compilation and numerical acceptance pass.
- Statement coverage: 278/283 = 98.23%.
- Branch coverage: 55/58 = 94.83%.
- Combined coverage: 333/341 = 97.65%, rounded to 98%.
- Threshold identifier: b1244d7709bf.
- Both detectors use the same 2,400-record holdout after 9,600 development records.
- Baseline TP/FP/FN/TN: 174/19/0/2207.
- Forest TP/FP/FN/TN: 107/82/67/2144.
- All 300 measured serial HTTP requests succeed, after ten warmups.
- Reopened SQLite contains 312 observations and one acknowledgement audit event.

`results/unit6/http_revalidation.json` contains the current request measurements.
`results/unit6/coverage_summary.json` records separate coverage denominators.
`results/unit6/tests_verified.txt` and `evaluation_verified.txt` retain fresh logs.
`dependencies_verified.txt` records the resolved verification environment.

Browser images are archived demonstrations. Current API, dashboard HTML,
persistence, and numerical results were reexecuted. Browser installation failed,
so the reports do not claim a fresh browser rendering or participant evaluation.
No Docker execution, staging deployment, actual failure prediction, or
participant satisfaction score is claimed.

## Merge and staging acceptance

Software acceptance requires the complete suite to pass, separate statement and
branch coverage of at least 90%, successful Python compilation, seeded baseline
confusion counts unchanged, recall and F1 at least 0.90, and false-positive rate
below 0.02. Security and configuration changes also require review. The existing
workflow runs the software gates; those gates do not accept the forest as the
primary operational detector.

Staging additionally requires a successful image build, readiness check,
persisted restart, tested backup restoration, protected secrets, HTTPS and
secure-cookie validation, dependency review, and serial p95 below 100 ms under
the documented protocol. Container and staging gates remain pending.

Existing v0.1.0 and v0.2.0 milestones remain intact. A future v0.3.0 prerelease
should identify the reviewed integration commit and retain its test evidence,
configuration, and deployment limitations. No operational release is implied.

## Rubric traceability

| Requirement | Report evidence |
|---|---|
| Integrated modules and feature completion | Architecture, module source captures, authenticated analysis, persistence and acknowledgement |
| Code and input-output screenshots | Figures 2–5 and the fresh HTTP execution capture |
| API, database and UI communication | Browser fetch, protected handler, service calls, parameterized SQL |
| At least two quantitative metrics | Detection precision/recall/F1, HTTP latency and throughput |
| Qualitative indicator and screenshots | Structured interface clarity inspection and archived browser evidence |
| Structured table and visualization | Detector table, request table, comparison and latency charts |
| Deployment alternatives and selected method | Local environment, on-premises/cloud comparison, selected Docker staging |
| Configuration and setup | Prerequisites, environment settings, install, evaluation, tests and build commands |
| Results, discussion and conclusion | Template Chapters 4, 5 and 6 |
| Scholarly literature after 2018 | Ruff et al. 2021; Han et al. 2022; Zhao et al. 2019 |

The remaining evaluation limits are explicit: threshold-aligned synthetic labels,
uncovered executable paths, developer inspection without participants, and
unexecuted staging. These limits constrain conclusions without removing the
implemented integration and measured local results.
