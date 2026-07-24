"""Đọc/ghi file dùng chung — CHỦ SỞ HỮU: Phong (branch `data-eng`).

Mọi thao tác I/O đi qua đây để thống nhất encoding — tên cầu thủ có dấu
(Pavel Šulc, João Cancelo, Rúben Dias) rất dễ vỡ nếu mỗi người tự mở file.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from . import config


def read_json(path: Path) -> dict | list:
    """Đọc JSON với ``encoding="utf-8"`` — không dùng encoding mặc định của Windows."""
    raise NotImplementedError("T1.1 @phong")


def fetch_json(url: str, retries: int = 3, timeout: int = 60) -> dict | list:
    """Tải JSON từ open-data, có retry + backoff."""
    raise NotImplementedError("T1.1 @phong")


def save_csv(df: pd.DataFrame, path: Path) -> None:
    """Ghi CSV với ``config.CSV_ENCODING`` (utf-8-sig) và ``index=False``.

    utf-8-sig để Excel mở không vỡ chữ có dấu.
    """
    raise NotImplementedError("T1.1 @phong")


def load_csv(path: Path) -> pd.DataFrame:
    """Đọc CSV do project sinh ra, đúng encoding."""
    raise NotImplementedError("T1.1 @phong")


def ensure_dirs() -> None:
    """Tạo sẵn các thư mục output trong ``config`` nếu chưa có."""
    raise NotImplementedError("T1.1 @phong")
