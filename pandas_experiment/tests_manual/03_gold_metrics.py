"""
uv run tests_manual/03_gold_metrics.py
"""

import pandas as pd
from lakehouse_pandas.io import load_partitioned_json
from lakehouse_pandas.gold import build_orders_metrics_daily


SILVER_DIR = "output/silver"


def validate_gold_metrics(gold_df: pd.DataFrame) -> None:
    required_columns = {
        "order_date",
        "total_orders",
        "valid_orders",
        "total_revenue",
        "avg_order_value",
        "high_value_orders",
    }

    assert required_columns.issubset(gold_df.columns)
    print("✓ Required Gold columns present")

    assert len(gold_df) == 7
    print("✓ One row per order_date")

    assert gold_df["order_date"].is_unique
    print("✓ order_date is unique")

    assert (
        gold_df["valid_orders"] <= gold_df["total_orders"]
    ).all()
    print("✓ Valid orders never exceed total orders")

    assert (
        gold_df["high_value_orders"] <= gold_df["valid_orders"]
    ).all()
    print("✓ High-value orders never exceed valid orders")

    feb_2 = gold_df.loc[
        gold_df["order_date"] == pd.Timestamp("2026-02-02")
    ].iloc[0]

    assert feb_2["total_orders"] == 3
    assert feb_2["valid_orders"] == 3
    assert feb_2["total_revenue"] == 113.99
    assert feb_2["avg_order_value"] == 113.99 / 3
    assert feb_2["high_value_orders"] == 1
    print("✓ 2026-02-02 metrics match expected values")

    jan_12 = gold_df.loc[
        gold_df["order_date"] == pd.Timestamp("2026-01-12")
    ].iloc[0]

    assert jan_12["total_orders"] == 3
    assert jan_12["valid_orders"] == 2
    assert jan_12["total_revenue"] == 52.25
    assert jan_12["avg_order_value"] == 52.25 / 2
    assert jan_12["high_value_orders"] == 0
    print("✓ 2026-01-12 null amount handled correctly")


def main() -> None:
    silver_df = load_partitioned_json(SILVER_DIR)
    print(f"Loaded Silver orders: {len(silver_df)} rows")

    gold_df = build_orders_metrics_daily(silver_df)

    print("\nGold metrics:")
    print(gold_df.to_string(index=False))

    print(f"\nGold rows: {len(gold_df)}")
    validate_gold_metrics(gold_df)


if __name__ == "__main__":
    main()
