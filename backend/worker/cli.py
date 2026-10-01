import argparse


def main() -> None:
    p = argparse.ArgumentParser(prog="worker.cli")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seed", help="isi companies dari data/companies_seed.csv")
    sub.add_parser("run-once", help="jalankan pipeline harian sekarang")
    bf = sub.add_parser("backfill", help="isi riwayat harga")
    bf.add_argument("--start", default="2021-01-01")
    p.parse_args()


if __name__ == "__main__":
    main()
