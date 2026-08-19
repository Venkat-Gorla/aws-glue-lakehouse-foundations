"""
uv run tests_manual/04_data_quality_input.py
"""

from lakehouse_pandas.io import load_partitioned_json


SILVER_DIR = "output/silver"


def main() -> None:
    silver_df = load_partitioned_json(SILVER_DIR)
    print(f"Loaded Silver orders: {len(silver_df)} rows")

    print("\nRecords with null or invalid amounts:")

    quality_df = silver_df[
        silver_df["amount"].isna() | (silver_df["amount"] < 0)
    ][
        ["order_id", "amount", "order_date"]
    ].sort_values("order_date")

    print(quality_df.to_string(index=False))

    print("\nData-quality records by order_date:")
    print(
        quality_df.groupby("order_date")
        .size()
        .to_string()
    )


if __name__ == "__main__":
    main()
