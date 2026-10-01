import pandas as pd

from worker.quality import flag_suspect


def test_flags_bad_range_and_large_jump():
    df = pd.DataFrame(
        {
            "ticker": ["AAAA"] * 3,
            "date": pd.to_datetime(["2026-09-28", "2026-09-29", "2026-09-30"]).date,
            "open": [100, 100, 100],
            "high": [101, 101, 160],
            "low": [99, 105, 99],
            "close": [100, 100, 150],
        }
    )
    flags = flag_suspect(df).tolist()
    assert flags == [False, True, True]
