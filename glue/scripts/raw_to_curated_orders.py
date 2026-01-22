from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import (
    col,
    to_timestamp,
    to_date,
    year,
    month,
    dayofmonth
)

sc = SparkContext()
glue_context = GlueContext(sc)

# Read Bronze orders
dyf = glue_context.create_dynamic_frame.from_catalog(
    database="lakehouse_raw",
    table_name="orders"
)

df = dyf.toDF()

# Parse created_at timestamp
df = df.withColumn(
    "created_at_ts",
    to_timestamp(col("created_at"))
)

# Derive order_date (business date)
df = df.withColumn(
    "order_date",
    to_date(col("created_at_ts"))
)

# Derive partition columns
df = (
    df
    .withColumn("year", year(col("order_date")))
    .withColumn("month", month(col("order_date")))
    .withColumn("day", dayofmonth(col("order_date")))
)

# Enforce Silver schema
df_silver = (
    df
    .withColumn("amount", col("amount").cast("decimal(10,2)"))
)

# Write partitioned Parquet to Silver
df_silver.write \
    .mode("overwrite") \
    .partitionBy("year", "month", "day") \
    .parquet("s3://aws-glue-lakehouse-vegorla/curated/orders/")
