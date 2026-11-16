
    
    

select
    day as unique_field,
    count(*) as n_records

from "lakehouse"."main"."dim_date"
where day is not null
group by day
having count(*) > 1


