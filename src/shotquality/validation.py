"""Kiểm định cụm: ARI + KNN cross-validation — CHỦ SỞ HỮU: Lộc (branch `eval-eng`).

Task T5.3a, T5.5a.

💡 Ngày 2 phát triển và test toàn bộ module này trên ``sklearn.datasets.make_blobs``
   — không cần chờ X thật của Thông. Đây là điều kiện để 3 luồng chạy song song.
"""

from __future__ import annotations

import pandas as pd

from . import config


def compare_labelings(labels_a, labels_b) -> float:
    """Adjusted Rand Index giữa hai tập nhãn. T5.3a.

    Diễn giải: ARI ≈ 0 ⇒ scaling đổi hoàn toàn kết quả phân cụm;
    ARI ≈ 1 ⇒ hầu như không đổi.

    ⚠️ Chỉ có nghĩa khi so ở **cùng một k**.
    ⚠️ Test bắt buộc: hoán vị tên nhãn (0↔1) phải cho ARI = 1.0.
    """
    raise NotImplementedError("T5.3a @loc")


def knn_cv(
    X: pd.DataFrame,
    labels,
    n_neighbors_grid=config.KNN_NEIGHBORS_GRID,
    cv: int = config.CV_FOLDS,
) -> pd.DataFrame:
    """KNN + k-fold CV dự đoán ``cluster_id``. T5.5a — ADR-011.

    Trả DataFrame ``[k_neighbors, mean_acc, std_acc, fold_accs]``.

    ⚠️ Dùng ``StratifiedKFold`` — các cụm thường lệch kích thước nhiều.
    ⚠️ metric L2: ``metric=config.DISTANCE_METRIC, p=config.DISTANCE_P`` (ADR-009).

    Vì sao CV lại dùng được cho bài toán unsupervised: nhãn cụm do K-Means sinh ra
    được coi như target của một bài toán classification phụ. Accuracy cao ⇒ ranh giới
    cụm nhất quán và tổng quát hoá được, không phải sản phẩm của một lần khởi tạo may mắn.

    ⚠️ Đây KHÔNG phải bằng chứng cụm "đúng" — nhãn vốn do chính K-Means tạo ra.
    Bằng chứng về ý nghĩa thực tế nằm ở ``evaluate.py`` (external validation).
    """
    raise NotImplementedError("T5.5a @loc")


def stability_summary(cv_result: pd.DataFrame) -> dict:
    """Chọn k_neighbors tốt nhất + accuracy ± std tương ứng. T6.1."""
    raise NotImplementedError("T6.1 @loc")
