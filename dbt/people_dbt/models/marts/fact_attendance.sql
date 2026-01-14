select
  employee_id,
  date,
  status,
  count(*) as records
from {{ ref('stg_attendance') }}
group by 1,2,3