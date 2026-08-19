import pandas as pd


def build_orders_data_quality(
    silver_df: pd.DataFrame,
) -> pd.DataFrame:
    """Build daily data-quality metrics from Silver orders."""
    df = silver_df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"])

    df["is_null_amount"] = df["amount"].isna()
    df["is_invalid_amount"] = df["amount"] <= 0
    df["is_valid_record"] = (
        df["amount"].notna()
        & (df["amount"] > 0)
    )

    gold_df = (
        df.groupby("order_date", as_index=False)
        .agg(
            total_records=("order_id", "size"),
            null_amount_count=("is_null_amount", "sum"),
            invalid_amount_count=("is_invalid_amount", "sum"),
            valid_records=("is_valid_record", "sum"),
        )
    )

    gold_df["percent_valid"] = (
        gold_df["valid_records"]
        .div(gold_df["total_records"])
        .mul(100)
        .where(
            gold_df["total_records"] > 0,
            0.0,
        )
    )

    return gold_df
