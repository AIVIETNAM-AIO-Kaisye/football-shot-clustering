"""K-Means runner — CHỦ SỞ HỮU: B (branch `ml-eng`).

Task T5.0a.

⚠️ API trong file này được **A dùng lại** ở Ngày 3 cho nhánh unscaled (ADR-010).
Đóng băng chữ ký hàm; muốn đổi phải báo A trước.

Lợi ích kép của việc dùng chung: không ai sửa file của ai (chống conflict), và
hai nhánh thí nghiệm đi qua cùng một code path nên chênh lệch kết quả chắc chắn
đến từ scaling chứ không phải do implementation khác nhau.
"""

from __future__ import annotations

import pandas as pd

from . import config


def run_kmeans(X: pd.DataFrame, k: int):
    """Chạy K-Means một giá trị k.

    T5.0a — luôn dùng ``config.RANDOM_STATE`` và ``config.KMEANS_N_INIT``
    để kết quả tái lập được trên cả 3 máy (ADR-005).
    Trả ``(labels, inertia, model)``.
    """
    raise NotImplementedError("T5.0a @B")


def run_kmeans_sweep(X: pd.DataFrame, k_range=config.K_RANGE) -> dict[int, tuple]:
    """Quét k, trả ``{k: (labels, inertia, model)}``.

    T5.0a — đây là hàm A gọi ở T5.1a cho nhánh unscaled.
    """
    raise NotImplementedError("T5.0a @B")


def describe_centroids(model, X_unscaled: pd.DataFrame, labels) -> pd.DataFrame:
    """Bảng mô tả centroid từng cụm — "cụm này là vùng sút nào". T5.4b.

    ⚠️ Nếu model fit trên dữ liệu đã chuẩn hoá thì phải ``inverse_transform``
    centroid về đơn vị gốc, nếu không bảng sẽ không đọc được.
    """
    raise NotImplementedError("T5.4b @B")
