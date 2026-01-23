from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import (
    col,
    count,
    sum as _sum,
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

# Gold data quality aggregation
# vegorla: safe division by 0
df_gold = (
    df
    .groupBy("order_date")
    .agg(
        count("*").alias("total_records"),
        _sum(
            when(col("amount").isNull(), 1).otherwise(0)
        ).alias("null_amount_count"),
        _sum(
            when(col("amount") <= 0, 1).otherwise(0)
        ).alias("invalid_amount_count"),
        _sum(
            when(col("amount").isNotNull() & (
                col("amount") > 0), 1).otherwise(0)
        ).alias("valid_records"),
    )
    .withColumn(
        "percent_valid",
        (col("valid_records") / col("total_records")) * 100
    )
)

# Write Gold dataset (partitioned, deterministic)
df_gold.write \
    .mode("overwrite") \
    .partitionBy("order_date") \
    .parquet("s3://aws-glue-lakehouse-vegorla/gold/orders_data_quality/")
