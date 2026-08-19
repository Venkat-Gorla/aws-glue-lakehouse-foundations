import pandas as pd


def transform_to_silver(bronze_df: pd.DataFrame) -> pd.DataFrame:
    """Transform Bronze orders into the Silver representation."""
    silver_df = bronze_df.copy()

    silver_df["created_at_ts"] = pd.to_datetime(silver_df["created_at"])
    silver_df["order_date"] = silver_df["created_at_ts"].dt.date
    silver_df["year"] = silver_df["created_at_ts"].dt.year
    silver_df["month"] = silver_df["created_at_ts"].dt.month
    silver_df["day"] = silver_df["created_at_ts"].dt.day
    silver_df["amount"] = pd.to_numeric(silver_df["amount"])

    return silver_df
