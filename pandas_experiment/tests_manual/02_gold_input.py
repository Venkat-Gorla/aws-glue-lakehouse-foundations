"""
uv run tests_manual/02_gold_input.py
"""

from lakehouse_pandas.io import load_partitioned_json


SILVER_DIR = "output/silver"


def main() -> None:
    silver_df = load_partitioned_json(SILVER_DIR)
    print(f"Loaded Silver orders: {len(silver_df)} rows")

    print("\nOrders by order_date:")
    print(
        silver_df[
            ["order_id", "amount", "order_date"]
        ]
        .sort_values(["order_date", "order_id"])
        .to_string(index=False)
    )

    print("\nRows per order_date:")
    print(
        silver_df.groupby("order_date")
        .size()
        .to_string()
    )


if __name__ == "__main__":
    main()
