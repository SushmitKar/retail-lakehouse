
    

    create  table
      "lakehouse"."main"."dim_household__dbt_tmp"
  
    
    as (
      with households as (
    select distinct household_key
    from delta_scan('../data/lake/silver/transactions')
)

select
    h.household_key,
    coalesce(d.age_desc, 'Unknown') as age_desc,
    coalesce(d.marital_status_code, 'Unknown') as marital_status_code,
    coalesce(d.income_desc, 'Unknown') as income_desc,
    coalesce(d.homeowner_desc, 'Unknown') as homeowner_desc,
    coalesce(d.hh_comp_desc, 'Unknown') as hh_comp_desc,
    coalesce(d.household_size_desc, 'Unknown') as household_size_desc,
    coalesce(d.kid_category_desc, 'Unknown') as kid_category_desc,
    d.household_key is not null as has_demographics
from households h
left join delta_scan('../data/lake/silver/hh_demographic') d
on h.household_key = d.household_key
    );
    
  