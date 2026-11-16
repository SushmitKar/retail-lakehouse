
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select household_key
from "lakehouse"."main"."dim_household"
where household_key is null



  
  
      
    ) dbt_internal_test