# Implemented System Architecture

The local Flask application separates presentation, request handling, detection,
and persistence. Analysis runs before an observation is stored. The current
SQLite database is not encrypted by the application.

```mermaid
flowchart TB
    Browser["Browser form and review table"] -->|Same origin JSON| API["Flask API"]
    Auth["Session and CSRF checks"] --> API
    API --> Service["Detection service"]
    Service --> Validation["Telemetry validation"]
    Service --> Rules["Threshold baseline"]
    Service --> Forest["Experimental Isolation Forest"]
    Service -->|Analysis result| API
    API -->|Save before HTTP 201| Store["SQLite observations"]
    API -->|Acknowledge open alert| Audit["Status update and audit transaction"]
    Audit --> Store
    API -->|Saved identifier and reasons| Browser
    Data["Synthetic development partition"] -->|Fit once at startup| Forest
    Config["Versioned thresholds"] --> Rules
```

The scaler and forest use 9,600 development observations. Both detectors are
evaluated on the same 2,400 held-out observations. Incoming API requests do not
retrain the model. Threshold breaches determine the stored alert status; the
forest result remains an experimental comparison.

The acknowledgement transaction updates an open observation and writes its audit
entry together. It records review for investigation, not equipment repair.
Authentication uses one configured prototype account. Organizational identity,
transport encryption, login throttling, and operational recovery remain staging
requirements. The application exposes no infrastructure-control endpoints.
