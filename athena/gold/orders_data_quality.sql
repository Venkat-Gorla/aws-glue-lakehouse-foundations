CREATE EXTERNAL TABLE IF NOT EXISTS lakehouse_gold.orders_data_quality (
  total_records        BIGINT,
  null_amount_count    BIGINT,
  invalid_amount_count BIGINT,
  valid_records        BIGINT,
  percent_valid        DOUBLE
)
PARTITIONED BY (
  order_date DATE
)
STORED AS PARQUET
LOCATION 's3://aws-glue-lakehouse-vegorla/gold/orders_data_quality/';
