with spend as (
    select
        household_key,
        sum(sales_value) as total_spend,
        count(distinct basket_id) as baskets
    from {{ ref('fact_sales') }}
    group by household_key
)

select
    h.household_key,
    h.age_desc,
    h.income_desc,
    h.household_size_desc,
    h.kid_category_desc,
    h.homeowner_desc,
    s.total_spend,
    s.baskets,
    s.total_spend / s.baskets as spend_per_basket
from {{ ref('dim_household') }} h
join spend s on h.household_key = s.household_key
where h.has_demographics