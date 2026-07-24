"""T0.1 + T1.1 — Tải events JSON. CHỦ SỞ HỮU: A

    python scripts/01_download.py
"""

from shotquality import config, ingest, io_utils


def main() -> None:
    io_utils.ensure_dirs()
    matches = ingest.fetch_match_ids()
    print(f"Tìm thấy {len(matches)} trận từ {len(config.COMPETITIONS)} giải")
    ingest.download_events([m["match_id"] for m in matches])
    print(f"Đã tải xong → {config.DATA_RAW}")


if __name__ == "__main__":
    main()
