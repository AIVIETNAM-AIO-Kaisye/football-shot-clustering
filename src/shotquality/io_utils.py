"""Đọc/ghi file dùng chung — CHỦ SỞ HỮU: Phong (branch `data-eng`).

Mọi thao tác I/O đi qua đây để thống nhất encoding — tên cầu thủ có dấu
(Pavel Šulc, João Cancelo, Rúben Dias) rất dễ vỡ nếu mỗi người tự mở file.
"""

from __future__ import annotations

import json
from pathlib import Path
import urllib.request
import time

import pandas as pd

from . import config


def read_json(path: Path) -> dict | list:
    """Đọc JSON với ``encoding="utf-8"`` — không dùng encoding mặc định của Windows."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_json(url: str, retries: int = 3, timeout: int = 60) -> dict | list:
    """Tải JSON từ open-data, có retry + backoff."""
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            if i == retries - 1:
                raise e
            time.sleep(2 ** i)
    return {}


def save_csv(df: pd.DataFrame, path: Path) -> None:
    """Ghi CSV với ``config.CSV_ENCODING`` (utf-8-sig) và ``index=False``.

    utf-8-sig để Excel mở không vỡ chữ có dấu.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding=config.CSV_ENCODING)


def load_csv(path: Path) -> pd.DataFrame:
    """Đọc CSV do project sinh ra, đúng encoding."""
    return pd.read_csv(path)


def ensure_dirs() -> None:
    """Tạo sẵn các thư mục output trong ``config`` nếu chưa có."""
    config.DATA_RAW.mkdir(parents=True, exist_ok=True)
    config.DATA_INTERIM.mkdir(parents=True, exist_ok=True)
    config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    config.REPORTS.mkdir(parents=True, exist_ok=True)
    config.FIGURES.mkdir(parents=True, exist_ok=True)
    config.TABLES.mkdir(parents=True, exist_ok=True)
