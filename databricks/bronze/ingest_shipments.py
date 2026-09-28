from pyspark.sql import functions as F
from pyspark.sql.utils import AnalysisException

BATCH_ID = "batch_001"
TARGET_TABLE = "bronze.shipments"

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(
        "/Workspace/Users/jtejada411@hotmail.com/northstar-lakehouse/data-generator/output/shipments.csv"
    )
)

bronze_df = (
    df
    .withColumn("source_file", F.col("_metadata.file_path"))
    .withColumn("ingested_at", F.current_timestamp())
    .withColumn("batch_id", F.lit(BATCH_ID))
)

try:
    existing_batch_count = (
        spark.table(TARGET_TABLE)
        .filter(F.col("batch_id") == BATCH_ID)
        .limit(1)
        .count()
    )
except AnalysisException:
    existing_batch_count = 0

if existing_batch_count > 0:
    print(f"{BATCH_ID} already exists. Skipping ingestion.")
else:
    (
        bronze_df.write
        .format("delta")
        .mode("append")
        .saveAsTable(TARGET_TABLE)
    )

    print(f"{BATCH_ID} ingested successfully.")