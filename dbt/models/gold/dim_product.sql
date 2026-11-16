select
    product_id,
    manufacturer,
    department,
    brand,
    commodity_desc,
    sub_commodity_desc,
    curr_size_of_product
from {{ source('silver', 'product') }}