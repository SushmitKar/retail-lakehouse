
    
    

select
    household_key as unique_field,
    count(*) as n_records

from "lakehouse"."main"."household_trend"
where household_key is not null
group by household_key
having count(*) > 1


