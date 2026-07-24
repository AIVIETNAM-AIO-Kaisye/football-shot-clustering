"""Chọn số cụm K: Elbow + Silhouette — CHỦ SỞ HỮU: B (branch `ml-eng`).

Task T5.0b. Gap Statistic nằm ở ``selection_gap.py`` (của C) — tách file để
hai người không sửa chung một module.
"""

from __future__ import annotations

import pandas as pd

from . import config


def elbow_curve(X: pd.DataFrame, k_range=config.K_RANGE) -> pd.DataFrame:
    """Inertia theo k. T5.0b — trả DataFrame ``[k, inertia]``."""
    raise NotImplementedError("T5.0b @B")


def suggest_k_elbow(curve: pd.DataFrame) -> int:
    """Dò điểm "khuỷu tay" tự động. T5.0b.

    Gợi ý: phương pháp khoảng cách lớn nhất tới đường thẳng nối
    (k_min, inertia_min) và (k_max, inertia_max) — tránh phán đoán bằng mắt.
    """
    raise NotImplementedError("T5.0b @B")


def silhouette_by_k(X: pd.DataFrame, k_range=config.K_RANGE) -> pd.DataFrame:
    """Silhouette trung bình theo k. T5.0b — trả ``[k, silhouette]``.

    ⚠️ metric = L2 (biến kiểm soát, ADR-009).
    """
    raise NotImplementedError("T5.0b @B")


def summarize_k_selection(
    elbow: pd.DataFrame,
    silhouette: pd.DataFrame,
    gap: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Bảng "3 phương pháp có đồng thuận cùng một k không?". T5.1d / T5.2.

    ``gap=None`` khi Gap Statistic bị descope — bảng vẫn dựng được với 2 phương pháp.

    Note: không đồng thuận **không phải lỗi** — đó là insight cần phân tích
    trong report (mỗi tiêu chí tối ưu một thứ khác nhau).
    """
    raise NotImplementedError("T5.1d @B")
