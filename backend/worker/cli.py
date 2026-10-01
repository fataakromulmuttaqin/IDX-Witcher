import argparse

from worker.jobs import compute_indicators, ingest_prices, run_rules, sync_companies
from worker.pipeline import run_daily_pipeline


def main() -> None:
    p = argparse.ArgumentParser(prog="worker.cli")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seed", help="isi companies dari data/companies_seed.csv")
    sub.add_parser("run-once", help="jalankan pipeline harian sekarang")
    bf = sub.add_parser("backfill", help="isi riwayat harga")
    bf.add_argument("--start", default="2021-01-01")
    args = p.parse_args()

    if args.cmd == "seed":
        sync_companies.run()
    elif args.cmd == "run-once":
        run_daily_pipeline(force=True)
    elif args.cmd == "backfill":
        ingest_prices.run(start=args.start)
        compute_indicators.run(calendar_days=3650, write_last_sessions=100000)
        run_rules.run()


if __name__ == "__main__":
    main()
