from pathlib import Path
import pandas as pd


def load_orders(path: str | Path) -> pd.DataFrame:
    """Load raw orders JSON into a Pandas DataFrame."""
    return pd.read_json(path)
