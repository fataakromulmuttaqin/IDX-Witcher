from alembic import op

revision = "0001"
down_revision = None

SQL = """
CREATE TABLE sectors (
  id    SMALLINT PRIMARY KEY,
  code  TEXT NOT NULL UNIQUE,
  name  TEXT NOT NULL
);

CREATE TABLE companies (
  ticker             TEXT PRIMARY KEY,
  yahoo_symbol       TEXT NOT NULL UNIQUE,
  name               TEXT NOT NULL,
  sector_id          SMALLINT REFERENCES sectors(id),
  subsector          TEXT,
  board              TEXT,
  listing_date       DATE,
  shares_outstanding BIGINT,
  is_financial       BOOLEAN NOT NULL DEFAULT FALSE,
  is_active          BOOLEAN NOT NULL DEFAULT TRUE,
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE prices_daily (
  ticker       TEXT NOT NULL REFERENCES companies(ticker),
  trade_date   DATE NOT NULL,
  open         NUMERIC(18,4),
  high         NUMERIC(18,4),
  low          NUMERIC(18,4),
  close        NUMERIC(18,4) NOT NULL,
  adj_close    NUMERIC(18,4),
  volume       BIGINT,
  value_traded NUMERIC(24,2),
  is_suspect   BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (ticker, trade_date)
);

CREATE INDEX ix_prices_date ON prices_daily (trade_date);

CREATE TABLE corporate_actions (
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  action_date DATE NOT NULL,
  kind        TEXT NOT NULL CHECK (kind IN ('dividend','split')),
  value       NUMERIC(18,6) NOT NULL,
  PRIMARY KEY (ticker, action_date, kind)
);

CREATE TABLE financial_statements (
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  period_end  DATE NOT NULL,
  period_type TEXT NOT NULL CHECK (period_type IN ('Q','FY')),
  statement   TEXT NOT NULL CHECK (statement IN ('IS','BS','CF')),
  item        TEXT NOT NULL,
  value       NUMERIC(28,2),
  currency    TEXT NOT NULL DEFAULT 'IDR',
  source      TEXT NOT NULL DEFAULT 'yfinance',
  PRIMARY KEY (ticker, period_end, period_type, statement, item)
);

CREATE TABLE indicators_daily (
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  trade_date  DATE NOT NULL,
  ret_1d REAL, ret_1m REAL, ret_3m REAL, ret_ytd REAL, ret_1y REAL,
  sma20 REAL, sma50 REAL, sma150 REAL, sma200 REAL,
  hi_52w REAL, lo_52w REAL,
  vol_avg20   DOUBLE PRECISION,
  value_avg20 DOUBLE PRECISION,
  atr14       REAL,
  rs_rating   SMALLINT,
  PRIMARY KEY (ticker, trade_date)
);

CREATE TABLE fundamentals_snapshot (
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  as_of       DATE NOT NULL,
  market_cap  NUMERIC(28,2),
  pe_ttm REAL, pb REAL, ps REAL, ev_ebitda REAL,
  roe REAL, roa REAL, gross_margin REAL, op_margin REAL, net_margin REAL,
  debt_equity REAL, current_ratio REAL,
  div_yield REAL, payout REAL,
  revenue_ttm NUMERIC(28,2), net_income_ttm NUMERIC(28,2), fcf_ttm NUMERIC(28,2),
  rev_growth_yoy REAL, eps_growth_yoy REAL,
  na_reason   JSONB NOT NULL DEFAULT '{}'::jsonb,
  PRIMARY KEY (ticker, as_of)
);

CREATE TABLE watchlists (
  slug        TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  description TEXT NOT NULL,
  rule_expr   TEXT NOT NULL,
  sort_order  SMALLINT NOT NULL DEFAULT 0
);

CREATE TABLE watchlist_members (
  slug        TEXT NOT NULL REFERENCES watchlists(slug),
  trade_date  DATE NOT NULL,
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  rank        INTEGER,
  PRIMARY KEY (slug, trade_date, ticker)
);

CREATE TABLE signals (
  id          BIGSERIAL PRIMARY KEY,
  trade_date  DATE NOT NULL,
  ticker      TEXT NOT NULL REFERENCES companies(ticker),
  kind        TEXT NOT NULL,
  detail      JSONB NOT NULL DEFAULT '{}'::jsonb,
  UNIQUE (trade_date, ticker, kind)
);

CREATE INDEX ix_signals_date ON signals (trade_date DESC);

CREATE TABLE ingest_runs (
  id             BIGSERIAL PRIMARY KEY,
  job            TEXT NOT NULL,
  started_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at    TIMESTAMPTZ,
  status         TEXT NOT NULL DEFAULT 'running',
  rows_written   INTEGER,
  tickers_failed INTEGER,
  error          TEXT
);

CREATE TABLE users (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email      TEXT NOT NULL UNIQUE,
  pw_hash    TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
)
"""

TABLES = [
    "users", "ingest_runs", "signals", "watchlist_members",
    "watchlists", "fundamentals_snapshot", "indicators_daily", "financial_statements",
    "corporate_actions", "prices_daily", "companies", "sectors",
]


def upgrade() -> None:
    for stmt in (s.strip() for s in SQL.split(";")):
        if stmt:
            op.execute(stmt)


def downgrade() -> None:
    for table in TABLES:
        op.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
