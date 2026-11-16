
    

    create  table
      "lakehouse"."main"."fact_sales__dbt_tmp"
  
    
    as (
      select
    basket_id,
    product_id,
    household_key,
    day,
    store_id,
    transaction_ts,
    quantity,
    sales_value,
    retail_disc,
    coupon_disc,
    coupon_match_disc,
    is_zero_sale
from delta_scan('../data/lake/silver/transactions')
    );
    
  