from alembic import op

revision = "0002"
down_revision = "0001"

SQL = """
CREATE TABLE sector_scores (
  trade_date       DATE NOT NULL,
  sector_id        SMALLINT NOT NULL REFERENCES sectors(id),
  members          INTEGER NOT NULL,
  med_ret_3m       REAL,
  pct_above_sma50  REAL,
  score            REAL,
  rank             SMALLINT,
  is_leading       BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (trade_date, sector_id)
);
"""


def upgrade() -> None:
    op.execute(SQL)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS sector_scores CASCADE")
