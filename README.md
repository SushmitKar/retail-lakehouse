**About the data:**
Contains household level transactions over two years  from a group of 2,500 households who are frequent shoppers at a retailer. It contains all of each household’s purchases, 
not just those from a limited number of categories. For certain households, demographic information as well as direct marketing contact history are included.


```
CSV files: 8

campaign_desc.csv: 30 rows
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ DESCRIPTION │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ CAMPAIGN    │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ START_DAY   │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ END_DAY     │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘


campaign_table.csv: 7,208 rows
┌───────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│  column_name  │ column_type │  null   │   key   │ default │  extra  │
│    varchar    │   varchar   │ varchar │ varchar │ varchar │ varchar │
├───────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ DESCRIPTION   │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ household_key │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ CAMPAIGN      │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
└───────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘


causal_data.csv: 36,786,524 rows
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ PRODUCT_ID  │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ STORE_ID    │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ WEEK_NO     │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ display     │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ mailer      │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘


coupon.csv: 124,548 rows
┌─────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│ column_name │ column_type │  null   │   key   │ default │  extra  │
│   varchar   │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ COUPON_UPC  │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ PRODUCT_ID  │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ CAMPAIGN    │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘


coupon_redempt.csv: 2,318 rows
┌───────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│  column_name  │ column_type │  null   │   key   │ default │  extra  │
│    varchar    │   varchar   │ varchar │ varchar │ varchar │ varchar │
├───────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ household_key │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ DAY           │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ COUPON_UPC    │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ CAMPAIGN      │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
└───────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘


hh_demographic.csv: 801 rows
┌─────────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│     column_name     │ column_type │  null   │   key   │ default │  extra  │
│       varchar       │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ AGE_DESC            │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ MARITAL_STATUS_CODE │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ INCOME_DESC         │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ HOMEOWNER_DESC      │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ HH_COMP_DESC        │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ HOUSEHOLD_SIZE_DESC │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ KID_CATEGORY_DESC   │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ household_key       │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
└─────────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘


product.csv: 92,353 rows
┌──────────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│     column_name      │ column_type │  null   │   key   │ default │  extra  │
│       varchar        │   varchar   │ varchar │ varchar │ varchar │ varchar │
├──────────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ PRODUCT_ID           │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ MANUFACTURER         │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ DEPARTMENT           │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ BRAND                │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ COMMODITY_DESC       │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ SUB_COMMODITY_DESC   │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ CURR_SIZE_OF_PRODUCT │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
└──────────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘


transaction_data.csv: 2,595,732 rows
┌───────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│    column_name    │ column_type │  null   │   key   │ default │  extra  │
│      varchar      │   varchar   │ varchar │ varchar │ varchar │ varchar │
├───────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ household_key     │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ BASKET_ID         │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ DAY               │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ PRODUCT_ID        │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ QUANTITY          │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ SALES_VALUE       │ DOUBLE      │ YES     │ NULL    │ NULL    │ NULL    │
│ STORE_ID          │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ RETAIL_DISC       │ DOUBLE      │ YES     │ NULL    │ NULL    │ NULL    │
│ TRANS_TIME        │ VARCHAR     │ YES     │ NULL    │ NULL    │ NULL    │
│ WEEK_NO           │ BIGINT      │ YES     │ NULL    │ NULL    │ NULL    │
│ COUPON_DISC       │ DOUBLE      │ YES     │ NULL    │ NULL    │ NULL    │
│ COUPON_MATCH_DISC │ DOUBLE      │ YES     │ NULL    │ NULL    │ NULL    │
└───────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┘
  12 rows                                                       6 columns


Process finished with exit code 0

```







```
D:\DEProjects\retail-lakehouse\env\Scripts\python.exe D:\DEProjects\retail-lakehouse\scripts\explore_transactions.py 

-- nulls per column
┌─────────┬─────────────┬───────────┬────────────┐
│ hh_null │ basket_null │ prod_null │ sales_null │
│  int64  │    int64    │   int64   │   int64    │
├─────────┼─────────────┼───────────┼────────────┤
│       0 │           0 │         0 │          0 │
└─────────┴─────────────┴───────────┴────────────┘


-- duplicate rows
┌────────────┬───────────────┐
│ total_rows │ distinct_rows │
│   int64    │     int64     │
├────────────┼───────────────┤
│    2595732 │       2595732 │
└────────────┴───────────────┘


-- is (BASKET_ID, PRODUCT_ID) unique?
┌────────────┬───────────────┐
│ total_rows │ distinct_keys │
│   int64    │     int64     │
├────────────┼───────────────┤
│    2595732 │       2595732 │
└────────────┴───────────────┘


-- DAY Range
┌────────────┬────────────┬───────────────┐
│ min("DAY") │ max("DAY") │ distinct_days │
│   int64    │   int64    │     int64     │
├────────────┼────────────┼───────────────┤
│          1 │        711 │           711 │
└────────────┴────────────┴───────────────┘


-- suspicious values
┌───────────────────┬───────────────┬────────────────┬────────────┐
│ negative_quantity │ zero_quantity │ negative_sales │ zero_sales │
│       int64       │     int64     │     int64      │   int64    │
├───────────────────┼───────────────┼────────────────┼────────────┤
│                 0 │         14466 │              0 │      18850 │
└───────────────────┴───────────────┴────────────────┴────────────┘


-- TRANS_TIME samples
┌────────────┐
│ TRANS_TIME │
│  varchar   │
├────────────┤
│ 1631       │
│ 1642       │
│ 1520       │
│ 1340       │
│ 2042       │
│ 1937       │
│ 0946       │
│ 1251       │
└────────────┘


-- zero sales but items sold
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│         4451 │
└──────────────┘


-- zero-qty vs zero-sales
┌──────────┬────────────┬────────┐
│ zero_qty │ zero_sales │ n_rows │
│ boolean  │  boolean   │ int64  │
├──────────┼────────────┼────────┤
│ false    │ true       │   4451 │
│ true     │ false      │     67 │
│ true     │ true       │  14399 │
└──────────┴────────────┴────────┘
1. no units sold but money received (free or full discount)
2. units sold but no money received (data error or adjustment error)
3. no units sold and no money received (cancelled or void scan)

Process finished with exit code 0

```