from pathlib import Path
import pandas as pd


def load_orders(path: str | Path) -> pd.DataFrame:
    """Load raw orders JSON Lines into a Pandas DataFrame."""
    return pd.read_json(path, lines=True)


def write_partitioned_json(
    df: pd.DataFrame,
    output_dir: str | Path,
) -> None:
    """Write a DataFrame as JSON files partitioned by year/month/day."""
    output_path = Path(output_dir)

    for (year, month, day), partition_df in df.groupby(
        ["year", "month", "day"],
        dropna=False,
    ):
        partition_path = (
            output_path
            / f"year={year}"
            / f"month={month:02d}"
            / f"day={day:02d}"
        )
        partition_path.mkdir(parents=True, exist_ok=True)

        partition_df.to_json(
            partition_path / "orders.json",
            orient="records",
            date_format="iso",
            indent=2,
        )


def load_partitioned_json(
    input_dir: str | Path,
) -> pd.DataFrame:
    """Load all JSON files from a partitioned directory."""
    files = sorted(Path(input_dir).glob("year=*/month=*/day=*/orders.json"))
    frames = [pd.read_json(file) for file in files]

    return pd.concat(frames, ignore_index=True)


def write_gold_metrics(
    df: pd.DataFrame,
    output_dir: str | Path,
) -> None:
    """Write Gold metrics partitioned by order_date."""
    output_path = Path(output_dir)

    for order_date, partition_df in df.groupby(
        "order_date",
        sort=True,
    ):
        partition_path = (
            output_path
            / f"order_date={order_date.strftime('%Y-%m-%d')}"
        )
        partition_path.mkdir(parents=True, exist_ok=True)

        partition_df.to_json(
            partition_path / "orders_metrics.json",
            orient="records",
            date_format="iso",
            indent=2,
        )
