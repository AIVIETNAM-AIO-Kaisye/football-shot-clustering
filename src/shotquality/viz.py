"""Hàm vẽ dùng chung — CHỦ SỞ HỮU: C (branch `eval-eng`).

Task T6.0. A và B **gọi** các hàm này để mọi figure trong report cùng một style;
không ai tự vẽ kiểu riêng.

Quy ước lưu file: ``reports/figures/{owner}_{task}_{name}.png``
ví dụ ``A_t3_shot_heatmap.png``, ``B_t5_elbow_scaled.png``.
"""

from __future__ import annotations

import pandas as pd

from . import config

# Bảng màu cố định theo cluster_id — dùng chung mọi figure để người đọc
# nhận ra cùng một cụm giữa các biểu đồ khác nhau.
CLUSTER_PALETTE = [
    "#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
    "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD",
]


def plot_elbow(curve: pd.DataFrame, title: str, out_path) -> None:
    """Đường cong inertia theo k, đánh dấu điểm khuỷu tay. T6.0."""
    raise NotImplementedError("T6.0 @C")


def plot_silhouette(sil: pd.DataFrame, title: str, out_path) -> None:
    """Silhouette trung bình theo k. T6.0."""
    raise NotImplementedError("T6.0 @C")


def plot_gap(gap_df: pd.DataFrame, title: str, out_path) -> None:
    """Gap statistic kèm error bar ``s_k``. T6.0."""
    raise NotImplementedError("T6.0 @C")


def plot_shots_on_pitch(df: pd.DataFrame, out_path, hue: str | None = None) -> None:
    """Scatter shot trên sơ đồ sân (``mplsoccer``). T3.2 / T6.0.

    ``hue="cluster_id"`` để tô màu theo cụm — đây là figure trực quan nhất
    cho phần kết quả của report.
    """
    raise NotImplementedError("T6.0 @C")


def plot_shot_heatmap(df: pd.DataFrame, out_path) -> None:
    """Heatmap mật độ sút trên sơ đồ sân. T3.2."""
    raise NotImplementedError("T6.0 @C")


def plot_knn_tuning(cv_result: pd.DataFrame, out_path) -> None:
    """Accuracy ± std theo ``k_neighbors``. T5.5b."""
    raise NotImplementedError("T6.0 @C")
