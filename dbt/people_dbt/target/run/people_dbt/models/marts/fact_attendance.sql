
  create view "people"."curated_curated"."fact_attendance__dbt_tmp"
    
    
  as (
    select
  employee_id,
  date,
  status,
  count(*) as records
from "people"."curated_staging"."stg_attendance"
group by 1,2,3
  );