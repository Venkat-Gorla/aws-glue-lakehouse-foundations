# Spark Lakehouse — Local Pandas Experiment

## Problem

The AWS lakehouse project uses Glue Spark to transform orders from Bronze to Silver and then build Gold datasets.

While the Spark job works, understanding and visualizing the DataFrame transformations is considerably easier with a small local dataset.

## Goal

Build a repeatable local experiment that reproduces the core Bronze → Silver → Gold flow of the Spark project.

## 🧱 Architecture

```text
               Raw JSON Orders
                     │
                     ▼
              Bronze DataFrame
                     │
                     │ Schema + semantics
                     ▼
              Silver DataFrame
                     │
                     │ Partitioned JSON
                     ▼
               output/silver/
                     │
           ┌─────────┴───────────┐
           ▼                     ▼
       UC-1 Gold             UC-2 Gold
    Business Metrics        Data Quality
           │                     │
           └─────────┬───────────┘
                     ▼
                Invariant Check
                     │
                     ▼
                 Validation
```

## Success Criteria

| Check                                       | Status |
| ------------------------------------------- | ------ |
| Core Spark data flow reproduced locally     | ✅     |
| Partitioned lakehouse layout visualized     | ✅     |
| Business and data-quality metrics validated | ✅     |
| UC-1 and UC-2 consistency verified          | ✅     |
