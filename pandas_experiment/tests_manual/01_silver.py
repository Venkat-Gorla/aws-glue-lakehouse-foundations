"""
uv run tests_manual/01_silver.py
"""

import pandas as pd
from lakehouse_pandas.io import load_orders
from lakehouse_pandas.silver import transform_to_silver


DATA_PATH = "data/orders_raw.json"


def validate_silver(bronze_df: pd.DataFrame, silver_df: pd.DataFrame) -> None:
    required_columns = {
        "order_id",
        "user_id",
        "amount",
        "currency",
        "created_at",
        "created_at_ts",
        "order_date",
        "year",
        "month",
        "day",
    }

    assert len(silver_df) == len(bronze_df)
    print("✓ Row count preserved")

    assert required_columns.issubset(silver_df.columns)
    print("✓ Required Silver columns present")

    assert silver_df["created_at_ts"].notna().all()
    print("✓ All timestamps parsed")

    assert (
        silver_df["order_date"]
        == silver_df["created_at_ts"].dt.date
    ).all()
    print("✓ order_date derived correctly")

    assert (
        silver_df["year"] == silver_df["created_at_ts"].dt.year
    ).all()
    assert (
        silver_df["month"] == silver_df["created_at_ts"].dt.month
    ).all()
    assert (
        silver_df["day"] == silver_df["created_at_ts"].dt.day
    ).all()
    print("✓ year/month/day derived correctly")

    assert pd.api.types.is_numeric_dtype(silver_df["amount"])
    assert silver_df["amount"].isna().sum() == bronze_df["amount"].isna().sum()
    print("✓ Amount converted to numeric and source null preserved")


def main() -> None:
    bronze_df = load_orders(DATA_PATH)
    print(f"Loaded Bronze orders: {len(bronze_df)} rows")

    silver_df = transform_to_silver(bronze_df)

    print("\nSilver sample:")
    print(
        silver_df[
            [
                "order_id",
                "amount",
                "created_at_ts",
                "order_date",
                "year",
                "month",
                "day",
            ]
        ]
        .head()
        .to_string(index=False)
    )

    print(f"\nSilver rows: {len(silver_df)}")

    validate_silver(bronze_df, silver_df)


if __name__ == "__main__":
    main()
