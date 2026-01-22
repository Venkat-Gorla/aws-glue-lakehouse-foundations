from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import (
    col,
    count,
    sum as _sum,
    avg,
    when
)

sc = SparkContext()
glue_context = GlueContext(sc)

# Read Silver orders
dyf = glue_context.create_dynamic_frame.from_catalog(
    database="lakehouse_curated",
    table_name="orders"
)

df = dyf.toDF()

# Gold daily metrics aggregation
df_gold = (
    df
    .groupBy("order_date")
    .agg(
        count("*").alias("total_orders"),
        count(col("amount")).alias("valid_orders"),
        _sum(col("amount")).alias("total_revenue"),
        avg(col("amount")).alias("avg_order_value"),
        _sum(
            when(col("amount") > 100, 1).otherwise(0)
        ).alias("high_value_orders")
    )
)

# Write Gold dataset (partitioned, deterministic)
df_gold.write \
    .mode("overwrite") \
    .partitionBy("order_date") \
    .parquet("s3://aws-glue-lakehouse-vegorla/gold/orders_metrics_daily/")
