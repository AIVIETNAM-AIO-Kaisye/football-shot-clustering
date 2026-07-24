"""Task 2 + T3.3 — Thống kê mô tả. CHỦ SỞ HỮU: Phong

    python scripts/03_descriptive.py
"""

from shotquality import config, descriptive, io_utils


def main() -> None:
    df = io_utils.load_csv(config.SHOTS_RAW_CSV)

    outputs = {
        "t2_describe": descriptive.numeric_summary(df),
        "t2_outcome": descriptive.outcome_distribution(df),
        "t2_categorical": descriptive.categorical_distribution(df, config.CATEGORICAL_FEATURES),
        "t2_sample_balance": descriptive.sample_balance(df),
        "t2_missing": descriptive.missing_report(df),
        "t3_feature_scales": descriptive.feature_scale_table(df, config.FEATURE_COLS),
    }

    for name, table in outputs.items():
        io_utils.save_csv(table, config.TABLES / f"{name}.csv")
        print(f"→ {name}.csv")


if __name__ == "__main__":
    main()
