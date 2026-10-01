import pandas as pd

LIQUID_VALUE = 1e9


def compute_indicators(prices: pd.DataFrame) -> pd.DataFrame:
    df = prices.sort_values(["ticker", "date"]).reset_index(drop=True)
    g = df.groupby("ticker")

    for n, name in [(1, "ret_1d"), (21, "ret_1m"), (63, "ret_3m"),
                    (126, "ret_6m"), (189, "ret_9m"), (252, "ret_1y")]:
        df[name] = g["close"].pct_change(periods=n, fill_method=None)

    for n in (20, 50, 150, 200):
        df[f"sma{n}"] = g["close"].transform(lambda s, n=n: s.rolling(n, min_periods=n).mean())
    df["hi_52w"] = g["close"].transform(lambda s: s.rolling(252, min_periods=120).max())
    df["lo_52w"] = g["close"].transform(lambda s: s.rolling(252, min_periods=120).min())
    df["vol_avg20"] = g["volume"].transform(lambda s: s.rolling(20, min_periods=10).mean())
    df["value_avg20"] = g["value_traded"].transform(lambda s: s.rolling(20, min_periods=10).mean())

    prev_close = g["close"].shift()
    tr = pd.concat(
        [df["high"] - df["low"],
         (df["high"] - prev_close).abs(),
         (df["low"] - prev_close).abs()],
        axis=1,
    ).max(axis=1)
    df["atr14"] = tr.groupby(df["ticker"]).transform(lambda s: s.rolling(14, min_periods=14).mean())

    df["year"] = pd.to_datetime(df["date"]).dt.year
    ye = df.groupby(["ticker", "year"])["close"].last().rename("ye_close").reset_index()
    ye["year"] += 1
    df = df.merge(ye, on=["ticker", "year"], how="left")
    df["ret_ytd"] = df["close"] / df["ye_close"] - 1

    df["rs_raw"] = (0.4 * df["ret_3m"] + 0.2 * df["ret_6m"]
                    + 0.2 * df["ret_9m"] + 0.2 * df["ret_1y"])
    liquid = df["value_avg20"] >= LIQUID_VALUE
    ranked = df[liquid].groupby("date")["rs_raw"].rank(pct=True)
    df["rs_rating"] = (ranked * 99).round().clip(lower=1).reindex(df.index)
    return df.drop(columns=["year", "ye_close", "rs_raw"])


def add_rule_columns(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("ticker")
    df["sma200_20d_ago"] = g["sma200"].shift(20)
    df["hi_20d_prev"] = g["close"].transform(lambda s: s.shift(1).rolling(20, min_periods=20).max())
    df["atr14_pct"] = df["atr14"] / df["close"]
    df["atr14_pct_20d_ago"] = df.groupby("ticker")["atr14_pct"].shift(20)
    return df
