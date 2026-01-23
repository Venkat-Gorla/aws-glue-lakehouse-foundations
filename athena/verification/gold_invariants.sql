SELECT
  m.order_date,
  m.valid_orders,
  q.valid_records,
  m.valid_orders = q.valid_records AS invariant_holds
FROM lakehouse_gold.orders_metrics_daily m
JOIN lakehouse_gold.orders_data_quality q
  ON m.order_date = q.order_date
ORDER BY m.order_date;
