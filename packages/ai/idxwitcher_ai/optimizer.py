"""Portfolio optimization for IDX stocks.

Mean-variance optimization with IDX market constraints:
- Buy fee 0.19%, sell fee 0.29%
- Lot size 100 shares
- Max weight per stock
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# IDX trading cost constants
BUY_FEE = 0.0019
SELL_FEE = 0.0029
LOT_SIZE = 100


RISK_PROFILES = {
    "conservative": {
        "target_return": 0.08,
        "max_weight": 0.25,
        "max_volatility": 0.15,
        "cash_min": 0.10,
        "top_k": 6,
    },
    "moderate": {
        "target_return": 0.12,
        "max_weight": 0.20,
        "max_volatility": 0.22,
        "cash_min": 0.05,
        "top_k": 8,
    },
    "aggressive": {
        "target_return": 0.18,
        "max_weight": 0.18,
        "max_volatility": 0.32,
        "cash_min": 0.0,
        "top_k": 10,
    },
}


def portfolio_volatility(weights: np.ndarray, cov: np.ndarray) -> float:
    """Annualized portfolio volatility."""
    return float(np.sqrt(weights @ cov @ weights) * np.sqrt(252))


def portfolio_return(weights: np.ndarray, expected_returns: np.ndarray, periods_per_year: int = 252) -> float:
    """Annualized expected portfolio return."""
    return float(weights @ expected_returns * periods_per_year)


def transaction_cost(weights: np.ndarray, turnover: np.ndarray) -> float:
    """Estimate transaction cost from turnover (fraction of portfolio)."""
    buys = np.clip(turnover, 0, None)
    sells = np.clip(-turnover, 0, None)
    return float(buys.sum() * BUY_FEE + sells.sum() * SELL_FEE)


def optimize_portfolio(
    expected_returns: np.ndarray,
    cov: np.ndarray,
    risk_profile: str = "moderate",
    num_samples: int = 20000,
    seed: int = 42,
) -> dict:
    """Find portfolio weights via random search + constraint filtering.

    This is a pragmatic substitute for full quadratic programming,
    suitable for online inference with a small universe (<=50 tickers).
    """
    profile = RISK_PROFILES.get(risk_profile, RISK_PROFILES["moderate"])
    n = len(expected_returns)
    if n == 0:
        return {"weights": [], "expected_return": 0.0, "volatility": 0.0, "sharpe": 0.0}

    rng = np.random.default_rng(seed)
    max_w = profile["max_weight"]
    cash_min = profile["cash_min"]
    max_vol = profile["max_volatility"]

    best = None
    best_score = -np.inf

    for _ in range(num_samples):
        # Dirichlet sampling gives naturally diversified weights
        alpha = np.ones(n) * 1.5
        w = rng.dirichlet(alpha)
        # Cap max weight and renormalize the non-cash portion
        w = np.minimum(w, max_w)
        investable = 1.0 - cash_min
        if w.sum() == 0:
            continue
        w = w / w.sum() * investable

        vol = portfolio_volatility(w, cov)
        if vol > max_vol:
            continue

        exp_ret = portfolio_return(w, expected_returns)
        score = (exp_ret - 0.02) / vol if vol > 1e-8 else -np.inf

        if score > best_score:
            best_score = score
            best = w

    if best is None:
        # Fallback: equal weight with cash floor
        investable = 1.0 - cash_min
        best = np.ones(n) / n * investable
        best_score = 0.0

    vol = portfolio_volatility(best, cov)
    exp_ret = portfolio_return(best, expected_returns)

    return {
        "weights": best.tolist(),
        "expected_return": exp_ret,
        "volatility": vol,
        "sharpe": float((exp_ret - 0.05) / vol) if vol > 1e-8 else 0.0,
        "cash_weight": float(1.0 - best.sum()),
        "risk_profile": risk_profile,
    }


def estimate_moments(returns_df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Estimate expected returns (mean daily) and covariance matrix."""
    returns = returns_df.dropna(axis=1, how="all").fillna(0.0)
    expected = returns.mean().to_numpy()
    cov = returns.cov().to_numpy()
    # Regularize covariance for numerical stability
    cov = cov + np.eye(len(cov)) * 1e-6
    return expected, cov
