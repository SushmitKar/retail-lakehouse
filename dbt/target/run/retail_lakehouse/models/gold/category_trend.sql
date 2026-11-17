
    

    create  table
      "lakehouse"."main"."category_trend__dbt_tmp"
  
    
    as (
      with spend as (
    select
        t.trend,
        p.department,
        sum( case when f.day <= 355 then f.sales_value else 0 end ) as spend_first_half,
        sum( case when f.day > 355 then f.sales_value else 0 end ) as spend_second_half
    from "lakehouse"."main"."fact_sales" f
    join "lakehouse"."main"."household_trend" t on f.household_key = t.household_key
    join "lakehouse"."main"."dim_product" p on f.product_id = p.product_id
    where t.trend in ('spending_more', 'spending_less')
    group by t.trend, p.department
)

select
    trend,
    department,
    spend_first_half,
    spend_second_half,
    spend_second_half - spend_first_half as change_amount,
    round((spend_second_half - spend_first_half) / nullif(spend_first_half, 0) * 100, 2) as change_pct,
    round((spend_first_half / sum(spend_first_half) over (partition by trend) * 100), 2) as share_first_half_pct,
    round((spend_second_half / sum(spend_second_half) over (partition by trend) * 100), 2) as share_second_half_pct,
    round(
    spend_second_half / sum(spend_second_half) over (partition by trend) * 100
    - spend_first_half / sum(spend_first_half) over (partition by trend) * 100, 2
    ) as share_change                                      -- share = a dept's spend as a % of its group's total spend in that half.
from spend
    );
    
  