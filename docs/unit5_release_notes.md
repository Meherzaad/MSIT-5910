# Unit 5 milestone release notes

## v0.1.0 Initial detector prototype
Target: c372ce6f26ae5c814ac9fc1a2422652d50699e5a
Retrospective milestone for the existing synthetic generator, rule detector,
Isolation Forest, two tests, and archived metrics. These original metrics used
different evaluation populations and should not be compared directly.

## v0.2.0 Tested core logic
Target: the merged Unit 5 validation commit on main.
Adds input validation, aligned binary scoring, reproducible local RNG, identical
holdout evaluation, 43 passing tests, and coverage evidence. Both detectors score
2,400 held-out observations. Baseline F1 is 0.94823; Isolation Forest F1 is 0.58953.
The generator's anomaly design favors the threshold baseline. This is a research
prototype prerelease, not a production release or proven failure forecaster.

Tags and GitHub prereleases must be published before this satisfies the full
version-control rubric. Preserve this distinction until publication is verified.
