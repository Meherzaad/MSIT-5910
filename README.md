# AI-Assisted Data Center Infrastructure Monitoring and Predictive Maintenance System

MSIT 5910 capstone prototype for technician-centered anomaly detection and decision support.

## Scope
The prototype processes selected infrastructure telemetry, compares a rule-based anomaly baseline with Isolation Forest, and produces technician-facing anomaly evidence. It does not autonomously control hardware.

## Repository structure
- `src/` prototype code
- `tests/` automated tests
- `data/` synthetic telemetry
- `docs/` requirements and documentation
- `design/` architecture
- `config/` thresholds/configuration
- `results/` evaluation outputs

## Branching
`main` is the stable branch. `development` is the integration branch.

## Reproduce the Unit 5 milestone
Use Python 3.12 and an isolated environment. From the repository root:

```sh
python -m pip install -r requirements.txt
python src/generate_data.py
python src/evaluate.py
python -m pytest -q --cov=src --cov-branch --cov-report=term-missing --cov-report=json:results/unit5/coverage.json
```

The fixed seed is 5910. Both detectors now score the same final 2,400 observations;
Isolation Forest is fitted on the first 9,600. The baseline does not learn from
training data. Timings are batch averages, not end-to-end operational latency.
No production telemetry, credentials, or participant information are included.
The synthetic CSV is regenerated rather than stored. This milestone does not
implement a dashboard, authentication, encrypted storage, or failure forecasting.

## Unit 5 validation
43 tests pass; statement coverage is 118/123 (95.93%) and branch coverage is
33/36 (91.67%). Remaining uncovered paths are command-line entry points.
The combined coverage score printed by pytest-cov is 95%.
`results/unit5/before_fixes.txt` records three failing regression tests before
validation and metric alignment fixes. `results/unit5/tests.txt` records the
passing run. `results/unit5/evaluation.txt` records the full detector comparison.

## Milestone policy
Feature branches feed `development`; reviewed integration reaches `main`.
Milestone tags and matching prereleases distinguish a verified prototype from
an operational release. See `docs/unit5_release_notes.md` for prepared milestones.

## Unit 6 integrated reproduction

The `feature/unit6-integration-recovery` review branch restores an authenticated
Flask dashboard, JSON API, cached detectors, SQLite observations, and atomic
acknowledgement audit. It does not change the Unit 5 detector algorithms.
Archived report screenshots cite an earlier local snapshot `7e517a6`; this
restoration is a new implementation snapshot, not a claim to have retrieved
that missing commit. See `docs/unit6_recovery_notes.md` for current results.

From the repository root, install requirements, generate data, and evaluate
before starting the application. Supply `APP_SECRET_KEY` and
`DEMO_PASSWORD_HASH` privately; `.env.example` contains names only.

```sh
python -m pip install -r requirements.txt
python src/generate_data.py
python src/evaluate.py
python -m pytest -q --cov=src --cov-branch --cov-report=json:results/unit6/coverage.json
python -m compileall -q src
python results/unit6/acceptance.py
python -m gunicorn --chdir src --bind 127.0.0.1:8000 --workers 1 'app:create_app()'
```

`python results/unit6/revalidate_http.py` runs an independent loopback server,
creates temporary random credentials, measures three serial request batches,
and records outputs without publishing credentials. The generated database is
excluded from Git. Do not run the restoration as an internet-facing service:
identity federation, login throttling, HTTPS termination, and recovery checks
remain staging prerequisites. Container execution and participant testing have
not been performed.
