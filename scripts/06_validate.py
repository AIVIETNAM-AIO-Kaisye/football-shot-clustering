"""Task 5.3 + 5.5 + 6.2 — ARI, KNN-CV, external validation. CHỦ SỞ HỮU: C

    python scripts/06_validate.py
"""

from shotquality import config, evaluate, io_utils, validation


def main() -> None:
    X = io_utils.load_csv(config.X_SCALED_CSV)
    y_hidden = io_utils.load_csv(config.Y_HIDDEN_CSV)
    lab_scaled = io_utils.load_csv(config.LABELS_SCALED_CSV)
    lab_unscaled = io_utils.load_csv(config.LABELS_UNSCALED_CSV)

    # T5.3 — scaling đổi kết quả phân cụm bao nhiêu?
    ari = validation.compare_labelings(lab_scaled["cluster_id"], lab_unscaled["cluster_id"])
    print(f"ARI scaled vs unscaled = {ari:.4f}")

    # T5.5 — cụm có ổn định / tổng quát hoá được không?
    cv = validation.knn_cv(X, lab_scaled["cluster_id"])
    io_utils.save_csv(cv, config.TABLES / "t5_knn_cv.csv")
    print(validation.stability_summary(cv))

    # T6.2 — cụm có ý nghĩa thực tế không? (field đã giấu)
    profile = evaluate.cluster_profile(lab_scaled["cluster_id"], y_hidden, X)
    io_utils.save_csv(profile, config.TABLES / "t6_cluster_profile.csv")
    print(profile)
    print(evaluate.rank_agreement(profile))


if __name__ == "__main__":
    main()
