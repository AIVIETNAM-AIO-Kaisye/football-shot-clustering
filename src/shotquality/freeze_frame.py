"""Phân tích ``shot.freeze_frame`` — CHỦ SỞ HỮU: Lộc (branch `eval-eng`).

Task T1.4. Phong gọi các hàm này trong `ingest.py` — chữ ký đóng băng từ Ngày 1.

Ghi chú: ``freeze_frame`` nằm ngay trong event Shot, KHÔNG cần 360 data (ADR-008).
Đo thực tế: Euro 2024 có 1304/1304 shot chứa freeze_frame.
"""

from __future__ import annotations

from typing import Any

from . import config

FreezeFrame = list[dict[str, Any]]


def split_players(ff: FreezeFrame) -> tuple[list[dict], list[dict], dict | None]:
    """Tách freeze_frame thành (đồng đội, đối phương ngoài GK, GK đối phương).

    T1.4a — đối phương là ``teammate == False``; GK nhận qua
    ``position.name == "Goalkeeper"``.

    ⚠️ Lỗi kinh điển: đếm nhầm đồng đội thành hậu vệ chắn.
    Trả về ``None`` cho GK nếu không tìm thấy.
    """
    raise NotImplementedError("T1.4a @loc")


def point_in_triangle(p, a, b, c) -> bool:
    """Kiểm tra điểm ``p`` nằm trong tam giác ``abc``.

    T1.4b — dùng dấu của tích có hướng (cross product) trên cả 3 cạnh:
    cùng dấu ⇒ nằm trong. Điểm nằm đúng trên cạnh tính là **nằm trong**.
    """
    raise NotImplementedError("T1.4b @loc")


def n_defenders_in_cone(ff: FreezeFrame, shot_xy: tuple[float, float]) -> int:
    """Số đối phương (KHÔNG tính GK) nằm trong tam giác S·P₁·P₂.

    T1.4b — nón chắn giữa điểm sút và hai cột dọc.
    """
    raise NotImplementedError("T1.4b @loc")


def n_opponents_within(
    ff: FreezeFrame,
    shot_xy: tuple[float, float],
    radius: float = config.NEAR_OPPONENT_RADIUS,
) -> int:
    """Số đối phương cách điểm sút ≤ ``radius`` yard. T1.4c."""
    raise NotImplementedError("T1.4c @loc")


def goalkeeper_position(ff: FreezeFrame) -> tuple[float, float] | tuple[None, None]:
    """Toạ độ GK đối phương; ``(None, None)`` nếu freeze_frame không có GK.

    T1.4c — giá trị thiếu sẽ thành NaN, do T4.3 (@thong) xử lý.
    """
    raise NotImplementedError("T1.4c @loc")


def extract_all(ff: FreezeFrame, shot_xy: tuple[float, float]) -> dict[str, float]:
    """Gộp toàn bộ feature freeze_frame cho một cú sút.

    T1.4 — trả dict có key: ``n_defenders_in_cone``, ``n_opponents_within_3y``,
    ``gk_x``, ``gk_y``, ``gk_dist_to_goal``.

    Đây là hàm **Phong gọi trong ingest.py** — đừng đổi tên key.
    """
    raise NotImplementedError("T1.4 @loc")
