"""Tiền xử lý cho model — CHỦ SỞ HỮU: B (branch `ml-eng`).

Task T4. Sản phẩm: hai phiên bản X (scaled / unscaled) + Y_hidden tách riêng.
"""

from __future__ import annotations

import pandas as pd

from . import config


def split_column_groups(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Tách thành ``(X, y_hidden, ids)``. T4.1 — ADR-006.

    ⚠️ ``y_hidden`` gồm cả ``end_x/end_y/end_z`` — vị trí bóng SAU khi sút,
    cũng là leakage. Rất hay bị quên.
    """
    raise NotImplementedError("T4.1 @B")


def encode_categoricals(X: pd.DataFrame) -> pd.DataFrame:
    """One-hot ``config.CATEGORICAL_FEATURES``. T4.2.

    Note: EDA của A (T2.3) có thể đề xuất gộp ``body_part == "Other"``
    (chỉ 7 shot ở Euro 2024) để tránh cột gần như toàn 0 làm nhiễu khoảng cách L2.
    """
    raise NotImplementedError("T4.2 @B")


def handle_missing(X: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Xử lý missing, trả ``(X_sạch, báo_cáo)``. T4.3.

    ``báo_cáo`` phải ghi số dòng/cột bị ảnh hưởng để đưa vào DECISIONS.md.
    Chú ý ``gk_*`` NaN khi freeze_frame không có GK.
    """
    raise NotImplementedError("T4.3 @B")


def make_scaled_unscaled(X: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Trả ``(X_unscaled, X_scaled)`` — cùng index, cùng thứ tự cột. T4.4.

    ⚠️ Ghi rõ trong report: scaler fit trên toàn bộ dữ liệu hay chỉ trên train,
    và vì sao cách đó không gây leakage trong bối cảnh unsupervised.
    """
    raise NotImplementedError("T4.4 @B")


def save_all(X_unscaled, X_scaled, y_hidden, ids) -> None:
    """Ghi ra ``config.DATA_PROCESSED`` kèm ``shot_id`` để join ngược. T4.5.

    Check: hai file X cùng số dòng, cùng thứ tự.
    """
    raise NotImplementedError("T4.5 @B")
