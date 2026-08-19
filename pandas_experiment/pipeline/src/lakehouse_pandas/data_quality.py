import pandas as pd


def build_orders_data_quality(
    silver_df: pd.DataFrame,
) -> pd.DataFrame:
    """Build daily data-quality metrics from Silver orders."""
    df = silver_df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"])

    return (
        df.groupby("order_date", as_index=False)
        .agg(
            null_amount_count=(
                "amount",
                lambda amounts: amounts.isna().sum(),
            ),
            invalid_amount_count=(
                "amount",
                lambda amounts: (amounts < 0).sum(),
            ),
            valid_records=("amount", "count"),
        )
    )
