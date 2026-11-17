
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select household_key
from "lakehouse"."main"."household_trend"
where household_key is null



  
  
      
    ) dbt_internal_test