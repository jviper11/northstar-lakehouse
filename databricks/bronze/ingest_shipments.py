from pyspark.sql import functions as F

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
    .withColumn("batch_id", F.lit("batch_001"))
)

bronze_df.write \
    .format("delta") \
    .mode("append") \
    .saveAsTable("bronze.shipments")