"""Feature engineering for IDX stock price prediction."""

from __future__ import annotations

import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=RuntimeWarning)


def add_feature_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Add technical and macro features to OHLCV DataFrame.

    Features added:
    - Returns, log returns
    - Moving averages (EMA 5/10/20/50)
    - RSI(14)
    - MACD
    - Bollinger Bands
    - ATR(14)
    - Volume SMA
    - Momentum
    - Lag features
    """
    data = df.copy().sort_values("date").reset_index(drop=True)

    if "close" not in data.columns:
        raise ValueError("DataFrame must contain a 'close' column")

    # Returns
    data["return_1d"] = data["close"].pct_change()
    data["log_return"] = np.log(data["close"].astype(float) / data["close"].shift(1).astype(float))

    # EMAs
    for window in [5, 10, 20, 50]:
        data[f"ema_{window}"] = data["close"].ewm(span=window, adjust=False).mean()
        data[f"ema_ratio_{window}"] = data["close"] / data[f"ema_{window}"]

    # RSI
    data["rsi_14"] = _rsi(data["close"], 14)

    # MACD
    ema_12 = data["close"].ewm(span=12, adjust=False).mean()
    ema_26 = data["close"].ewm(span=26, adjust=False).mean()
    data["macd"] = ema_12 - ema_26
    data["macd_signal"] = data["macd"].ewm(span=9, adjust=False).mean()
    data["macd_hist"] = data["macd"] - data["macd_signal"]

    # Bollinger Bands
    data["bb_mid"] = data["close"].rolling(window=20).mean()
    bb_std = data["close"].rolling(window=20).std()
    data["bb_upper"] = data["bb_mid"] + 2 * bb_std
    data["bb_lower"] = data["bb_mid"] - 2 * bb_std
    data["bb_position"] = (data["close"] - data["bb_lower"]) / (data["bb_upper"] - data["bb_lower"])

    # ATR
    data["atr_14"] = _atr(data, 14)

    # Volume features
    data["volume_sma_20"] = data["volume"].rolling(window=20).mean()
    data["volume_ratio"] = data["volume"] / data["volume_sma_20"]

    # Momentum
    data["momentum_5"] = data["close"] / data["close"].shift(5) - 1
    data["momentum_10"] = data["close"] / data["close"].shift(10) - 1
    data["momentum_20"] = data["close"] / data["close"].shift(20) - 1

    # Lag features
    for lag in [1, 2, 3, 5]:
        data[f"close_lag_{lag}"] = data["close"].shift(lag)
        data[f"return_lag_{lag}"] = data["return_1d"].shift(lag)

    return data


def _rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def _atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    high = df["high"]
    low = df["low"]
    close = df["close"]
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=window).mean()
