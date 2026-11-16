
    

    create  table
      "lakehouse"."main"."dim_product__dbt_tmp"
  
    
    as (
      select
    product_id,
    manufacturer,
    department,
    brand,
    commodity_desc,
    sub_commodity_desc,
    curr_size_of_product
from delta_scan('../data/lake/silver/product')
    );
    
  