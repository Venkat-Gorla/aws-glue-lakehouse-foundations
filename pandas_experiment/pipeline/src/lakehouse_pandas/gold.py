import pandas as pd


def build_orders_metrics_daily(
    silver_df: pd.DataFrame,
) -> pd.DataFrame:
    """Build daily order metrics from Silver orders."""
    df = silver_df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"])

    gold_df = (
        df.groupby("order_date", as_index=False)
        .agg(
            total_orders=("order_id", "size"),
            valid_orders=("amount", "count"),
            total_revenue=("amount", "sum"),
            avg_order_value=("amount", "mean"),
            high_value_orders=(
                "amount",
                lambda amounts: (amounts > 100).sum(),
            ),
        )
    )

    return gold_df
