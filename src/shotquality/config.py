"""Hằng số dùng chung toàn project.

⚠️ FILE [SHARED] — mọi thay đổi phải qua PR + 1 approve và báo cả nhóm.
Không hardcode đường dẫn hay tham số ở nơi khác; lấy hết từ đây.
"""

from pathlib import Path

# ─────────────────────────────────────────────────────────────────────
# Đường dẫn
# ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]

DATA_RAW = ROOT / "data" / "raw"
DATA_INTERIM = ROOT / "data" / "interim"
DATA_PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
TABLES = REPORTS / "tables"

SHOTS_RAW_CSV = DATA_INTERIM / "shots_raw.csv"
MATCH_IDS_JSON = DATA_INTERIM / "match_ids.json"
X_SCALED_CSV = DATA_PROCESSED / "X_scaled.csv"
X_UNSCALED_CSV = DATA_PROCESSED / "X_unscaled.csv"
Y_HIDDEN_CSV = DATA_PROCESSED / "y_hidden.csv"
LABELS_SCALED_CSV = DATA_PROCESSED / "labels_scaled.csv"
LABELS_UNSCALED_CSV = DATA_PROCESSED / "labels_unscaled.csv"

# ─────────────────────────────────────────────────────────────────────
# Nguồn dữ liệu — ADR-001, ADR-002
# ─────────────────────────────────────────────────────────────────────
OPEN_DATA_BASE = "https://raw.githubusercontent.com/hudl/open-data/master/data"

# (competition_id, season_id, tên gọi)
COMPETITIONS = [
    (55, 282, "UEFA Euro 2024"),
    (43, 106, "FIFA World Cup 2022"),
]

# ─────────────────────────────────────────────────────────────────────
# Hình học sân bóng StatsBomb — đơn vị YARD (không phải mét)
# ─────────────────────────────────────────────────────────────────────
PITCH_LENGTH = 120.0
PITCH_WIDTH = 80.0

GOAL_CENTER = (120.0, 40.0)
GOAL_POST_LEFT = (120.0, 36.0)
GOAL_POST_RIGHT = (120.0, 44.0)
GOAL_WIDTH = 8.0

NEAR_OPPONENT_RADIUS = 3.0  # yard — ngưỡng cho n_opponents_within_3y

# ─────────────────────────────────────────────────────────────────────
# Bộ lọc shot — ADR-004
# ─────────────────────────────────────────────────────────────────────
EXCLUDE_SHOT_TYPES = ("Penalty",)
EXCLUDE_PERIODS = (5,)  # loạt luân lưu

# Boolean chỉ xuất hiện trong JSON khi = True → BẮT BUỘC fillna(0)
BOOL_FLAGS = [
    "under_pressure",
    "first_time",
    "one_on_one",
    "open_goal",
    "follows_dribble",
    "aerial_won",
]

# ─────────────────────────────────────────────────────────────────────
# Nhóm cột — ADR-006. Chốt lại lần cuối ở T3.6 (@phong).
# ─────────────────────────────────────────────────────────────────────
ID_COLS = [
    "shot_id", "match_id", "competition_id", "season_id",
    "team_id", "team_name", "player_id", "player_name",
    "period", "minute", "second", "play_pattern", "position_name",
]

# 🚫 CẤM đưa vào K-Means / KNN
HIDDEN_COLS = [
    "shot_outcome", "is_goal", "statsbomb_xg",
    "end_x", "end_y", "end_z",
]

NUMERIC_FEATURES = [
    "distance_to_goal",
    "angle_to_goal",
    "n_defenders_in_cone",
    "n_opponents_within_3y",
    "gk_dist_to_goal",
]

CATEGORICAL_FEATURES = ["body_part", "technique", "shot_type"]

FEATURE_COLS = NUMERIC_FEATURES + CATEGORICAL_FEATURES + BOOL_FLAGS

# ─────────────────────────────────────────────────────────────────────
# Tham số model — ADR-005, ADR-009
# ─────────────────────────────────────────────────────────────────────
RANDOM_STATE = 42

K_RANGE = range(2, 11)          # số cụm K-Means
KMEANS_N_INIT = 10

GAP_N_REFS = 10                 # số lần lấy mẫu reference cho Gap Statistic

CV_FOLDS = 5
KNN_NEIGHBORS_GRID = [3, 5, 7, 9]
DISTANCE_METRIC = "minkowski"   # p=2 ⇒ Euclidean/L2 — BIẾN KIỂM SOÁT
DISTANCE_P = 2

CSV_ENCODING = "utf-8-sig"      # để Excel đọc đúng tên có dấu
