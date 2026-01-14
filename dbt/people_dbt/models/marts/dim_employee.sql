select distinct
  employee_id
from {{ ref('stg_attendance') }}