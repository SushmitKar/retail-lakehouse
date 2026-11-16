
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with child as (
    select household_key as from_field
    from "lakehouse"."main"."fact_sales"
    where household_key is not null
),

parent as (
    select household_key as to_field
    from "lakehouse"."main"."dim_household"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



  
  
      
    ) dbt_internal_test