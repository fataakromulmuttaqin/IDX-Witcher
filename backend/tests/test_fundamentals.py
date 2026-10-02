import pandas as pd

from worker.fundamentals import compute_snapshot


def _df(**rows):
    dates = pd.date_range("2025-03-31", periods=5, freq="QE")
    return pd.DataFrame(rows, index=dates).T


def test_compute_snapshot_bank_financial_na_reason():
    income = _df(**{
        "Total Revenue": [200_000_000, 200_000_000, 200_000_000, 200_000_000, 200_000_000],
        "Net Income": [50_000_000, 50_000_000, 50_000_000, 50_000_000, 50_000_000],
        "Gross Profit": [80_000_000, 80_000_000, 80_000_000, 80_000_000, 80_000_000],
        "Operating Income": [60_000_000, 60_000_000, 60_000_000, 60_000_000, 60_000_000],
        "EBITDA": [70_000_000, 70_000_000, 70_000_000, 70_000_000, 70_000_000],
    })
    balance = _df(**{
        "Stockholders Equity": [200_000_000, 200_000_000, 200_000_000, 200_000_000, 200_000_000],
        "Total Assets": [500_000_000, 500_000_000, 500_000_000, 500_000_000, 500_000_000],
        "Total Debt": [100_000_000, 100_000_000, 100_000_000, 100_000_000, 100_000_000],
        "Cash And Cash Equivalents": [50_000_000, 50_000_000, 50_000_000, 50_000_000, 50_000_000],
        "Current Assets": [100_000_000, 100_000_000, 100_000_000, 100_000_000, 100_000_000],
        "Current Liabilities": [50_000_000, 50_000_000, 50_000_000, 50_000_000, 50_000_000],
    })
    cashflow = _df(**{"Free Cash Flow": [25_000_000, 25_000_000, 25_000_000, 25_000_000, 25_000_000]})

    snap = compute_snapshot(
        price=1000,
        shares=1_000_000,
        is_financial=True,
        info={},
        income=income,
        balance=balance,
        cashflow=cashflow,
        div12=0,
    )

    assert snap["market_cap"] == 1_000_000_000
    assert snap["pe_ttm"] is not None
    assert snap["roe"] is not None
    assert snap["na_reason"]["debt_equity"] == "bank"
    assert snap["na_reason"]["current_ratio"] == "bank"
    assert snap["na_reason"]["ev_ebitda"] == "bank"


def test_compute_snapshot_loss_company():
    income = _df(**{
        "Total Revenue": [100, 100, 100, 100, 100],
        "Net Income": [-10, -10, -10, -10, -10],
        "Gross Profit": [40, 40, 40, 40, 40],
        "Operating Income": [-5, -5, -5, -5, -5],
        "EBITDA": [0, 0, 0, 0, 0],
    })
    balance = _df(**{
        "Stockholders Equity": [200, 200, 200, 200, 200],
        "Total Assets": [500, 500, 500, 500, 500],
        "Total Debt": [100, 100, 100, 100, 100],
        "Cash And Cash Equivalents": [50, 50, 50, 50, 50],
        "Current Assets": [100, 100, 100, 100, 100],
        "Current Liabilities": [50, 50, 50, 50, 50],
    })
    cashflow = _df(**{"Free Cash Flow": [25, 25, 25, 25, 25]})

    snap = compute_snapshot(
        price=1000,
        shares=1_000_000_000,
        is_financial=False,
        info={},
        income=income,
        balance=balance,
        cashflow=cashflow,
        div12=0,
    )

    assert snap["pe_ttm"] is None
    assert snap["na_reason"].get("pe_ttm") == "loss"
