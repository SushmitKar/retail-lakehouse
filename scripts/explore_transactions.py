import duckdb
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
src = f"read_csv_auto('{(RAW / 'transaction_data.csv').as_posix()}')"
con = duckdb.connect()

def query(title, sql):
    print(f"\n-- {title}")
    con.sql(sql).show()

query("nulls per column", f"""
SELECT
COUNT(*) FILTER (WHERE household_key IS NULL) AS hh_null,
COUNT(*) FILTER (WHERE BASKET_ID IS NULL) AS basket_null,
COUNT(*) FILTER (WHERE PRODUCT_ID IS NULL) AS prod_null,
COUNT(*) FILTER (WHERE SALES_VALUE IS NULL) AS sales_null,
FROM {src}
""")

query("duplicate rows", f"""
SELECT COUNT(*) AS total_rows,
(SELECT COUNT(*) FROM (SELECT DISTINCT * FROM {src})) AS distinct_rows
FROM {src}
""")

query("is (BASKET_ID, PRODUCT_ID) unique?", f"""
SELECT COUNT(*) AS total_rows,
COUNT(DISTINCT (BASKET_ID, PRODUCT_ID)) AS distinct_keys
FROM {src}
""")

query("DAY Range", f"""
SELECT MIN(DAY), MAX(DAY), COUNT(DISTINCT DAY) AS distinct_days
FROM {src}
""")

query("suspicious values", f"""
SELECT
COUNT(*) FILTER (WHERE QUANTITY < 0) AS negative_quantity,  -- Means returns or reversals
COUNT(*) FILTER (WHERE QUANTITY = 0) AS zero_quantity,      -- Scans with no units
COUNT(*) FILTER (WHERE SALES_VALUE < 0) AS negative_sales,  -- refunds or reversed revenue
COUNT(*) FILTER (WHERE SALES_VALUE = 0) AS zero_sales,      -- no money received, free or 100% discount
FROM {src}
""")

query("TRANS_TIME samples", f"""
SELECT DISTINCT TRANS_TIME
FROM {src} LIMIT 8
""")

query("zero sales but items sold", f"""
SELECT COUNT(*)
FROM {src} WHERE SALES_VALUE = 0 AND QUANTITY > 0
""")

query("zero-qty vs zero-sales", f"""
SELECT
(QUANTITY = 0) AS zero_qty,
(SALES_VALUE = 0) AS zero_sales,
COUNT(*) AS n_rows
FROM {src}
WHERE QUANTITY = 0 OR SALES_VALUE = 0
GROUP BY 1, 2
ORDER BY 1, 2
""")



