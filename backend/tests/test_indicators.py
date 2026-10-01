import pandas as pd

from worker.indicators import compute_indicators


def _prices(n=300, ticker="AAAA", start=1000.0, step=1.0):
    dates = pd.bdate_range("2025-01-01", periods=n).date
    close = [start + step * i for i in range(n)]
    return pd.DataFrame({
        "ticker": ticker,
        "date": dates,
        "high": [c * 1.01 for c in close],
        "low": [c * 0.99 for c in close],
        "close": close,
        "volume": 1_000_000.0,
        "value_traded": [c * 1_000_000 for c in close],
    })


def test_sma_and_return_match_hand_calculation():
    df = compute_indicators(_prices())
    last = df.iloc[-1]
    assert abs(last["sma20"] - df["close"].tail(20).mean()) < 1e-9
    assert abs(last["ret_1d"] - (1299 / 1298 - 1)) < 1e-9


def test_faster_stock_gets_higher_rs_rating():
    both = pd.concat([_prices(ticker="AAAA", step=1.0), _prices(ticker="BBBB", step=3.0)])
    df = compute_indicators(both)
    last = df[df["date"] == df["date"].max()].set_index("ticker")
    assert last.loc["BBBB", "rs_rating"] > last.loc["AAAA", "rs_rating"]
