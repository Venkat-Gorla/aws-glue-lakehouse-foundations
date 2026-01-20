from awsglue.context import GlueContext
from pyspark.context import SparkContext

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

# Read from Glue Catalog (Bronze)
df = spark.read \
    .format("glueparquet") \
    .table("lakehouse_raw.orders")

# Write to S3 as Parquet (Silver)
df.write \
    .mode("overwrite") \
    .parquet("s3://aws-glue-lakehouse-vegorla/curated/orders/")
