# People Analytics Platform

Minimal people analytics data platform with ingestion, warehouse layers, data quality checks, transformations, and orchestration.

## What this repo contains
- FastAPI service for ingestion and health endpoints
- Postgres warehouse with raw and curated schemas
- Airflow DAG to orchestrate data quality checks and dbt transformations
- dbt project for staging and curated models

## API endpoints
- `GET /health` -> service health check
- `POST /ingest/attendance` -> CSV ingest (required columns: `employee_id`, `date`, `status`)

## Warehouse layout
- `raw` schema: ingestion tables (append-only)
- `curated_staging` schema: dbt staging models
- `curated` schema: dbt marts (facts and dimensions)
- `meta` schema: pipeline metadata

## dbt models
Location: `dbt/people_dbt/models`
- `staging/stg_attendance.sql`: cleaned attendance staging view
- `marts/fact_attendance.sql`: aggregated fact table
- `marts/dim_employee.sql`: distinct employee dimension

## Airflow DAG
DAG: `people_platform`
Order:
1) DQ checks (Python)
2) dbt run
3) dbt test

If DQ fails (e.g., `raw.attendance` empty), downstream tasks stop.
