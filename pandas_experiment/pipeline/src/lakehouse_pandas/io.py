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
