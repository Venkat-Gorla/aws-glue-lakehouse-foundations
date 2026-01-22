from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import col, to_date, year, month, dayofmonth

sc = SparkContext()
glue_context = GlueContext(sc)

# Read from Glue Data Catalog (Bronze)
dyf = glue_context.create_dynamic_frame.from_catalog(
    database="lakehouse_raw",
    table_name="orders"
)

df = dyf.toDF()

# Parse order_date for partitioning
df = df.withColumn(
    "order_date",
    to_date(col("order_date"))
)

# Derive partition columns
df = df \
    .withColumn("year", year(col("order_date"))) \
    .withColumn("month", month(col("order_date"))) \
    .withColumn("day", dayofmonth(col("order_date")))

# Silver schema enforcement:
# - amount is cast to decimal for correct analytics semantics
df_silver = df.withColumn(
    "amount",
    col("amount").cast("decimal(10,2)")
)

# Write to S3 as partitioned Parquet (Silver)
df_silver.write \
    .mode("overwrite") \
    .partitionBy("year", "month", "day") \
    .parquet("s3://aws-glue-lakehouse-vegorla/curated/orders/")
