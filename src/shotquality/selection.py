"""Chọn số cụm K: Elbow + Silhouette — CHỦ SỞ HỮU: Thông (branch `ml-eng`).

Task T5.0b. Gap Statistic nằm ở ``selection_gap.py`` (của Lộc) — tách file để
hai người không sửa chung một module.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score

from . import config
from .clustering import run_kmeans_sweep


def elbow_curve(X: pd.DataFrame, k_range=config.K_RANGE) -> pd.DataFrame:
    """Inertia theo k. T5.0b — trả DataFrame ``[k, inertia]``."""
    results = run_kmeans_sweep(X, k_range)
    data = [{"k": k, "inertia": res[1]} for k, res in results.items()]
    return pd.DataFrame(data)


def suggest_k_elbow(curve: pd.DataFrame) -> int:
    """Dò điểm "khuỷu tay" tự động. T5.0b.

    Gợi ý: phương pháp khoảng cách lớn nhất tới đường thẳng nối
    (k_min, inertia_min) và (k_max, inertia_max) — tránh phán đoán bằng mắt.
    """
    n_points = len(curve)
    if n_points < 3:
        return curve["k"].iloc[0]
        
    all_coords = curve[["k", "inertia"]].values
    first_point = all_coords[0]
    last_point = all_coords[-1]
    
    line_vec = last_point - first_point
    line_vec_norm = line_vec / np.linalg.norm(line_vec)
    
    vec_from_first = all_coords - first_point
    scalar_proj = np.sum(vec_from_first * line_vec_norm, axis=1)
    
    vec_proj = np.outer(scalar_proj, line_vec_norm)
    vec_to_line = vec_from_first - vec_proj
    dist_to_line = np.linalg.norm(vec_to_line, axis=1)
    
    best_idx = np.argmax(dist_to_line)
    return int(curve["k"].iloc[best_idx])


def silhouette_by_k(X: pd.DataFrame, k_range=config.K_RANGE) -> pd.DataFrame:
    """Silhouette trung bình theo k. T5.0b — trả ``[k, silhouette]``.

    ⚠️ metric = L2 (biến kiểm soát, ADR-009).
    """
    results = run_kmeans_sweep(X, k_range)
    data = []
    for k, (labels, inertia, model) in results.items():
        if k > 1:
            score = silhouette_score(X, labels, metric=config.DISTANCE_METRIC)
        else:
            score = -1.0 # Silhouette not defined for k=1
        data.append({"k": k, "silhouette": score})
    return pd.DataFrame(data)


def summarize_k_selection(
    elbow: pd.DataFrame,
    silhouette: pd.DataFrame,
    gap: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Bảng "3 phương pháp có đồng thuận cùng một k không?". T5.1d / T5.2.

    ``gap=None`` khi Gap Statistic bị descope — bảng vẫn dựng được với 2 phương pháp.

    Note: không đồng thuận **không phải lỗi** — đó là insight cần phân tích
    trong report (mỗi tiêu chí tối ưu một thứ khác nhau).
    """
    df = elbow.merge(silhouette, on="k")
    
    if gap is not None:
        df = df.merge(gap, on="k")
        
    # Highlight suggested K for each method
    best_elbow = suggest_k_elbow(elbow)
    best_silhouette = silhouette.loc[silhouette["silhouette"].idxmax(), "k"]
    
    suggestions = {
        "k": [best_elbow, best_silhouette],
        "method": ["Elbow (Max dist)", "Silhouette (Max score)"]
    }
    
    if gap is not None and "gap_value" in gap.columns:
        # Assuming gap statistic rule: smallest k such that Gap(k) >= Gap(k+1) - s_{k+1}
        # For simplicity in this summary function, if they provide a best_k in gap table, use it
        # or we just mark the max gap
        best_gap = gap.loc[gap["gap_value"].idxmax(), "k"]
        suggestions["k"].append(best_gap)
        suggestions["method"].append("Gap (Max value)")
        
    print("\nSuggested K by method:")
    for m, k in zip(suggestions["method"], suggestions["k"]):
        print(f" - {m}: k={k}")
        
    return df
