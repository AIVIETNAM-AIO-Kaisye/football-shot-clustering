"""T1.2 + T1.5 — Trích xuất shot → shots_raw.csv (artifact GATE 1). CHỦ SỞ HỮU: Phong

    python scripts/02_extract_shots.py
"""

from shotquality import config, ingest, io_utils


def main() -> None:
    df = ingest.build_shots_dataframe()
    ingest.sanity_check(df)
    io_utils.save_csv(df, config.SHOTS_RAW_CSV)
    print(f"{len(df)} shot → {config.SHOTS_RAW_CSV}")


if __name__ == "__main__":
    main()
