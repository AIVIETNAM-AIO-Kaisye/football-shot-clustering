"""Thống kê mô tả (Task 2) — CHỦ SỞ HỮU: Phong (branch `data-eng`)."""

from __future__ import annotations

import pandas as pd

from . import config


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """min/max/mean/std/median cho toàn bộ cột numeric. T2.1."""
    raise NotImplementedError("T2.1 @phong")


def outcome_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Phân bố ``shot_outcome`` (đếm + %). T2.2.

    Đối chiếu: World Cup 2018 (1.304 shot hợp lệ) — goal rate 7,5%,
    Off T 397 · Blocked 386 · Saved 310 · Goal 98 · Wayward 81 · Post 24.
    """
    raise NotImplementedError("T2.2 @phong")


def categorical_distribution(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Phân bố ``body_part``, ``technique``, ``shot_type``. T2.3.

    ⚠️ ``body_part == "Other"`` chỉ có 7 shot ở World Cup 2018 → quá ít để one-hot riêng;
    cột gần như toàn 0 chỉ làm nhiễu khoảng cách L2. Đề xuất gộp hoặc bỏ.
    """
    raise NotImplementedError("T2.3 @phong")


def sample_balance(df: pd.DataFrame) -> pd.DataFrame:
    """Số shot theo đội / theo trận → phát hiện lệch mẫu. T2.4."""
    raise NotImplementedError("T2.4 @phong")


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    """Bảng missing values từng cột (đếm + %). T2.5."""
    raise NotImplementedError("T2.5 @phong")


def feature_scale_table(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """Bảng so sánh scale giữa các feature. T3.3.

    🎯 Đây là **bằng chứng định lượng** biện minh cho toàn bộ thí nghiệm
    scaled vs unscaled — bảng này bắt buộc phải có trong report.
    Kỳ vọng thấy: ``distance_to_goal`` (0–120) áp đảo ``angle_to_goal`` (0–π)
    và các boolean (0–1) khi tính khoảng cách L2.
    """
    raise NotImplementedError("T3.3 @phong")
