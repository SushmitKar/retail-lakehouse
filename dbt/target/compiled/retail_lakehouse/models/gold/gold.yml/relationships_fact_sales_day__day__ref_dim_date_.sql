
    
    

with child as (
    select day as from_field
    from "lakehouse"."main"."fact_sales"
    where day is not null
),

parent as (
    select day as to_field
    from "lakehouse"."main"."dim_date"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


