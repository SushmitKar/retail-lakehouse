
    
    

with all_values as (

    select
        trend as value_field,
        count(*) as n_records

    from "lakehouse"."main"."household_trend"
    group by trend

)

select *
from all_values
where value_field not in (
    'new','lapsed','spending_more','spending_less','flat'
)


