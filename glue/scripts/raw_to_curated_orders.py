from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import col

sc = SparkContext()
glue_context = GlueContext(sc)

# Read from Glue Data Catalog (Bronze)
dyf = glue_context.create_dynamic_frame.from_catalog(
    database="lakehouse_raw",
    table_name="orders"
)

df = dyf.toDF()

# Silver schema enforcement:
# - amount is cast to decimal for correct analytics semantics
df_silver = df.withColumn(
    "amount",
    col("amount").cast("decimal(10,2)")
)

# Write to S3 as Parquet (Silver)
df_silver.write \
    .mode("overwrite") \
    .parquet("s3://aws-glue-lakehouse-vegorla/curated/orders/")
