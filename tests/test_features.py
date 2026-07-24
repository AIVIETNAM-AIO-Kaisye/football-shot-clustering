"""Test geometry features — CHỦ SỞ HỮU: B. Task T1.3c.

Các test này là **đặc tả** của T1.3: viết trước, implement sau.
Marker ``xfail`` giữ cho ``pytest`` xanh trong lúc chưa implement — khi hàm chạy được,
pytest báo XPASS, đó là tín hiệu để xoá marker.
"""

import math

import pytest

from shotquality import config, features

pytestmark = pytest.mark.xfail(raises=NotImplementedError, reason="T1.3 chưa implement")


def test_distance_at_goal_center_is_zero():
    assert features.distance_to_goal(120.0, 40.0) == pytest.approx(0.0)


def test_distance_from_penalty_spot():
    """Chấm phạt đền StatsBomb ở (108, 40) → cách khung 12 yard."""
    assert features.distance_to_goal(108.0, 40.0) == pytest.approx(12.0)


def test_angle_is_widest_straight_on_close():
    """Sút chính diện gần khung cho góc lớn hơn sút chính diện xa."""
    near = features.angle_to_goal(114.0, 40.0)
    far = features.angle_to_goal(90.0, 40.0)
    assert near > far


def test_angle_near_byline_is_tiny():
    """Sút từ sát biên ngang, ngang hàng cột dọc → góc gần 0."""
    assert features.angle_to_goal(119.0, 2.0) < math.radians(10)


def test_angle_in_valid_range():
    for x, y in [(100, 40), (80, 20), (119, 79), (60, 40)]:
        angle = features.angle_to_goal(float(x), float(y))
        assert 0.0 < angle < math.pi


def test_angle_symmetric_about_pitch_centre():
    """Hai điểm đối xứng qua trục y=40 phải cho cùng một góc."""
    assert features.angle_to_goal(100.0, 30.0) == pytest.approx(
        features.angle_to_goal(100.0, 50.0)
    )


def test_angle_no_division_by_zero_on_goal_line():
    """Sút từ ngay trên vạch cầu môn không được raise."""
    features.angle_to_goal(120.0, 36.0)


def test_one_hot_column_order_is_stable():
    """Thứ tự cột phải giống nhau giữa các lần chạy → kết quả tái lập được."""
    import pandas as pd

    df1 = pd.DataFrame({"body_part": ["Head", "Right Foot", "Left Foot"]})
    df2 = pd.DataFrame({"body_part": ["Left Foot", "Head", "Right Foot"]})
    assert list(features.one_hot(df1, ["body_part"]).columns) == list(
        features.one_hot(df2, ["body_part"]).columns
    )
