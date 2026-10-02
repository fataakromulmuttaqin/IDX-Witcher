from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


def _float():
    return mapped_column(Float, nullable=True)


class Sector(Base):
    __tablename__ = "sectors"
    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    code: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)


class Company(Base):
    __tablename__ = "companies"
    ticker: Mapped[str] = mapped_column(String, primary_key=True)
    yahoo_symbol: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)
    sector_id: Mapped[int | None] = mapped_column(ForeignKey("sectors.id"))
    subsector: Mapped[str | None] = mapped_column(String)
    board: Mapped[str | None] = mapped_column(String)
    listing_date: Mapped[date | None] = mapped_column(Date)
    shares_outstanding: Mapped[int | None] = mapped_column(BigInteger)
    is_financial: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class PriceDaily(Base):
    __tablename__ = "prices_daily"
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"), primary_key=True)
    trade_date: Mapped[date] = mapped_column(Date, primary_key=True)
    open: Mapped[float | None] = mapped_column(Numeric(18, 4))
    high: Mapped[float | None] = mapped_column(Numeric(18, 4))
    low: Mapped[float | None] = mapped_column(Numeric(18, 4))
    close: Mapped[float] = mapped_column(Numeric(18, 4))
    adj_close: Mapped[float | None] = mapped_column(Numeric(18, 4))
    volume: Mapped[int | None] = mapped_column(BigInteger)
    value_traded: Mapped[float | None] = mapped_column(Numeric(24, 2))
    is_suspect: Mapped[bool] = mapped_column(Boolean, default=False)


class IndicatorDaily(Base):
    __tablename__ = "indicators_daily"
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"), primary_key=True)
    trade_date: Mapped[date] = mapped_column(Date, primary_key=True)
    ret_1d: Mapped[float | None] = _float()
    ret_1m: Mapped[float | None] = _float()
    ret_3m: Mapped[float | None] = _float()
    ret_ytd: Mapped[float | None] = _float()
    ret_1y: Mapped[float | None] = _float()
    sma20: Mapped[float | None] = _float()
    sma50: Mapped[float | None] = _float()
    sma150: Mapped[float | None] = _float()
    sma200: Mapped[float | None] = _float()
    hi_52w: Mapped[float | None] = _float()
    lo_52w: Mapped[float | None] = _float()
    vol_avg20: Mapped[float | None] = mapped_column(Float(53))
    value_avg20: Mapped[float | None] = mapped_column(Float(53))
    atr14: Mapped[float | None] = _float()
    rs_rating: Mapped[int | None] = mapped_column(SmallInteger)


class FundamentalsSnapshot(Base):
    __tablename__ = "fundamentals_snapshot"
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"), primary_key=True)
    as_of: Mapped[date] = mapped_column(Date, primary_key=True)
    market_cap: Mapped[float | None] = mapped_column(Numeric(28, 2))
    pe_ttm: Mapped[float | None] = _float()
    pb: Mapped[float | None] = _float()
    ps: Mapped[float | None] = _float()
    ev_ebitda: Mapped[float | None] = _float()
    roe: Mapped[float | None] = _float()
    roa: Mapped[float | None] = _float()
    gross_margin: Mapped[float | None] = _float()
    op_margin: Mapped[float | None] = _float()
    net_margin: Mapped[float | None] = _float()
    debt_equity: Mapped[float | None] = _float()
    current_ratio: Mapped[float | None] = _float()
    div_yield: Mapped[float | None] = _float()
    payout: Mapped[float | None] = _float()
    revenue_ttm: Mapped[float | None] = mapped_column(Numeric(28, 2))
    net_income_ttm: Mapped[float | None] = mapped_column(Numeric(28, 2))
    fcf_ttm: Mapped[float | None] = mapped_column(Numeric(28, 2))
    rev_growth_yoy: Mapped[float | None] = _float()
    eps_growth_yoy: Mapped[float | None] = _float()
    na_reason: Mapped[dict] = mapped_column(JSONB, default=dict)


class CorporateAction(Base):
    __tablename__ = "corporate_actions"
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"), primary_key=True)
    action_date: Mapped[date] = mapped_column(Date, primary_key=True)
    kind: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[float] = mapped_column(Numeric(18, 6))


class FinancialStatement(Base):
    __tablename__ = "financial_statements"
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"), primary_key=True)
    period_end: Mapped[date] = mapped_column(Date, primary_key=True)
    period_type: Mapped[str] = mapped_column(String, primary_key=True)
    statement: Mapped[str] = mapped_column(String, primary_key=True)
    item: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[float | None] = mapped_column(Numeric(28, 2))
    currency: Mapped[str] = mapped_column(String, default="IDR")
    source: Mapped[str] = mapped_column(String, default="yfinance")


class Watchlist(Base):
    __tablename__ = "watchlists"
    slug: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    rule_expr: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(SmallInteger, default=0)


class WatchlistMember(Base):
    __tablename__ = "watchlist_members"
    slug: Mapped[str] = mapped_column(String, primary_key=True)
    trade_date: Mapped[date] = mapped_column(Date, primary_key=True)
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"), primary_key=True)
    rank: Mapped[int | None] = mapped_column(Integer)


class Signal(Base):
    __tablename__ = "signals"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    trade_date: Mapped[date] = mapped_column(Date)
    ticker: Mapped[str] = mapped_column(ForeignKey("companies.ticker"))
    kind: Mapped[str] = mapped_column(String)
    detail: Mapped[dict] = mapped_column(JSONB, default=dict)


class SectorScore(Base):
    __tablename__ = "sector_scores"
    trade_date: Mapped[date] = mapped_column(Date, primary_key=True)
    sector_id: Mapped[int] = mapped_column(ForeignKey("sectors.id"), primary_key=True)
    members: Mapped[int] = mapped_column(Integer)
    med_ret_3m: Mapped[float | None] = _float()
    pct_above_sma50: Mapped[float | None] = _float()
    score: Mapped[float | None] = _float()
    rank: Mapped[int | None] = mapped_column(SmallInteger)
    is_leading: Mapped[bool] = mapped_column(Boolean, default=False)


class IngestRun(Base):
    __tablename__ = "ingest_runs"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    job: Mapped[str] = mapped_column(String)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String, default="running")
    rows_written: Mapped[int | None] = mapped_column(Integer)
    tickers_failed: Mapped[int | None] = mapped_column(Integer)
    error: Mapped[str | None] = mapped_column(Text)
