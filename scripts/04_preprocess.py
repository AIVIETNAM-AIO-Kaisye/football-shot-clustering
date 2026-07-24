"""Task 4 — Sinh X_scaled / X_unscaled / y_hidden (artifact GATE 2). CHỦ SỞ HỮU: Thông

    python scripts/04_preprocess.py
"""

from shotquality import config, io_utils, preprocess


def main() -> None:
    df = io_utils.load_csv(config.SHOTS_RAW_CSV)

    X, y_hidden, ids = preprocess.split_column_groups(df)
    X = preprocess.encode_categoricals(X)
    X, missing_report = preprocess.handle_missing(X)
    X_unscaled, X_scaled = preprocess.make_scaled_unscaled(X)

    preprocess.save_all(X_unscaled, X_scaled, y_hidden, ids)

    print(f"X: {X_scaled.shape} | y_hidden: {y_hidden.shape}")
    print(f"Missing đã xử lý: {missing_report}  ← ghi vào DECISIONS.md")


if __name__ == "__main__":
    main()
