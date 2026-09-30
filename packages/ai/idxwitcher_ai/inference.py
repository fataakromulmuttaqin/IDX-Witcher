"""Lightweight inference engine for return prediction.

This module provides a deterministic, dependency-light predictor so the
API can serve /ai/predict without requiring PyTorch at runtime. It blends
momentum, mean-reversion and trend signals into a 5-day expected return.

When the real NeuralAlpha CNN-BiLSTM weights are available, swap
`predict_returns` to load them; the interface stays the same.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .features import add_feature_pipeline


def predict_returns(df: pd.DataFrame, horizon_days: int = 5) -> dict:
    """Predict expected return over `horizon_days` for one ticker.

    Expects a DataFrame with columns: date, open, high, low, close, volume.
    """
    if df is None or len(df) < 30:
        return {"ok": False, "error": "insufficient_data", "expected_return": 0.0}

    data = add_feature_pipeline(df).dropna()
    if data.empty:
        return {"ok": False, "error": "no_features", "expected_return": 0.0}

    last = data.iloc[-1]

    # Signal components (each roughly in [-1, 1])
    momentum = _clip(np.tanh(last.get("momentum_20", 0.0) * 8))
    trend = _clip(np.tanh((last.get("ema_ratio_20", 1.0) - 1.0) * 12))
    macd_signal = _clip(np.tanh(last.get("macd_hist", 0.0) / max(last.get("atr_14", 1.0), 1e-6)))
    rsi = last.get("rsi_14", 50.0)
    mean_reversion = _clip((50.0 - rsi) / 30.0)
    volume_confirm = _clip(np.tanh((last.get("volume_ratio", 1.0) - 1.0)))

    # Weighted blend
    score = (
        0.30 * momentum
        + 0.25 * trend
        + 0.20 * macd_signal
        + 0.15 * mean_reversion
        + 0.10 * volume_confirm
    )

    # Convert score to expected return scaled by realized volatility
    daily_vol = float(data["return_1d"].tail(60).std() or 0.02)
    expected_daily = score * daily_vol * 0.5
    expected_total = expected_daily * horizon_days

    # Confidence from data quality and signal agreement
    signs = [np.sign(momentum), np.sign(trend), np.sign(macd_signal)]
    agreement = abs(sum(signs)) / 3.0
    confidence = float(min(0.95, 0.4 + 0.35 * agreement + 0.2 * min(len(data) / 250, 1.0)))

    return {
        "ok": True,
        "expected_return": float(expected_total),
        "expected_return_daily": float(expected_daily),
        "confidence": confidence,
        "horizon_days": horizon_days,
        "volatility_daily": daily_vol,
        "components": {
            "momentum": float(momentum),
            "trend": float(trend),
            "macd": float(macd_signal),
            "mean_reversion": float(mean_reversion),
            "volume": float(volume_confirm),
        },
        "indicators": {
            "rsi_14": float(rsi) if pd.notna(rsi) else None,
            "ema_ratio_20": float(last.get("ema_ratio_20", 1.0)),
            "atr_14": float(last.get("atr_14", 0.0)),
        },
    }


def _clip(value: float, low: float = -1.0, high: float = 1.0) -> float:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return 0.0
    return float(np.clip(value, low, high))
