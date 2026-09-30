"""Portfolio builder router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np

from idxwitcher_api.db import get_db
from idxwitcher_api.db.models import OHLCV

import sys
from pathlib import Path

_AI_ROOT = Path(__file__).resolve().parents[4] / "packages" / "ai"
sys.path.insert(0, str(_AI_ROOT))
from idxwitcher_ai.inference import predict_returns
from idxwitcher_ai.optimizer import optimize_portfolio, estimate_moments

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


LQ45_TICKERS = [
    "ACES", "ADRO", "AKR", "AMMN", "AMRT", "ANTM", "ARTO", "ASII", "BBCA", "BBNI",
    "BBRI", "BMRI", "BRMS", "BRPT", "BTPN", "CAMP", "CARE", "CEPU", "CMRY", "CPIN",
    "DCII", "DMAS", "DOID", "DSFI", "ELSA", "EXCL", "GGRM", "GJTL", "GOTO", "HRUM",
    "ICBP", "INCO", "INDF", "INKP", "INTP", "ITMG", "JPFA", "JSMR", "KLBF", "MAPI",
    "MBMA", "MEDC", "MIKA", "MNCN", "MTEL", "MNCN", "MTEL", "PTBA", "SMGR", "SRIL",
    "TINS", "TKIM", "TLKM", "TPIA", "UNTR", "UNVR",
]


def _fetch_prices(db: Session, tickers: list[str], min_days: int = 60) -> dict[str, pd.DataFrame]:
    data = {}
    for code in tickers:
        records = (
            db.query(OHLCV)
            .filter(OHLCV.code == code.upper())
            .order_by(OHLCV.date.asc())
            .all()
        )
        if not records or len(records) < min_days:
            continue
        df = pd.DataFrame(
            [
                {
                    "date": r.date,
                    "open": r.open_price,
                    "high": r.high_price,
                    "low": r.low_price,
                    "close": r.close_price,
                    "volume": r.volume,
                }
                for r in records
            ]
        )
        data[code.upper()] = df
    return data


@router.post("/build")
def build_portfolio(
    risk_profile: str = "moderate",
    universe: list[str] | None = None,
    db: Session = Depends(get_db),
):
    """Build AI-recommended portfolio from available OHLCV data."""
    tickers = universe or LQ45_TICKERS
    prices = _fetch_prices(db, tickers, min_days=60)

    if not prices:
        raise HTTPException(status_code=400, detail="No price data available for portfolio build")

    # Predict returns for each available ticker
    predictions = {}
    for code, df in prices.items():
        try:
            pred = predict_returns(df)
            predictions[code] = pred
        except Exception:
            continue

    if not predictions:
        raise HTTPException(status_code=400, detail="Could not generate predictions for any ticker")

    # Filter to positive expected return predictions, sorted by expected return
    ranked = sorted(
        predictions.items(),
        key=lambda x: x[1].get("expected_return", -np.inf),
        reverse=True,
    )
    selected = [code for code, _ in ranked[:12]]

    # Build returns matrix and estimate moments
    returns_dict = {}
    for code in selected:
        df = prices[code].set_index("date")
        rets = df["close"].pct_change().dropna()
        rets.name = code
        returns_dict[code] = rets

    returns_df = pd.DataFrame(returns_dict).dropna()
    if returns_df.empty or len(returns_df.columns) < 2:
        raise HTTPException(status_code=400, detail="Insufficient return history to optimize")

    expected, cov = estimate_moments(returns_df)
    opt = optimize_portfolio(expected, cov, risk_profile=risk_profile, num_samples=10000)

    weights = opt["weights"]
    portfolio_items = []
    for code, weight in zip(returns_df.columns, weights):
        portfolio_items.append(
            {
                "code": code,
                "weight": round(weight, 4),
                "expected_return_5d": round(predictions[code].get("expected_return", 0.0), 4),
                "confidence": round(predictions[code].get("confidence", 0.0), 4),
            }
        )

    return {
        "ok": True,
        "risk_profile": risk_profile,
        "portfolio": portfolio_items,
        "cash_weight": opt["cash_weight"],
        "expected_return_annual": opt["expected_return"],
        "volatility_annual": opt["volatility"],
        "sharpe": opt["sharpe"],
    }


@router.post("/backtest")
def backtest_portfolio(
    tickers: list[str],
    initial_cash: float = 100_000_000,
    db: Session = Depends(get_db),
):
    """Run a simple equal-weight backtest for given tickers."""
    import sys
    _AI_ROOT = Path(__file__).resolve().parents[4] / "packages" / "ai"
    sys.path.insert(0, str(_AI_ROOT))
    from idxwitcher_ai.backtest import backtest_equal_weight

    prices_dict = _fetch_prices(db, tickers, min_days=60)
    if not prices_dict:
        raise HTTPException(status_code=400, detail="No price data available for backtest")

    prices = None
    for code, df in prices_dict.items():
        df = df.set_index("date")[["close"]].rename(columns={"close": code})
        if prices is None:
            prices = df
        else:
            prices = prices.join(df, how="outer")

    if prices is None:
        raise HTTPException(status_code=400, detail="No price data available for backtest")

    prices = prices.ffill().bfill()
    result = backtest_equal_weight(prices, list(prices.columns), initial_cash=initial_cash)
    return result
