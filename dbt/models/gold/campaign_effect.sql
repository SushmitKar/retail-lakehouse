with windows as (
    select
        t.household_key,
        t.campaign,
        d.start_day,
        d.end_day,
        d.end_day - d.start_day + 1 as length_days
    from {{ source('silver', 'campaign_table') }} t
    join {{ source('silver', 'campaign_desc') }} d on t.campaign = d.campaign
    where d.start_day - (d.end_day - d.start_day + 1) >= 1
)

select
    w.household_key,
    w.campaign,
    count(distinct case when f.day between w.start_day and w.end_day then f.basket_id end) as baskets_during,
    count(distinct case when f.day between w.start_day - w.length_days and w.start_day - 1 then f.basket_id end) as baskets_before
from windows w
left join {{ ref('fact_sales') }} f
    on f.household_key = w.household_key
   and f.day between w.start_day - w.length_days and w.end_day
group by w.household_key, w.campaign