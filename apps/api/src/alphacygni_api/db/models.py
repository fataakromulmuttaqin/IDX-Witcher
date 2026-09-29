"""SQLAlchemy models for Alpha Cygni."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import String, Float, Integer, Date, DateTime, Boolean, Numeric, Index, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from Alpha Cygni_api.db.base import Base


class Company(Base):
    """Listed company profile."""

    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sector: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sub_sector: Mapped[str | None] = mapped_column(String(100), nullable=True)
    listing_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    shares: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    source: Mapped[str] = mapped_column(String(20), default="idx")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __table_args__ = (Index("ix_companies_sector", "sector"),)


class OHLCV(Base):
    """Daily OHLCV price record."""

    __tablename__ = "ohlcv"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    open_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    high_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    low_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    close_price: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    volume: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    value: Mapped[Decimal | None] = mapped_column(Numeric(28, 4), nullable=True)
    frequency: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source: Mapped[str] = mapped_column(String(20), default="yahoo")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (Index("ix_ohlcv_code_date", "code", "date", unique=True),)


class MarketSummary(Base):
    """Daily market/index summary."""

    __tablename__ = "market_summary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    index_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    index_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    open_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    high_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    low_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    close_value: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    change: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    change_percent: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    volume: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    value: Mapped[Decimal | None] = mapped_column(Numeric(28, 4), nullable=True)
    source: Mapped[str] = mapped_column(String(20), default="yahoo")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (Index("ix_market_summary_date_index", "date", "index_code", unique=True),)
