"""Gap Statistic — CHỦ SỞ HỮU: Lộc (branch `eval-eng`).

Task T5.0c. Tách khỏi ``selection.py`` (của Thông) để hai người không sửa chung file.

⚠️ Đây là thẻ **đầu tiên bị descope** nếu GATE 2 trễ — khi đó
``selection.summarize_k_selection(gap=None)`` vẫn chạy với Elbow + Silhouette.

Tham chiếu: Tibshirani, Walther & Hastie (2001), *Estimating the number of
clusters in a data set via the gap statistic*.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import config


def sample_reference(X: np.ndarray, random_state: int) -> np.ndarray:
    """Sinh một tập tham chiếu ngẫu nhiên. T5.0c.

    Cách đơn giản: uniform trong bounding box từng chiều của X.
    (Bản tinh hơn: sinh trong không gian PCA của X.)
    """
    raise NotImplementedError("T5.0c @loc")


def gap_statistic(
    X: pd.DataFrame,
    k_range=config.K_RANGE,
    n_refs: int = config.GAP_N_REFS,
) -> pd.DataFrame:
    """Tính Gap Statistic. T5.0c — trả DataFrame ``[k, gap, s_k]``.

        gap(k) = mean(log W*_k) − log W_k
        s_k    = sd(log W*_k) · sqrt(1 + 1/n_refs)

    với W_k là within-cluster dispersion.
    """
    raise NotImplementedError("T5.0c @loc")


def suggest_k_gap(gap_df: pd.DataFrame) -> int:
    """k nhỏ nhất thoả ``gap(k) ≥ gap(k+1) − s_{k+1}``. T5.0c."""
    raise NotImplementedError("T5.0c @loc")
