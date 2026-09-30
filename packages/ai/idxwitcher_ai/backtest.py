"""Backtest engine for portfolio strategies.

Provides a simple walk-forward backtest with monthly rebalancing.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def backtest_equal_weight(
    prices: pd.DataFrame,
    tickers: list[str],
    initial_cash: float = 100_000_000,
    rebalance_days: int = 21,
    fee: float = 0.0029,
) -> dict:
    """Backtest an equal-weight buy-and-hold strategy with periodic rebalancing.

    Args:
        prices: DataFrame indexed by date with one column per ticker close price.
        tickers: List of tickers to include.
        initial_cash: Starting capital in IDR.
        rebalance_days: Rebalance interval in trading days.
        fee: Total fee per side (buy + sell) as fraction.

    Returns:
        Dictionary with equity curve, metrics, and trades.
    """
    if not tickers or prices is None or prices.empty:
        return {"error": "insufficient_data"}

    subset = prices[tickers].dropna(how="all").ffill().bfill()
    if subset.empty:
        return {"error": "insufficient_data"}

    returns = subset.pct_change().fillna(0.0)
    n = len(tickers)
    weights = np.ones(n) / n
    portfolio_value = initial_cash
    cash = initial_cash
    shares = pd.Series(0.0, index=tickers)
    equity = []
    trades = 0

    for i, (date, row) in enumerate(subset.iterrows()):
        if i == 0:
            # Initial allocation
            target_value = initial_cash / n
            for t in tickers:
                shares[t] = target_value / row[t] if row[t] > 0 else 0.0
            cash = 0.0
        elif i > 0 and i % rebalance_days == 0:
            # Rebalance: sell all, then buy equal weight
            portfolio_value = sum(shares[t] * row[t] for t in tickers)
            trades += 2
            cash = portfolio_value * (1.0 - fee)
            target_value = cash / n
            for t in tickers:
                shares[t] = target_value / row[t] if row[t] > 0 else 0.0
            cash = 0.0

        portfolio_value = sum(shares[t] * row[t] for t in tickers) + cash
        equity.append({"date": date, "value": portfolio_value})

    equity_df = pd.DataFrame(equity).set_index("date")
    final_value = equity_df["value"].iloc[-1]
    total_return = final_value / initial_cash - 1.0
    equity_returns = equity_df["value"].pct_change().dropna()
    volatility = float(equity_returns.std() * np.sqrt(252))
    sharpe = float((equity_returns.mean() * 252 - 0.05) / (equity_returns.std() * np.sqrt(252))) if volatility > 0 else 0.0
    max_drawdown = float((equity_df["value"] / equity_df["value"].cummax() - 1.0).min())

    return {
        "initial_cash": initial_cash,
        "final_value": float(final_value),
        "total_return": float(total_return),
        "volatility_annual": volatility,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "trades": trades,
        "equity_curve": equity_df.reset_index().to_dict("records"),
    }
