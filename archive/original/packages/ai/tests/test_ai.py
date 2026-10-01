"""Tests for the AI package."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from idxwitcher_ai.features import add_feature_pipeline
from idxwitcher_ai.inference import predict_returns
from idxwitcher_ai.optimizer import optimize_portfolio, estimate_moments
from idxwitcher_ai.backtest import backtest_equal_weight


@pytest.fixture
def sample_ohlcv() -> pd.DataFrame:
    rng = np.random.default_rng(7)
    n = 300
    dates = pd.date_range("2024-01-01", periods=n, freq="B")
    price = 5000.0
    rows = []
    for d in dates:
        change = rng.normal(0, 60)
        open_p = max(100, price)
        price = max(100, price + change)
        close_p = price
        high_p = max(open_p, close_p) + abs(rng.normal(0, 20))
        low_p = min(open_p, close_p) - abs(rng.normal(0, 20))
        rows.append(
            {
                "date": d,
                "open": open_p,
                "high": high_p,
                "low": low_p,
                "close": close_p,
                "volume": int(abs(rng.normal(5_000_000, 1_000_000))),
            }
        )
    return pd.DataFrame(rows)


def test_feature_pipeline(sample_ohlcv: pd.DataFrame) -> None:
    out = add_feature_pipeline(sample_ohlcv)
    for col in ["ema_20", "rsi_14", "macd", "atr_14", "bb_position"]:
        assert col in out.columns
    assert out["rsi_14"].dropna().between(0, 100).all()


def test_predict_returns(sample_ohlcv: pd.DataFrame) -> None:
    result = predict_returns(sample_ohlcv)
    assert result["ok"] is True
    assert -1.0 < result["expected_return"] < 1.0
    assert 0.0 <= result["confidence"] <= 1.0


def test_predict_insufficient_data() -> None:
    small = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=5),
            "open": [1, 2, 3, 4, 5],
            "high": [1, 2, 3, 4, 5],
            "low": [1, 2, 3, 4, 5],
            "close": [1, 2, 3, 4, 5],
            "volume": [1, 2, 3, 4, 5],
        }
    )
    result = predict_returns(small)
    assert result["ok"] is False


def test_optimizer_weights_sum(sample_ohlcv: pd.DataFrame) -> None:
    rets = sample_ohlcv["close"].pct_change().dropna()
    returns_df = pd.DataFrame(
        {
            "A": rets.values[:250],
            "B": rets.values[:250] * 0.8,
            "C": rets.values[:250] * 1.2,
        }
    )
    expected, cov = estimate_moments(returns_df)
    result = optimize_portfolio(expected, cov, risk_profile="moderate", num_samples=2000)
    weights = np.array(result["weights"])
    assert len(weights) == 3
    assert weights.sum() <= 1.001
    assert result["volatility"] >= 0


def test_backtest_runs(sample_ohlcv: pd.DataFrame) -> None:
    prices = pd.DataFrame(
        {
            "A": sample_ohlcv["close"].values,
            "B": sample_ohlcv["close"].values * 0.9,
        },
        index=pd.to_datetime(sample_ohlcv["date"]),
    )
    result = backtest_equal_weight(prices, ["A", "B"], initial_cash=1_000_000)
    assert "total_return" in result
    assert result["final_value"] > 0
    assert len(result["equity_curve"]) > 0
