"""AI router for return predictions and model metadata."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

from idxwitcher_api.db import get_db
from idxwitcher_api.db.models import OHLCV

# Local AI package import
import sys
from pathlib import Path

_AI_ROOT = Path(__file__).resolve().parents[4] / "packages" / "ai"
sys.path.insert(0, str(_AI_ROOT))
from idxwitcher_ai.inference import predict_returns

router = APIRouter(prefix="/ai", tags=["AI"])


def _ohlcv_to_dataframe(records: list[OHLCV]) -> pd.DataFrame:
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
    return df


@router.get("/predict/{ticker}")
def predict_ticker(ticker: str, horizon_days: int = 5, db: Session = Depends(get_db)):
    records = (
        db.query(OHLCV)
        .filter(OHLCV.code == ticker.upper())
        .order_by(OHLCV.date.asc())
        .all()
    )
    if not records:
        raise HTTPException(status_code=404, detail="No price data for ticker")

    df = _ohlcv_to_dataframe(records)
    result = predict_returns(df, horizon_days=horizon_days)
    return {
        "ok": result.get("ok"),
        "ticker": ticker.upper(),
        "horizon_days": horizon_days,
        "expected_return": result.get("expected_return"),
        "expected_return_daily": result.get("expected_return_daily"),
        "confidence": result.get("confidence"),
        "volatility_daily": result.get("volatility_daily"),
        "components": result.get("components"),
        "indicators": result.get("indicators"),
    }
