import pandas as pd


def compare_gold_metrics(
    metrics_df: pd.DataFrame,
    quality_df: pd.DataFrame,
) -> pd.DataFrame:
    """Compare UC-1 and UC-2 daily validity metrics."""
    comparison_df = metrics_df[
        ["order_date", "valid_orders"]
    ].merge(
        quality_df[
            ["order_date", "valid_records"]
        ],
        on="order_date",
        how="inner",
    )

    comparison_df["invariant_holds"] = (
        comparison_df["valid_orders"]
        == comparison_df["valid_records"]
    )

    return comparison_df
