"""
uv run tests_manual/06_invariant.py
"""

import pandas as pd

from lakehouse_pandas.io import load_partitioned_json
from lakehouse_pandas.gold import build_orders_metrics_daily
from lakehouse_pandas.data_quality import build_orders_data_quality
from lakehouse_pandas.validation import compare_gold_metrics


SILVER_DIR = "output/silver"


def validate_invariant(comparison_df: pd.DataFrame) -> None:
    assert len(comparison_df) == 7
    print("✓ All order dates matched between UC-1 and UC-2")

    assert comparison_df["order_date"].is_unique
    print("✓ One comparison row per order_date")

    assert (
        comparison_df["valid_records"]
        <= comparison_df["valid_orders"]
    ).all()
    print("✓ UC-2 valid records never exceed UC-1 valid orders")

    mismatches = comparison_df[
        ~comparison_df["invariant_holds"]
    ]

    assert len(mismatches) == 2
    print("✓ Exactly two intentional invariant mismatches found")

    expected_mismatches = {
        pd.Timestamp("2026-02-01"),
        pd.Timestamp("2026-02-02"),
    }

    assert set(mismatches["order_date"]) == expected_mismatches
    print("✓ Mismatches occur on expected dates")


def main() -> None:
    silver_df = load_partitioned_json(SILVER_DIR)
    print(f"Loaded Silver orders: {len(silver_df)} rows")

    metrics_df = build_orders_metrics_daily(silver_df)
    quality_df = build_orders_data_quality(silver_df)

    comparison_df = compare_gold_metrics(
        metrics_df,
        quality_df,
    )

    print("\nUC-1 vs UC-2 invariant:")
    print(comparison_df.to_string(index=False))

    print(
        f"\nInvariant mismatches: "
        f"{(~comparison_df['invariant_holds']).sum()}"
    )

    validate_invariant(comparison_df)


if __name__ == "__main__":
    main()
