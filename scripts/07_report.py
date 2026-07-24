"""Task 6.3–6.4 — Gộp toàn bộ bảng kết quả vào final_report.md. CHỦ SỞ HỮU: Lộc

    python scripts/07_report.py
"""

from shotquality import config, io_utils

# 4 bảng bắt buộc có trong report (xem PLAN.md GATE 4)
REQUIRED_TABLES = [
    "t5_k_selection_unscaled",
    "t5_k_selection_scaled",
    "t5_knn_cv",
    "t6_cluster_profile",
]


def main() -> None:
    missing = [t for t in REQUIRED_TABLES if not (config.TABLES / f"{t}.csv").exists()]
    if missing:
        raise SystemExit(f"Thiếu bảng kết quả: {missing}")

    # TODO T6.4 @loc — render các bảng vào reports/final_report.md
    raise NotImplementedError("T6.4 @loc")


if __name__ == "__main__":
    main()
