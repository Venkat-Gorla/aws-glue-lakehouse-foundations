from awsglue.context import GlueContext
from pyspark.context import SparkContext

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

# Read from Glue Data Catalog
dyf = glue_context.create_dynamic_frame.from_catalog(
    database="lakehouse_raw",
    table_name="orders"
)

df = dyf.toDF()

# Write to S3 as Parquet (Silver)
df.write \
    .mode("overwrite") \
    .parquet("s3://aws-glue-lakehouse-vegorla/curated/orders/")
