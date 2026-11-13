"""Load all other csv files into bronze Delta tables.
Input:  data/raw/<table>.csv
Output: data/lake/bronze/<table>

Unlike transactions, these arrive as one snapshot, so each load replaces the
whole table. Rerunning gives the same result.
Run from the project root: python -m src.ingestion.load_bronze_reference
"""
from src.ingestion.load_bronze import ROOT, get_spark

RAW = ROOT/"data"/"raw"
BRONZE_DIR = ROOT/"data"/"lake"/"bronze"

EXPECTED = {
    "campaign_desc" : 30,
    "campaign_table" : 7_208,
    "coupon": 124_548,
    "coupon_redempt": 2_318,
    "hh_demographic": 801,
    "product": 92_353,
    "causal_data": 36_786_524
}

def load_table(spark, name):
    """Load one raw CSV into its bronze Delta table (all text); return the row count."""
    target = (BRONZE_DIR / name).as_posix()
    df = spark.read.option("header", True).csv((RAW / f"{name}.csv").as_posix())
    df.write.format("delta").mode("overwrite").save(target)
    return spark.read.format("delta").load(target).count()


if __name__ == "__main__":
    spark = get_spark()
    spark.sparkContext.setLogLevel("ERROR")

    for name, expected in EXPECTED.items():
        n = load_table(spark, name)
        assert n == expected, f"{name}: loaded {n:,}, expected {expected:,}"
        print(f"{name}: {n:,} rows OK")

    spark.stop()