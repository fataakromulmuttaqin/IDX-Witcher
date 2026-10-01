import pandas as pd

MAX_DAILY_MOVE = 0.35


def flag_suspect(df: pd.DataFrame) -> pd.Series:
    bad_price = (df[["open", "high", "low", "close"]] <= 0).any(axis=1)
    bad_range = (df["low"] > df["close"]) | (df["close"] > df["high"])
    prev = df.sort_values(["ticker", "date"]).groupby("ticker")["close"].shift()
    jump = (df["close"] / prev - 1).abs() > MAX_DAILY_MOVE
    return (bad_price | bad_range | jump.fillna(False)).astype(bool)
