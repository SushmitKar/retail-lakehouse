"""
Build silver for the 6reference tables from bronze, driven by one config.
Input:  data/lake/bronze/<table>
Output: data/lake/silver/<table>      (typed, clean rows)
        data/lake/quarantine/<table>  (rejected rows, kept as raw text, plus a reason)
Each table is a full snapshot, so each run replaces the whole table.
"""
import sys
from pyspark.sql import Window
from pyspark.sql import functions as F
from src.ingestion.load_bronze import get_spark, lake_root

LAKE = lake_root()
BRONZE_DIR = f"{LAKE}/bronze"
SILVER_DIR = f"{LAKE}/silver"
QUARANTINE_DIR = f"{LAKE}/quarantine"

# long       = columns cast to whole numbers (a failed cast sends the row to quarantine)
# key        = columns that identify one row
# dupes      = "copies": keep one row, quarantine the extras (they are identical)
#              "conflict": quarantine every row of a key whose rows differ
#              missing: no duplicate handling
# unknown    = blank text becomes "Unknown"
# blank_null = blank text becomes NULL

CONFIG = {
    "campaign_desc": {"long": ["campaign", "start_day", "end_day"],
                      "key": ["campaign"]},
    "campaign_table": {"long": ["household_key", "campaign"],
                       "key": ["household_key", "campaign"]},
    "coupon_redempt": {"long": ["household_key", "day", "coupon_upc", "campaign"],
                       "key": ["household_key", "day", "coupon_upc", "campaign"]},
    "hh_demographic": {"long": ["household_key"],
                       "key": ["household_key"]},
    "product": {"long": ["product_id", "manufacturer"],
                "key": ["product_id"],
                "unknown": ["department", "commodity_desc", "sub_commodity_desc"],
                "blank_null": ["curr_size_of_product"]},
    "coupon": {"long": ["coupon_upc", "product_id", "campaign"],
               "key": ["coupon_upc", "product_id", "campaign"],
               "dupes": "copies"},
}

def typed(name):
    """Return column 'name' cast to its silver type. Failed casts give NULL."""
    return F.col(name).cast("long")

def add_reason(df, cfg):
    """Add the reason for quarantine (quarantine_reason) for rows to reject, NULL for rows to keep."""
    bad_type = F.lit(False)
    for c in cfg["long"]:
        bad_type = bad_type | typed(c).isNull()     ## True if any long column failed to convert.
    reason = F.when(bad_type, "invalid_type")

    keys = [typed(c) for c in cfg["key"]]
    mode = cfg.get("dupes")
    if mode == "copies":
        win = Window.partitionBy(*keys).orderBy(F.monotonically_increasing_id())
        reason = reason.when(F.row_number().over(win) > 1, "duplicate_key")
    elif mode == "conflict":
        win = Window.partitionBy(*keys)
        reason = reason.when(F.count(F.lit(1)).over(win) > 1, "conflicting_key")
    return df.withColumn("quarantine_reason", reason)

def to_silver(df, cfg):
    """Cast number cols, fix blanks, drop reason column."""
    cols = []
    for c in df.columns:
        is_blank = F.col(c).isNull() | (F.trim(F.col(c)) == "")
        if c == "quarantine_reason":
            continue
        if c in cfg["long"]:
            cols.append(typed(c).alias(c))
        elif c in cfg.get("unknown", []):
            cols.append(F.when(is_blank, "Unknown").otherwise(F.col(c)).alias(c))
        elif c in cfg.get("blank_null", []):
            cols.append(F.when(is_blank, None).otherwise(F.col(c)).alias(c))
        else:
            cols.append(F.col(c))
    return df.select(*cols)

def write_table(df, path):
    """Replace the whole Delta table at 'path'."""
    (df.write.format('delta')
     .mode("overwrite")
     .option("overwriteSchema", "true")
     .save(path)
    )

def build_table(spark, name):
    """Build silver and quarantine for one table; return (bronze, silver, quarantine) counts."""
    cfg = CONFIG[name]
    raw = spark.read.format("delta").load(f"{BRONZE_DIR}/{name}")
    raw = raw.toDF(*[c.lower() for c in raw.columns])   ## lower-case all columns
    flagged = add_reason(raw, cfg)

    silver_path = f"{SILVER_DIR}/{name}"
    quarantine_path = f"{QUARANTINE_DIR}/{name}"
    write_table(to_silver(flagged.filter(F.col("quarantine_reason").isNull()), cfg), silver_path)
    write_table(flagged.filter(F.col("quarantine_reason").isNotNull()), quarantine_path)

    return (
        raw.count(),
        spark.read.format("delta").load(silver_path).count(),
        spark.read.format("delta").load(quarantine_path).count()
    )

if __name__ == "__main__":
    names = [sys.argv[1]] if len(sys.argv) > 1 else list(CONFIG)

    spark = get_spark()
    spark.sparkContext.setLogLevel("ERROR")

    for t in names:
        b, s, q = build_table(spark, t)
        assert b == s + q, f"{t}: bronze {b} != silver {s} + quarantine {q}"
        print(f"{t}: bronze {b:,} = silver {s:,} + quarantine {q:,}")
    print("All tables reconciled.")

    spark.stop()