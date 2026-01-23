CREATE EXTERNAL TABLE IF NOT EXISTS lakehouse_gold.orders_metrics_daily (
    total_orders BIGINT,
    valid_orders BIGINT,
    total_revenue DECIMAL(18,2),
    avg_order_value DECIMAL(18,2),
    high_value_orders BIGINT
)
PARTITIONED BY (order_date DATE)
STORED AS PARQUET
LOCATION 's3://aws-glue-lakehouse-vegorla/gold/orders_metrics_daily/';
