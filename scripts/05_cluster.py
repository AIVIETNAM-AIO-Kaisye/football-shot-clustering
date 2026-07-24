"""Task 5.1–5.4 — K-Means + chọn K cho một nhánh. CHỦ SỞ HỮU: B
(A dùng lại script này cho nhánh unscaled — ADR-010, không copy code)

    python scripts/05_cluster.py --arm scaled
    python scripts/05_cluster.py --arm unscaled
"""

import argparse

from shotquality import clustering, config, io_utils, selection, selection_gap


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arm", choices=["scaled", "unscaled"], required=True)
    parser.add_argument("--skip-gap", action="store_true",
                        help="bỏ Gap Statistic (dùng khi descope)")
    args = parser.parse_args()

    path = config.X_SCALED_CSV if args.arm == "scaled" else config.X_UNSCALED_CSV
    X = io_utils.load_csv(path)

    elbow = selection.elbow_curve(X)
    sil = selection.silhouette_by_k(X)
    gap = None if args.skip_gap else selection_gap.gap_statistic(X)

    summary = selection.summarize_k_selection(elbow, sil, gap)
    io_utils.save_csv(summary, config.TABLES / f"t5_k_selection_{args.arm}.csv")
    print(summary)

    k = int(input("Chốt k cho nhánh này: "))
    labels, inertia, model = clustering.run_kmeans(X, k)

    out = config.LABELS_SCALED_CSV if args.arm == "scaled" else config.LABELS_UNSCALED_CSV
    io_utils.save_csv(labels, out)
    print(f"k={k} · inertia={inertia:.1f} → {out}")


if __name__ == "__main__":
    main()
