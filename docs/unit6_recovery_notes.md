# Unit 6 integration recovery and independent verification

## Provenance
The prior reports contain source and output screenshots associated with local
snapshot 7e517a6. That commit is absent from retrieved remote branches. This
branch restores equivalent module contracts from those artifacts and the
verified Unit 5 core at cf9b069. It is a new source snapshot. Earlier browser
captures and the 55-test run remain archived evidence, not fresh execution.

## Current verification on October 12 2026 Phoenix time
- 59 tests passed: the 43 core cases and 16 expanded integration cases.
- Statement coverage: 278/283 = 98.23%; branch coverage: 55/58 = 94.83%.
- Combined coverage: 333/341 = 97.65%, displayed as 98%.
- Remaining gaps: CLI entry paths in evaluate, generate_data, isolation_forest.
- Compilation and the separate numerical acceptance gate passed.
- Real HTTP: normal and hot inputs returned 201; acknowledgement returned 200.
- The hot fixture breached 82 degrees at 90 degrees; forest called it typical.
- Ten warmups preceded three serial batches of 100 authenticated HTTP requests.
- Batch medians: 14.60, 14.85, 14.70 ms; p95: 20.04, 18.57, 22.80 ms.
- Throughput: 66.00, 65.40, 63.27 requests/second; 300/300 succeeded.
- Reopened database: 312 observations; one audit event for observation 2.
- Dashboard HTML and API links were checked. Browser rendering was not rerun.

The figures describe serial loopback performance, not concurrency, production
capacity, failure forecasting, or participant usability. Hardware and client
implementation differ from the archived run, so timing differences cannot be
attributed to a specific source change.

## Configuration and deployment
Use the pinned direct dependencies in requirements.txt and Python 3.12.
Generate synthetic telemetry and evaluation outputs before app startup.
Configure APP_SECRET_KEY and DEMO_PASSWORD_HASH externally; DEMO_USER defaults
to technician. DATABASE_PATH defaults to data/monitor.db locally and
/app/state/monitor.db in the container. COOKIE_SECURE=1 requires HTTPS.

The prepared container writes observations to a separate state directory,
avoiding a persistent volume that masks the synthetic model-input directory.
Proposed commands, not executed here:

```sh
docker build -t msit5910:unit6 .
docker volume create msit5910-state
docker run --rm --env-file .env -p 127.0.0.1:8000:8000 \
  --mount type=volume,src=msit5910-state,dst=/app/state msit5910:unit6
```

Before staging: verify non-root volume permissions, successful image build,
HTTPS, secret injection, health readiness, restart persistence, backup restore,
dependency review, and documented serial p95 below 100 ms. The Actions workflow
implements software checks only; it cannot authorize staging or deployment.

Feature branches enter development for review, then main after acceptance.
Keep existing v0.1.0 and v0.2.0 tags unchanged. Propose v0.3.0 as a prerelease
only after integration review and an immutable commit are approved. No new tag,
release, merge, or deployment is claimed in this recovery.
