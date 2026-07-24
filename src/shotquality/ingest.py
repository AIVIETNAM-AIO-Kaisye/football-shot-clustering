"""Tải và trích xuất shot events — CHỦ SỞ HỮU: Phong (branch `data-eng`).

Task T0.1, T1.1, T1.2, T1.5. Đây là module *điều phối*: nó gọi
``features`` (của Thông) và ``freeze_frame`` (của Lộc) qua interface đã đóng băng
— nhờ vậy cả 3 người code song song được ngay từ Ngày 1.
"""

from __future__ import annotations

import pandas as pd

from . import config, features, freeze_frame


def fetch_match_ids() -> list[dict]:
    """Lấy danh sách match_id của toàn bộ competition trong ``config.COMPETITIONS``.

    T0.1 — đọc ``matches/{competition_id}/{season_id}.json``.
    Trả list dict: ``{match_id, competition_id, season_id}``. Kỳ vọng 115 trận.
    """
    raise NotImplementedError("T0.1 @phong")


def download_events(match_ids: list[int], skip_existing: bool = True) -> None:
    """Tải ``events/{match_id}.json`` về ``config.DATA_RAW``.

    T1.1 — có retry; ``skip_existing=True`` để chạy lại không tải trùng
    (~350 MB, gitignored). Dùng tqdm hiển thị tiến độ.
    """
    raise NotImplementedError("T1.1 @phong")


def is_valid_shot(event: dict) -> bool:
    """Lọc shot hợp lệ. T1.2 — ADR-004.

    Loại ``shot.type.name`` trong ``config.EXCLUDE_SHOT_TYPES`` và
    ``period`` trong ``config.EXCLUDE_PERIODS`` (luân lưu).
    """
    raise NotImplementedError("T1.2 @phong")


def flatten_shot(event: dict, match_id: int, competition_id: int, season_id: int) -> dict:
    """Làm phẳng một shot event thành 1 dòng theo DATA_CONTRACT.

    T1.2 — gọi ``features.add_geometry_features`` (Thông) và
    ``freeze_frame.extract_all`` (Lộc).

    ⚠️ ``match_id`` KHÔNG có trong event → phải truyền từ ngoài vào (tên file).
    ⚠️ Boolean trong ``config.BOOL_FLAGS`` chỉ tồn tại khi True → mặc định 0.
    ⚠️ Nhớ lấy cả ``shot.end_location`` vào nhóm HIDDEN (ADR-006) — dễ quên.
    """
    raise NotImplementedError("T1.2 @phong")


def build_shots_dataframe() -> pd.DataFrame:
    """Duyệt toàn bộ file events → DataFrame theo DATA_CONTRACT. T1.5."""
    raise NotImplementedError("T1.5 @phong")


def sanity_check(df: pd.DataFrame) -> None:
    """Kiểm tra trước GATE 1. T1.5 — raise nếu không đạt.

    - số dòng trong khoảng 2.500–2.700
    - đủ cột theo ``config.ID_COLS + FEATURE_COLS + HIDDEN_COLS``
    - ``x ∈ [0, 120]``, ``y ∈ [0, 80]``
    - các cột trong ``BOOL_FLAGS`` không còn NaN
    - tên cầu thủ có dấu hiển thị đúng (không bị mojibake)
    """
    raise NotImplementedError("T1.5 @phong")
