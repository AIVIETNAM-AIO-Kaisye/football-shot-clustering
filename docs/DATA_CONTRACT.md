# Data Contract — `shots_raw.csv`

> **Trạng thái:** 🟡 DRAFT — sẽ chuyển thành 🔒 **FROZEN** tại GATE 1 (cuối Ngày 1).
> Sau khi FROZEN, mọi thay đổi phải qua PR có **1 approve** và ghi vào `DECISIONS.md`.

Đây là **giao diện chung** giữa 3 thành viên. B và C code dựa trên bản hợp đồng này mà **không cần chờ**
A chạy xong ingest — đó là lý do Ngày 2–3 chạy song song được.

## 1. Nguồn & bộ lọc

| | |
|---|---|
| Nguồn | `https://raw.githubusercontent.com/hudl/open-data/master/data/events/{match_id}.json` |
| Giải | Euro 2024 (`comp=55, season=282`) + World Cup 2022 (`comp=43, season=106`) |
| Lọc event | `type.name == "Shot"` |
| **Loại bỏ** | `shot.type.name == "Penalty"` **và** `period == 5` (luân lưu) |
| Số dòng kỳ vọng | **2.500 – 2.700** |

## 2. Schema

### 2.1 Nhóm ID — dùng để join, **không** đưa vào model

| Cột | Dtype | Nguồn JSON | Ghi chú |
|---|---|---|---|
| `shot_id` | str | `id` | UUID, khoá chính |
| `match_id` | int | *tên file* | ⚠️ **không có trong event** — lấy từ filename |
| `competition_id` | int | — | gán thủ công theo vòng lặp |
| `season_id` | int | — | gán thủ công |
| `team_id` / `team_name` | int / str | `team.*` | |
| `player_id` / `player_name` | int / str | `player.*` | ⚠️ có dấu tiếng nước ngoài |
| `period` | int | `period` | |
| `minute` / `second` | int | `minute`, `second` | |
| `play_pattern` | str | `play_pattern.name` | From Corner / From Free Kick / Regular Play… |
| `position_name` | str | `position.name` | |

### 2.2 Nhóm X — feature ứng viên cho K-Means

| Cột | Dtype | Nguồn / công thức | Chủ |
|---|---|---|---|
| `x` | float | `location[0]` | A |
| `y` | float | `location[1]` | A |
| `distance_to_goal` | float | `hypot(120 − x, 40 − y)` | B |
| `angle_to_goal` | float | góc chắn bởi **2 cột dọc** (xem §4) | B |
| `under_pressure` | int 0/1 | `under_pressure` → **fillna(0)** | A |
| `body_part` | str | `shot.body_part.name` | A |
| `technique` | str | `shot.technique.name` | A |
| `shot_type` | str | `shot.type.name` | A |
| `first_time` | int 0/1 | `shot.first_time` → **fillna(0)** | A |
| `one_on_one` | int 0/1 | `shot.one_on_one` → **fillna(0)** | A |
| `open_goal` | int 0/1 | `shot.open_goal` → **fillna(0)** | A |
| `follows_dribble` | int 0/1 | `shot.follows_dribble` → **fillna(0)** | A |
| `aerial_won` | int 0/1 | `shot.aerial_won` → **fillna(0)** | A |
| `n_defenders_in_cone` | int | từ `shot.freeze_frame` (xem §5) | C |
| `n_opponents_within_3y` | int | từ `shot.freeze_frame` | C |
| `gk_x` / `gk_y` | float | vị trí GK đối phương trong freeze_frame | C |
| `gk_dist_to_goal` | float | `hypot(120 − gk_x, 40 − gk_y)` | C |

### 2.3 Nhóm Y_hidden — 🚫 **CẤM đưa vào K-Means/KNN**

Chỉ dùng ở Task 6 để external validation. Lưu **cùng file** nhưng `preprocess.py` phải tách ra ngay.

| Cột | Dtype | Nguồn | Vì sao phải giấu |
|---|---|---|---|
| `shot_outcome` | str | `shot.outcome.name` | là kết quả → data leakage |
| `is_goal` | int 0/1 | `outcome == "Goal"` | nhãn thật |
| `statsbomb_xg` | float | `shot.statsbomb_xg` | model xG đã học từ chính các feature này |
| `end_x` / `end_y` / `end_z` | float | `shot.end_location` | vị trí bóng **sau** khi sút → leakage |

## 3. ⚠️ Bốn cạm bẫy bắt buộc xử lý

**① Boolean chỉ tồn tại khi `True`.**
Đo thực tế trên Euro 2024 (1.304 shot hợp lệ): `under_pressure` chỉ có ở **387** dòng, `first_time` **380**,
`one_on_one` **52**, `open_goal` **9**. `pd.json_normalize` sẽ sinh `NaN` → **bắt buộc `.fillna(0).astype(int)`**.
Quên bước này sẽ mất ~70% dữ liệu khi `dropna()`.

**② Penalty tạo cụm suy biến.**
36 penalty + 24 quả luân lưu trong Euro 2024, tất cả ở **cùng một toạ độ**, xG cố định ~0.78.
K-Means sẽ dành hẳn 1 cụm cho chúng → hỏng cả Elbow lẫn Silhouette. **Phải lọc bỏ.**

**③ `match_id` không nằm trong events JSON.** Lấy từ tên file.

**④ Encoding.** Tên cầu thủ có dấu (Pavel Šulc, João Cancelo, Rúben Dias).
Đọc: `open(path, encoding="utf-8")`. Ghi: `to_csv(..., encoding="utf-8-sig")` để Excel không vỡ chữ.

## 4. Công thức `angle_to_goal`

Không dùng góc tới tâm khung thành. Dùng **góc chắn bởi hai cột dọc** — đây là feature chuẩn trong mô hình xG:

```
P₁ = (120, 36)      cột trái
P₂ = (120, 44)      cột phải
S  = (x, y)         vị trí sút

a = |S − P₁|,  b = |S − P₂|,  c = 8   (bề ngang khung thành, đơn vị yard)

angle_to_goal = arccos( (a² + b² − c²) / (2ab) )      # radian, ∈ (0, π)
```

Góc càng lớn ⇒ khung thành càng "mở" ⇒ cơ hội càng tốt. Sút từ sát biên ngang cho góc ≈ 0.

> **Đơn vị:** toạ độ StatsBomb tính bằng **yard** trên sân chuẩn hoá 120 × 80 (không phải mét).

## 5. Quy ước đọc `shot.freeze_frame`

Mỗi phần tử: `{location: [x, y], player: {...}, position: {...}, teammate: bool}`.

- **Đối phương** = `teammate == false`. Thủ môn nhận biết qua `position.name == "Goalkeeper"`.
- `n_defenders_in_cone` = số đối phương (trừ GK) nằm trong tam giác `S · P₁ · P₂`.
- `n_opponents_within_3y` = số đối phương cách điểm sút ≤ 3 yard.
- Nếu không tìm thấy GK đối phương → `gk_x = gk_y = NaN`, `gk_dist_to_goal = NaN`. Xử lý ở Task 4.3.

Đo thực tế: **100%** shot của Euro 2024 có `freeze_frame` (1304/1304) → **không cần 360 data**.

## 6. Nhật ký thay đổi hợp đồng

| Ngày | Thay đổi | Người | ADR |
|---|---|---|---|
| D1 | Bản đầu tiên | LEAD | ADR-001 |
| | *(EDA của A ở Ngày 2 có thể đề xuất bỏ feature dư thừa — ghi vào đây)* | | |
