"""Feature engineering hình học — CHỦ SỞ HỮU: Thông (branch `ml-eng`).

Task T1.3. Người khác chỉ *gọi* các hàm này, không sửa file.
Chữ ký hàm đã đóng băng từ Ngày 1 — Phong gọi trong `ingest.py`.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import config


def distance_to_goal(x: float, y: float) -> float:
    """Khoảng cách Euclid từ điểm sút tới tâm khung thành (yard).

    T1.3a — dùng ``config.GOAL_CENTER``.
    """
    raise NotImplementedError("T1.3a @thong")


def angle_to_goal(x: float, y: float) -> float:
    """Góc chắn bởi hai cột dọc, nhìn từ điểm sút (radian, ∈ (0, π)).

    T1.3b — định lý cosin với P₁=(120,36), P₂=(120,44), c=8. Xem ADR-007.

        a = |S − P₁|,  b = |S − P₂|
        angle = arccos((a² + b² − c²) / (2ab))

    ⚠️ Không dùng góc tới tâm khung — không phân biệt được sút sát biên ngang
    với sút chính diện ở xa.
    ⚠️ Chặn a·b = 0 (sút từ ngay trên vạch cầu môn).
    """
    raise NotImplementedError("T1.3b @thong")


def add_geometry_features(df: pd.DataFrame) -> pd.DataFrame:
    """Thêm cột ``distance_to_goal`` và ``angle_to_goal`` (vector hoá).

    T1.3 — nhận DataFrame có sẵn cột ``x``, ``y``; trả bản copy đã thêm cột.
    """
    raise NotImplementedError("T1.3 @thong")


def one_hot(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """One-hot encode giữ thứ tự cột ổn định giữa các máy.

    T1.3d — ``drop_first=False`` để cụm dễ diễn giải; sort tên cột sau khi encode
    để 3 máy cho ra cùng thứ tự (điều kiện để kết quả tái lập được).
    """
    raise NotImplementedError("T1.3d @thong")
