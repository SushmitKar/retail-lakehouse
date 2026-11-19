"""Write and read a tiny Delta table on ADLS to prove the connection works."""
import os
from src.ingestion.load_bronze import get_spark

spark = get_spark()
acct = os.environ["AZURE_STORAGE_ACCOUNT"]
path = f"abfss://lake@{acct}.dfs.core.windows.net/bronze/_smoke"

spark.createDataFrame([(1, "milk")], ["id", "item"]).write.format("delta").mode("overwrite").save(path)
print(spark.read.format("delta").load(path).count())
spark.stop()