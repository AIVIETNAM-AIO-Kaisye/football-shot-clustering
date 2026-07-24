"""Test ARI + KNN cross-validation — CHỦ SỞ HỮU: C. Task T5.3a, T5.5a.

Toàn bộ test chạy trên dữ liệu synthetic (``make_blobs``) — không phụ thuộc
dữ liệu thật của B. Đây là cơ chế cho phép C làm việc song song ở Ngày 2.
"""

import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import make_blobs

from shotquality import config, validation

pytestmark = pytest.mark.xfail(raises=NotImplementedError, reason="T5.3/T5.5 chưa implement")


@pytest.fixture
def blobs():
    X, y = make_blobs(
        n_samples=600, centers=4, n_features=5,
        cluster_std=1.0, random_state=config.RANDOM_STATE,
    )
    return pd.DataFrame(X, columns=[f"f{i}" for i in range(5)]), y


def test_ari_identical_labels_is_one(blobs):
    _, y = blobs
    assert validation.compare_labelings(y, y) == pytest.approx(1.0)


def test_ari_invariant_to_label_permutation(blobs):
    """Đổi tên nhãn không đổi cách phân hoạch → ARI vẫn = 1.

    Đây là lý do dùng ARI thay vì accuracy khi so hai kết quả clustering.
    """
    _, y = blobs
    permuted = np.where(y == 0, 1, np.where(y == 1, 0, y))
    assert validation.compare_labelings(y, permuted) == pytest.approx(1.0)


def test_ari_random_labels_near_zero(blobs):
    _, y = blobs
    rng = np.random.default_rng(config.RANDOM_STATE)
    assert abs(validation.compare_labelings(y, rng.permutation(y))) < 0.1


def test_knn_cv_returns_one_row_per_grid_value(blobs):
    X, y = blobs
    result = validation.knn_cv(X, y, n_neighbors_grid=[3, 5])
    assert len(result) == 2
    assert {"k_neighbors", "mean_acc", "std_acc"} <= set(result.columns)


def test_knn_cv_high_accuracy_on_separated_blobs(blobs):
    """Blob tách bạch rõ ⇒ accuracy phải rất cao. Kiểm tra harness đúng."""
    X, y = blobs
    result = validation.knn_cv(X, y, n_neighbors_grid=[5])
    assert result["mean_acc"].iloc[0] > 0.95


def test_knn_cv_low_accuracy_on_random_labels(blobs):
    """Nhãn ngẫu nhiên ⇒ accuracy về mức đoán mò (~1/4).

    Test này bảo vệ khỏi bug khiến accuracy luôn cao — nếu thiếu nó, một harness
    hỏng vẫn "chứng minh" được cụm ổn định.
    """
    X, _ = blobs
    rng = np.random.default_rng(config.RANDOM_STATE)
    random_labels = rng.integers(0, 4, size=len(X))
    result = validation.knn_cv(X, random_labels, n_neighbors_grid=[5])
    assert result["mean_acc"].iloc[0] < 0.45
