"""External validation bằng field đã giấu — CHỦ SỞ HỮU: C (branch `eval-eng`).

Task T6.2, T6.3.

Đây là phần trả lời câu hỏi quan trọng nhất của project: cụm tìm được có ý nghĩa
thực tế không, hay chỉ đẹp về mặt hình học?

- *Internal validation* (Silhouette) — cụm có tách bạch về mặt hình học không?
- *External validation* (module này) — cụm có phản ánh khả năng ghi bàn thật không?

Vì ``outcome`` và ``statsbomb_xg`` chưa từng được đưa vào K-Means (ADR-006), việc
chúng xếp đúng thứ tự giữa các cụm là **bằng chứng độc lập**, không phải hệ quả hiển nhiên.
"""

from __future__ import annotations

import pandas as pd

from . import config


def cluster_profile(
    labels,
    y_hidden: pd.DataFrame,
    X_unscaled: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Bảng kiểm chứng cụm. T6.2.

    Trả DataFrame mỗi dòng một cụm, gồm:
        ``cluster_id · n_shots · mean_distance · mean_angle · goal_rate · mean_xg``

    🎯 Kỳ vọng: cụm gần khung thành / góc mở lớn phải có **cả** goal_rate **và**
    mean_xg cao hơn. Thứ tự khớp ⇒ cụm có ý nghĩa thực tế.
    """
    raise NotImplementedError("T6.2 @C")


def rank_agreement(profile: pd.DataFrame) -> dict:
    """Đo mức khớp thứ hạng giữa ``goal_rate`` và ``mean_xg``. T6.2.

    Gợi ý: Spearman rank correlation giữa hai cột. Trả cả hệ số lẫn kết luận
    dạng chữ để đưa thẳng vào report.
    """
    raise NotImplementedError("T6.2 @C")


def scaling_comparison_table(
    ari: float,
    sil_scaled: float,
    sil_unscaled: float,
    k_scaled: int,
    k_unscaled: int,
) -> pd.DataFrame:
    """Bảng tổng hợp scaled vs unscaled. T6.3."""
    raise NotImplementedError("T6.3 @C")
