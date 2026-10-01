import pandas as pd

from core.rules import apply_rule, load_rules


def test_every_watchlist_expression_parses():
    cols = ["close", "sma20", "sma50", "sma150", "sma200", "sma200_20d_ago", "rs_rating",
            "value_avg20", "hi_52w", "hi_20d_prev", "volume", "vol_avg20", "atr14_pct",
            "atr14_pct_20d_ago", "sector_id", "in_leading_stocks"]
    df = pd.DataFrame([[1.0] * len(cols)], columns=cols)
    df["in_leading_stocks"] = True
    for r in load_rules("watchlists"):
        apply_rule(df, r["expr"], leading_sector_ids=[1])
