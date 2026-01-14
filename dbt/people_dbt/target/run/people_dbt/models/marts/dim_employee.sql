
  create view "people"."curated_curated"."dim_employee__dbt_tmp"
    
    
  as (
    select distinct
  employee_id
from "people"."curated_staging"."stg_attendance"
  );