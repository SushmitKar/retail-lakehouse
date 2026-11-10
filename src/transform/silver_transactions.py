"""
Build silver from bronze: type the columns, quarantine bad rows, flag free items.

Input:  data/lake/bronze/transactions
Output: data/lake/silver/transactions      (typed, clean rows)
        data/lake/quarantine/transactions  (rejected rows, kept as raw text, plus a reason)

Runs one day at a time. Rerunning a day replaces that day only.
Run from the project root: python -m src.transform.silver_transactions [days]
"""
import sys

from pyspark.sql import functions as F
from src.ingestion.load_bronze import BRONZE, ROOT, get_spark

SILVER = (ROOT / "data" / "lake" / "silver" / "transactions").as_posix()
QUARANTINE = (ROOT / "data" / "lake" / "quarantine" / "transactions").as_posix()

LONG_COLS = ["household_key", "basket_id", "day", "product_id", "quantity", "store_id", "week_no"]
DOUBLE_COLS = ["sales_value", "retail_disc", "coupon_disc", "coupon_match_disc"]
REQUIRED = ["household_key", "basket_id", "day", "product_id", "quantity", "sales_value"]

def typed(name):
    """Return columns 'name' cast to its silver type (long or double)."""
    return F.col(name).cast("long" if name in LONG_COLS else "double")

def add_reason(df):
    """Add quarantine reason - a label for rows to reject, null rows to keep."""
    bad_type = F.lit(False)
    for c in REQUIRED:
        bad_type = bad_type | typed(c).isNull()
    qty_zero = typed("quantity") == 0
    sales_zero = typed("sales_value") == 0
    return df.withColumn(
        "quarantine_reason",
        F.when(bad_type, "invalid_key_or_type")
        .when(qty_zero & sales_zero, "zero_qty_and_sales")
        .when(qty_zero, "zero_qty_with_sales")
    )

def to_silver(df):
    """Select typed lower-case cols, build the timestamp and flag free items."""
    hhmm = F.lpad(F.col("trans_time"), 4, "0")
    clock = F.concat(hhmm.substr(1,2), F.lit(":"), hhmm.substr(3,2))
    ts = F.to_timestamp(F.concat_ws(" ", F.col("_file_date"), clock), "yyyy-MM-dd HH:mm")   ## formal pyspark ts format
    return df.select(
        *[typed(c).alias(c) for c in LONG_COLS + DOUBLE_COLS],
        F.to_date("_file_date").alias("transaction_date"),
        ts.alias("transaction_ts"),
        ((typed("sales_value") == 0) & (typed("quantity") > 0)).alias("is_zero_sale"),
        F.col("_file_date")
    )

def write_day(df, path, file_date):
    """Replace one day's partiition in the delta table at 'path'."""
    (df.write.format("delta")
     .mode("overwrite")
     .option("replaceWhere", f"_file_date = '{file_date}'")
    .partitionBy("_file_date")
     .save(path)
     )

def build_day(spark, file_date):
    """Build silver and quarantine for one day; return (bronze, silver, quarantine) counts."""
    raw = spark.read.format("delta").load(BRONZE).filter(F.col("_file_date") == file_date)
    flagged = add_reason(raw).cache()

    good = to_silver(flagged.filter(F.col("quarantine_reason").isNull()))
    bad = flagged.filter(F.col("quarantine_reason").isNotNull())

    write_day(good, SILVER, file_date)
    write_day(bad, QUARANTINE, file_date)

    counts = (flagged.count(), good.count(), bad.count())
    flagged.unpersist()
    return counts

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None

    # Initialize the Spark session
    spark =get_spark()
    spark.sparkContext.setLogLevel("ERROR")

    bronze = spark.read.format("delta").load(BRONZE)
    dates = sorted(r[0] for r in bronze.select("_file_date").distinct().collect())[:limit]

    for d in dates:
        b, s, q = build_day(spark, d)
        assert b == s + q, f"{d}: bronze {b} != silver {s} + quarantine {q}"
        assert b == s + q, f"{d}: bronze {b} != silver {s} + quarantine {q}"
        print(f"{d}: bronze {b:,} = silver {s:,} + quarantine {q:,}")
    print("All days reconciled.")

    spark.stop()