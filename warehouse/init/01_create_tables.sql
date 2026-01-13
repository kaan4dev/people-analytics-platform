CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS curated;
CREATE SCHEMA IF NOT EXISTS meta;

CREATE TABLE IF NOT EXISTS raw.attendance (
  run_id TEXT NOT NULL,
  ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
  employee_id TEXT NOT NULL,
  date DATE NOT NULL,
  status TEXT NOT NULL,
  source_file TEXT,
  PRIMARY KEY (run_id, employee_id, date)
);

CREATE TABLE IF NOT EXISTS meta.pipeline_runs (
  run_id TEXT PRIMARY KEY,
  started_at TIMESTAMP NOT NULL DEFAULT NOW(),
  finished_at TIMESTAMP,
  status TEXT NOT NULL,
  rows_loaded INT DEFAULT 0,
  dq_passed BOOLEAN DEFAULT NULL,
  notes TEXT
);
