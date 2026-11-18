import os, sys
from pathlib import Path
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from dotenv import load_dotenv

os.environ["PYSPARK_PYTHON"] = sys.executable

ROOT = Path(__file__).resolve().parents[2]

load_dotenv(ROOT/".env") # .env is at root, not inside src.

def lake_root():
    """Return the lake(container) base path: ADLS if Azure Storage Account is set, else local."""
    account = os.getenv("AZURE_STORAGE_ACCOUNT")
    if account:
        return f"abfss://lake@{account}.dfs.core.windows.net"
    return (ROOT/"data"/"lake").as_posix()

LANDING = ROOT / "data" / "landing" / "transactions"
BRONZE = f"{lake_root()}/bronze/transactions"
def get_spark():
    """Start a local Spark session with Delta enabled and optional Azure (ADLS) access."""
    builder = (
        SparkSession.builder.appName("bronze_loader")
        .master('local[2]')
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    )
    account = os.getenv("AZURE_STORAGE_ACCOUNT")    ## ADLS Credentials.
    key = os.getenv("AZURE_STORAGE_KEY")
    if account and key:
        builder = builder.config(
            f"spark.hadoop.fs.azure.account.key.{account}.dfs.core.windows.net", key
        )
    return configure_spark_with_delta_pip(
        builder, extra_packages=["org.apache.hadoop:hadoop-azure:3.3.4"]
    ).getOrCreate()

def load_day(spark, file_path, bronze_path=BRONZE):
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
        .save(bronze_path)
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