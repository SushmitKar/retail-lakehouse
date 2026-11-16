
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    household_key as unique_field,
    count(*) as n_records

from "lakehouse"."main"."dim_household"
where household_key is not null
group by household_key
having count(*) > 1



  
  
      
    ) dbt_internal_test