# Zakir Hussaini | IT Capstone Portfolio

<img src="profile.jpg" alt="Portrait of Zakir Hussaini" width="220">

**Data center operations • Applied machine learning • Reliable software**

[LinkedIn](https://www.linkedin.com/in/zakirhussaini/) · [Project repository](https://github.com/Meherzaad/MSIT-5910)

## Project at a glance
**AI-Assisted Data Center Infrastructure Monitoring and Predictive Maintenance System**

MSIT 5910, University of the People. A technician-centered research prototype comparing rule-based anomaly detection with Isolation Forest on synthetic infrastructure telemetry. The broader project title describes the research direction; this milestone detects anomalies and does not forecast failures or control hardware.

**Research question:** How do a rule-based baseline and Isolation Forest compare in detecting labeled anomalies in synthetic infrastructure telemetry, and what are the implications for technician decision support?

## Evidence directory
| Deliverable | What it demonstrates |
|---|---|
| [Prototype source](../src) | Telemetry validation, data generation, baseline and Isolation Forest detection, evaluation |
| [Requirements](../docs/requirements.md) | Functional requirements, quality attributes, human decision authority |
| [Architecture](../design/architecture.md) | Separation of ingestion, detection, and evaluation |
| [Automated tests](../tests) | Module validation and regression testing |
| [Recorded test run](../results/unit5/tests.txt) | Repository record of 43 passing tests |
| [Coverage evidence](../results/unit5/coverage_summary.json) | Recorded statement and branch coverage |
| [Detector comparison](../results/unit5/evaluation.txt) | Evaluation on the same 2,400 held-out observations |
| [Release notes](../docs/unit5_release_notes.md) | Milestone scope and version-control practices |
| [Reproduction instructions](../README.md#reproduce-the-unit-5-milestone) | Environment setup, evaluation, and test commands |

## Technical approach
Python prototype; a fixed seed of 5910 supports repeatable synthetic data generation. Isolation Forest trains on the first 9,600 observations; both detectors score the final 2,400. Recorded F1 scores are 0.94823 for the baseline and 0.58953 for Isolation Forest. The synthetic anomaly design favors threshold detection; these results do not establish general superiority. Batch-average timings must not be interpreted as operational latency. Recorded test results are historical milestone evidence, not a new test run performed for this portfolio.

## Learning demonstrated
| Outcome | Evidence and scope |
|---|---|
| CLO 1 / PLO 1 | Defined operational problem and comparative research question; literature synthesis belongs in the final report |
| CLO 2 / PLO 2 | Requirements, architecture, implemented detectors, and evaluation |
| CLO 3 / PLO 4 | Synthetic data, documented boundaries, human decision authority |
| CLO 4 / PLO 2 | Source, regression tests, configuration, and version history; CI/CD and staging validation remain future work |
| PLO 3 | Technician-readable anomaly evidence is a requirement; technician acceptance testing remains pending |
| CLO 5 / PLO 5 | This portfolio, technical documentation, and linked evidence; final paper and narrated video will be added when verified |

## Responsible interpretation
No production telemetry, participant information, or credentials are included. Synthetic performance does not establish production generalizability. This milestone does not implement a dashboard, authentication, encrypted storage, or failure forecasting. No employer endorsement is implied.

## Next deliverables
Publish the final research report, a captioned narrated demonstration, and stakeholder validation evidence after completion and privacy review. Add dataset and model documentation covering intended uses, limitations, and evaluation assumptions.

## Reproduce and review
Start with the project README, inspect the requirements and architecture, then review source, tests, and recorded results. Each artifact is linked above so reviewers can distinguish implementation evidence from future plans.

## Selected foundations
- [MSIT program learning outcomes](https://catalog.uopeople.edu/graduate-catalog-t1/graduate-program-of-study/master-of-science-in-information-technology-msit)
- [Design science in software engineering (2020)](https://doi.org/10.1007/s10664-020-09818-7)
- [Model cards (2019)](https://arxiv.org/abs/1810.03993)
- [Datasheets for datasets (2021)](https://arxiv.org/abs/1803.09010)
- [Employer expectations of ePortfolios (2021)](https://files.eric.ed.gov/fulltext/EJ1294417.pdf)
