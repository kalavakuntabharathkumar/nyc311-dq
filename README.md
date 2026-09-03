# Multi-Source Data Quality Monitoring Pipeline for NYC 311 Service Requests

A production-style portfolio project for ingesting NYC 311 data, loading it into SQLite with chunking,
running 14 Great Expectations-inspired data-quality rules, quarantining invalid rows, and producing
Power BI-ready summary tables.

## Tech Stack
Python, Pandas, SQL, SQLite, Great Expectations, Power BI, Git

## Quick Start
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python run_pipeline.py
```

The default run uses a small synthetic dataset so the repository works immediately without downloading
2.1M records. To use NYC Open Data, set `NYC311_LIMIT` to a larger value.

```bash
# Example: request up to 100000 rows from Socrata
set NYC311_LIMIT=100000
python run_pipeline.py
```

## Outputs
- `data/nyc311.db` — SQLite database
- `data/quarantine.csv` — invalid records
- `reports/daily_quality_scores.csv`
- `reports/complaint_trends.csv`
- `reports/closure_time_patterns.csv`

These CSVs are directly suitable as Power BI data sources.

## Pipeline
1. Extract from Socrata API or local synthetic fallback.
2. Normalize and transform fields.
3. Load SQLite in chunks.
4. Run 14 quality rules.
5. Quarantine invalid records.
6. Generate dashboard summary tables.

## 14 Quality Rules
Required fields, numeric ID validity, duplicate keys, date parsing, created/closed ordering,
closed-date presence, resolution-time non-negativity, borough validity, latitude/longitude range,
category consistency, descriptor consistency, incident-address consistency, invalid ZIP codes,
and future-date detection.

## Note
The project is designed to be reproducible. The synthetic fallback is intentionally included so the
pipeline can be demonstrated offline; the API extractor is available for real NYC Open Data runs.
