# Unit 5 milestone release notes

## v0.1.0 Initial Detector Prototype
Published prerelease: https://github.com/Meherzaad/MSIT-5910/releases/tag/v0.1.0
Target: c372ce6f26ae5c814ac9fc1a2422652d50699e5a
Retrospective milestone for the existing synthetic generator, rule detector,
Isolation Forest, two tests, and archived metrics. These original metrics used
different evaluation populations and should not be compared directly.

## v0.2.0 Tested Core Logic
Published prerelease: https://github.com/Meherzaad/MSIT-5910/releases/tag/v0.2.0
Target: e7ff1285e10d92a700c5f4ea73a36e82370c92d3
Adds input validation, aligned binary scoring, reproducible local RNG, identical
holdout evaluation, 43 passing tests, and coverage evidence. Both detectors score
2,400 held-out observations. Baseline F1 is 0.94823; Isolation Forest F1 is 0.58953.
The generator's anomaly design favors the threshold baseline. This is a research
prototype prerelease, not a production release or proven failure forecaster.

Both tags and GitHub prereleases were published and visually verified on October 1,
2026. Preserve these milestone snapshots; create new versions for future changes.
This documentation update follows the tagged validation snapshot and changes no
implementation or test result.
