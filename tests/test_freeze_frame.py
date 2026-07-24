"""Test freeze-frame parser — CHỦ SỞ HỮU: Lộc. Task T1.4d."""

import pytest

from shotquality import freeze_frame

pytestmark = pytest.mark.xfail(raises=NotImplementedError, reason="T1.4 chưa implement")


def _player(x, y, teammate, position="Center Back"):
    return {
        "location": [x, y],
        "player": {"id": 1, "name": "Test"},
        "position": {"id": 1, "name": position},
        "teammate": teammate,
    }


def test_teammates_never_counted_as_defenders():
    """Lỗi kinh điển: đếm nhầm đồng đội thành hậu vệ chắn."""
    ff = [_player(115, 40, teammate=True) for _ in range(5)]
    assert freeze_frame.n_defenders_in_cone(ff, (100.0, 40.0)) == 0


def test_goalkeeper_excluded_from_cone_count():
    """GK đứng chắn nhưng phải đếm riêng, không tính vào n_defenders_in_cone."""
    ff = [_player(118, 40, teammate=False, position="Goalkeeper")]
    assert freeze_frame.n_defenders_in_cone(ff, (100.0, 40.0)) == 0


def test_defender_directly_in_line_is_counted():
    ff = [_player(110, 40, teammate=False)]
    assert freeze_frame.n_defenders_in_cone(ff, (100.0, 40.0)) == 1


def test_defender_far_wide_is_not_counted():
    """Đối phương đứng ngoài nón sút không tính."""
    ff = [_player(110, 5, teammate=False)]
    assert freeze_frame.n_defenders_in_cone(ff, (100.0, 40.0)) == 0


def test_empty_freeze_frame():
    assert freeze_frame.n_defenders_in_cone([], (100.0, 40.0)) == 0


def test_missing_goalkeeper_returns_none():
    ff = [_player(110, 40, teammate=False)]
    assert freeze_frame.goalkeeper_position(ff) == (None, None)


def test_near_opponent_radius():
    ff = [
        _player(101, 40, teammate=False),  # cách 1 yard  → tính
        _player(110, 40, teammate=False),  # cách 10 yard → không
    ]
    assert freeze_frame.n_opponents_within(ff, (100.0, 40.0), radius=3.0) == 1


def test_extract_all_returns_contract_keys():
    """Key phải đúng DATA_CONTRACT — A gọi hàm này trong ingest.py."""
    out = freeze_frame.extract_all([_player(110, 40, teammate=False)], (100.0, 40.0))
    assert set(out) == {
        "n_defenders_in_cone",
        "n_opponents_within_3y",
        "gk_x",
        "gk_y",
        "gk_dist_to_goal",
    }
