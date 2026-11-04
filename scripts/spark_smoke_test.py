import os
import sys
from pathlib import Path
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

os.environ["PYSPARK_PYTHON"] = sys.executable

ROOT = Path(__file__).resolve().parents[1]
out = (ROOT / "data" / "lake" / "_smoke").as_posix()

builder = (
    SparkSession.builder.appName("smoke")
    .master("local[*]")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
)
spark = configure_spark_with_delta_pip(builder).getOrCreate()

spark.createDataFrame([(1, "milk"), (2, "bread")], ["id", "item"]).write.format("delta").mode("overwrite").save(out)

print("Rows read back:", spark.read.format("delta").load(out).count())
spark.stop()