with halves as (
    select
        household_key,
        sum(case when day<=355 then sales_value else 0 end) as spend_first_half,
        sum(case when day>355 then sales_value else 0 end) as spend_second_half
    from {{ ref('fact_sales') }}
    group by household_key
)

select
    household_key,
    spend_first_half,
    spend_second_half,
    round((spend_second_half - spend_first_half) / nullif(spend_first_half, 0), 2) as change_pct,
    case
        when spend_first_half = 0 and spend_second_half > 0 then 'new'
        when spend_first_half > 0 and spend_second_half = 0 then 'lapsed'
        when spend_second_half >= spend_first_half * 1.15 then 'spending_more'
        when spend_second_half <= spend_first_half * 0.85 then 'spending_less'
        else 'flat'
end as trend
from halves