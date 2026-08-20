"""
uv run tests_manual/05_data_quality.py
"""

import pandas as pd

from lakehouse_pandas.io import load_partitioned_json
from lakehouse_pandas.data_quality import build_orders_data_quality


SILVER_DIR = "output/silver"


def validate_jan_12_quality(gold_df: pd.DataFrame) -> None:
    jan_12 = gold_df.loc[
        gold_df["order_date"] == pd.Timestamp("2026-01-12")
    ].iloc[0]

    assert jan_12["total_records"] == 3
    assert jan_12["null_amount_count"] == 1
    assert jan_12["invalid_amount_count"] == 0
    assert jan_12["valid_records"] == 2
    assert jan_12["percent_valid"] == (2 / 3) * 100

    print("✓ 2026-01-12 NULL amount handled correctly")


def validate_feb_1_quality(gold_df: pd.DataFrame) -> None:
    feb_1 = gold_df.loc[
        gold_df["order_date"] == pd.Timestamp("2026-02-01")
    ].iloc[0]

    assert feb_1["total_records"] == 3
    assert feb_1["null_amount_count"] == 0
    assert feb_1["invalid_amount_count"] == 1
    assert feb_1["valid_records"] == 2
    assert feb_1["percent_valid"] == (2 / 3) * 100

    print("✓ 2026-02-01 zero amount handled correctly")


def validate_feb_2_quality(gold_df: pd.DataFrame) -> None:
    feb_2 = gold_df.loc[
        gold_df["order_date"] == pd.Timestamp("2026-02-02")
    ].iloc[0]

    assert feb_2["total_records"] == 3
    assert feb_2["null_amount_count"] == 0
    assert feb_2["invalid_amount_count"] == 1
    assert feb_2["valid_records"] == 2
    assert feb_2["percent_valid"] == (2 / 3) * 100

    print("✓ 2026-02-02 negative amount handled correctly")


def validate_data_quality(gold_df: pd.DataFrame) -> None:
    required_columns = {
        "order_date",
        "total_records",
        "null_amount_count",
        "invalid_amount_count",
        "valid_records",
        "percent_valid",
    }

    assert required_columns.issubset(gold_df.columns)
    print("✓ Required UC-2 columns present")

    assert len(gold_df) == 7
    print("✓ One row per order_date")

    assert gold_df["order_date"].is_unique
    print("✓ order_date is unique")

    assert (
        gold_df["valid_records"] <= gold_df["total_records"]
    ).all()
    print("✓ Valid records never exceed total records")

    assert (
        gold_df["percent_valid"].between(0, 100)
    ).all()
    print("✓ Percent valid is between 0 and 100")

    validate_jan_12_quality(gold_df)
    validate_feb_1_quality(gold_df)
    validate_feb_2_quality(gold_df)


def main() -> None:
    silver_df = load_partitioned_json(SILVER_DIR)
    print(f"Loaded Silver orders: {len(silver_df)} rows")

    gold_df = build_orders_data_quality(silver_df)

    print("\nData quality metrics:")
    print(gold_df.to_string(index=False))

    print(f"\nGold rows: {len(gold_df)}")
    validate_data_quality(gold_df)


if __name__ == "__main__":
    main()
