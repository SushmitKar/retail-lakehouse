select distinct
    day,
    date '2024-01-01' + cast(day - 1 as integer) as date,
    week_no,
    month(date '2024-01-01' + cast(day - 1 as integer)) as month,
    year(date '2024-01-01' + cast(day - 1 as integer)) as year,
    dayname(date '2024-01-01' + cast(day - 1 as integer)) as day_of_week
from delta_scan('../data/lake/silver/transactions')