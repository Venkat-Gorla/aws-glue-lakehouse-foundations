"""
uv run tests_manual/07_data_quality_output.py
"""

from lakehouse_pandas.data_quality import build_orders_data_quality
from lakehouse_pandas.io import (
    load_partitioned_json,
    write_gold_data_quality,
)


SILVER_DIR = "output/silver"
GOLD_DIR = "output/gold"


def main() -> None:
    silver_df = load_partitioned_json(SILVER_DIR)
    print(f"Loaded Silver orders: {len(silver_df)} rows")

    quality_df = build_orders_data_quality(silver_df)

    write_gold_data_quality(
        quality_df,
        GOLD_DIR,
    )

    print(
        f"Wrote UC-2 Gold output: "
        f"{len(quality_df)} partitions"
    )


if __name__ == "__main__":
    main()
