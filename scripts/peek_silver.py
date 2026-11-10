"""Look at silver and quarantine after a run: coutns, schema, a sample, reasons."""
from src.ingestion.load_bronze import get_spark
from src.transform.silver_transactions import SILVER, QUARANTINE

spark = get_spark()
spark.sparkContext.setLogLevel("ERROR")

silver = spark.read.format("delta").load(SILVER)
quarantine = spark.read.format("delta").load(QUARANTINE)

print("Silver rows:", silver.count())
print("Quarantine rows:", quarantine.count())

# silver.printSchema()

silver.show(3, truncate=False)
quarantine.groupBy("quarantine_reason").count().show()

spark.stop()