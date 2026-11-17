
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select trend
from "lakehouse"."main"."category_trend"
where trend is null



  
  
      
    ) dbt_internal_test