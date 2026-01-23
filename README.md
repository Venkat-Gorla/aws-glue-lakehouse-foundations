# 🧱 AWS Glue Lakehouse Foundations

![AWS](https://img.shields.io/badge/AWS-Glue%20%7C%20Athena%20%7C%20S3-orange)
![Lakehouse](https://img.shields.io/badge/Architecture-Lakehouse-blue)
![Spark](https://img.shields.io/badge/Engine-Apache%20Spark-red)
![Data Layers](https://img.shields.io/badge/Data%20Layers-Bronze%20→%20Silver%20→%20Gold-lightgrey)
![Infra as Code](https://img.shields.io/badge/Infra-CLI%20%7C%20JSON-brightgreen)

An **end-to-end Bronze → Silver → Gold lakehouse** on AWS, built to demonstrate
data modeling discipline, analytics contracts, and cost-aware design using
**AWS Glue, S3, and Athena**.

**Designed around Spark’s scatter–gather pattern**, with heavy parallel work pushed to Silver and shuffles reserved for small, governed Gold aggregates.

The project is intentionally built without AWS Console-driven configuration to ensure reproducibility and operational parity.

## ✨ Project Highlights

- Physically partitioned Parquet for **Athena cost optimization**
- Deterministic Spark jobs with reproducible outputs
- Manual Gold table DDL (no crawlers) to enforce **analytics contracts**
- Business metrics and data quality signals at the Gold layer

## 🧰 Tech Stack

| Category         | Technology                             |
| ---------------- | -------------------------------------- |
| **Language**     | PySpark                                |
| **Storage**      | Amazon S3 (raw / curated / gold zones) |
| **Processing**   | AWS Glue Spark (Glue 4.0)              |
| **Catalog**      | AWS Glue Data Catalog                  |
| **Query Engine** | Amazon Athena                          |
| **Format**       | Parquet (columnar, compressed)         |
| **Infra**        | CLI-only, JSON job definitions         |

## 🏗️ Architecture (Lakehouse)

```
      ┌──────────────┐
      │  Raw Orders  │
      │   (JSON)     │
      │  S3 /raw     │
      └──────┬───────┘
             │  Glue Crawler (discovery)
             ▼
    ┌──────────────────┐
    │ Bronze Table     │
    │ lakehouse_raw    │
    │ orders (strings) │
    └────────┬─────────┘
             │  Glue Spark Job
             │  (schema + semantics)
             ▼
  ┌──────────────────────┐
  │ Silver Table         │
  │ lakehouse_curated    │
  │ orders (Parquet)     │
  │ partitioned by date  │
  └──────────┬───────────┘
             │  Glue Spark Job
             │  (business metrics)
             ▼
┌──────────────────────────┐
│ Gold Tables (Athena)     │
│ lakehouse_gold           │
│ - orders_metrics_daily   │
│ - orders_data_quality    │
│ (manual DDL, no crawler) │
└──────────────────────────┘
```

## 🧩 Data Model & Design

### Bronze (Raw)

- JSON source-of-truth with minimal assumptions
- Schema discovered via crawler (ingestion flexibility)

### Silver (Curated)

- Event time normalized to business date
- Strong typing (`DECIMAL`, `DATE`) and partitioned Parquet
- Deterministic, reproducible transformations

### Gold (Analytics)

- Business-owned analytics contracts
- Manual table definitions and partition governance
- No crawlers by design (control > discovery)

## 📌 Gold Invariants

The Gold layer implements **two complementary use cases**:

1. **Orders Metrics (UC-1)** – aggregates daily revenue, orders, and high-value orders. Deterministic and resilient to bad/null data.

2. **Data Quality & Governance (UC-2)** – tracks null/invalid records and pipeline health, surfacing what UC-1 ignores.

**Invariant Principle:**

> For each `order_date`, valid records in UC-2 never exceed UC-1 valid orders. Matches confirm nulls are consistently ignored; mismatches flag invalid or out-of-spec data.

**Verification:**

```sql
SELECT
  m.order_date,
  m.valid_orders,
  q.valid_records,
  m.valid_orders = q.valid_records AS invariant_holds
FROM lakehouse_gold.orders_metrics_daily m
JOIN lakehouse_gold.orders_data_quality q
  ON m.order_date = q.order_date
WHERE q.null_amount_count > 0
   OR q.invalid_amount_count > 0
ORDER BY m.order_date;
```

**Expected output:**

| order_date | valid_orders | valid_records | invariant_holds |
| ---------- | ------------ | ------------- | --------------- |
| 2026-01-12 | 2            | 2             | true            |
| 2026-02-01 | 3            | 2             | false           |
| 2026-02-02 | 3            | 2             | false           |

**Summary:**

- UC-1 remains deterministic
- UC-2 surfaces null or invalid records
- The invariant **verifies pipeline correctness and contract adherence**

## 🔁 Conceptual Lineage: MapReduce → Spark

Before this Spark-based lakehouse, I built a **serverless MapReduce pipeline** using **AWS Lambda and Step Functions** to explicitly implement fan-out, shuffling, and reduction:

👉 [https://github.com/Venkat-Gorla/mapreduce-lambda-aws](https://github.com/Venkat-Gorla/mapreduce-lambda-aws)

Both projects share the same core execution model:

- **Scatter–gather processing** with map-side partial aggregation and reduce-side final aggregation
- **Key-based grouping and deterministic reduction** over distributed data
- **Failure-tolerant, idempotent pipelines** designed for scale

The difference is **abstraction level**:
the Lambda project implements MapReduce _explicitly_, while this lakehouse expresses the same semantics _declaratively_ using Spark.
