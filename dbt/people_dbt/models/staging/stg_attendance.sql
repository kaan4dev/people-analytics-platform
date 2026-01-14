select
  run_id,
  ingested_at,
  employee_id,
  date::date as date,
  lower(status) as status,
  source_file
from raw.attendance