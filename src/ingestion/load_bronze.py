import os, sys
from pathlib import Path
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

os.environ["PYSPARK_PYTHON"] = sys.executable

ROOT = Path(__file__).resolve().parents[2]
LANDING = ROOT / "data" / "landing" / "transactions"
BRONZE = (ROOT / "data" / "lake" / "bronze" / "transactions").as_posix()

def get_spark():
    builder = (
        SparkSession.builder.appName("bronze_loader")
        .master('local[2]')
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()

def load_day(spark, file_path):
    file_date = file_path.stem.replace("transactions_", "")     # "2024-01-01"

    df = (
        spark.read.option("header", True)
        .csv(file_path.as_posix())
        .withColumn("_file_date", F.lit(file_date))
    )
    (
        df.write.format("delta")
        .mode("overwrite")
        .option("replaceWhere", f"_file_date = '{file_date}'")
        .partitionBy("_file_date")
        .save(BRONZE)
    )
    return df.count()

if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    files = sorted(LANDING.glob("transactions_*.csv"))[:limit]

    spark = get_spark()
    spark.sparkContext.setLogLevel("ERROR")

    expected = 0
    for f in files:
        n = load_day(spark, f)
        expected += n
        print(f"{f.name}: {n:,} rows loaded")

    actual = spark.read.format("delta").load(BRONZE).count()
    print(f"\nExpected rows: {expected:,}")
    print(f"Bronze rows:   {actual:,}")
    print("MATCH" if expected == actual else "MISMATCH")
    spark.stop()