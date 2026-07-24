# Board — A · Data Engineer

**Branch:** `data-eng` · **WIP limit:** 2 thẻ `#doing`
**File được commit trực tiếp:** `io_utils.py` · `ingest.py` · `descriptive.py` · `scripts/01,02,03` · `notebooks/A_eda.ipynb` · `figures/A_*` · file này

---

## NGÀY 1 — Ingest *(GATE 1)*

- [ ] **T0.1** `@A` `#data` `#p0` `#todo` — Sinh danh sách `match_id` từ 2 giải `est 1h`
      ↳ out: `data/interim/match_ids.json` (115 trận)
      ↳ note: đọc `matches/55/282.json` + `matches/43/106.json`

- [ ] **T1.1** `@A` `#data` `#p0` `#todo` — Downloader events JSON có retry + resume `est 2h`
      ↳ out: `data/raw/events/{match_id}.json` (~350 MB, gitignored)
      ↳ note: bỏ qua file đã tải để chạy lại được; `tqdm` để theo dõi

- [ ] **T1.2** `@A` `#data` `#p0` `#todo` — Lọc Shot + làm phẳng nhóm ID và boolean flags `est 3h`
      ↳ out: hàm `ingest.flatten_shot()`
      ↳ ⚠️ `fillna(0)` cho `under_pressure`, `first_time`, `one_on_one`, `open_goal`, `follows_dribble`, `aerial_won`
      ↳ ⚠️ `match_id` lấy từ **tên file**, không có trong event
      ↳ ⚠️ loại `shot_type == "Penalty"` và `period == 5`

- [ ] **T1.5** `@A` `#data` `#p0` `#todo` — Chạy end-to-end + sanity check `est 1h`
      ↳ out: **`data/interim/shots_raw.csv`** ← artifact GATE 1
      ↳ check: số dòng 2.500–2.700 · không NaN ngoài dự kiến · `encoding="utf-8-sig"` · tên có dấu hiển thị đúng
      ↳ blocked-by: T1.3 (@B), T1.4 (@C) — cần merge trước 16:00

---

## NGÀY 2 — Thống kê mô tả + EDA

- [ ] **T2.1** `@A` `#eda` `#p1` `#todo` — `describe()` toàn bộ cột numeric `est 1h`
      ↳ out: `reports/tables/t2_describe.csv`

- [ ] **T2.2** `@A` `#eda` `#p1` `#todo` — Phân bố `shot_outcome`, xác nhận mức mất cân bằng `est 0.5h`
      ↳ note: đối chiếu Euro 2024 đo sẵn — goal rate 7,5%

- [ ] **T2.3** `@A` `#eda` `#p2` `#todo` — Phân bố `body_part`, `technique`, `shot_type` `est 0.5h`
      ↳ ⚠️ `body_part == "Other"` chỉ có 7 shot ở Euro 2024 → quá ít để one-hot riêng, đề xuất gộp/bỏ

- [ ] **T2.4** `@A` `#eda` `#p2` `#todo` — Số shot theo đội / theo trận → phát hiện lệch mẫu `est 1h`

- [ ] **T2.5** `@A` `#eda` `#p1` `#todo` — Bảng missing values từng cột `est 0.5h`
      ↳ note: đặc biệt `gk_x/gk_y` khi freeze_frame không có GK

- [ ] **T3.1** `@A` `#eda` `#p1` `#todo` — Validate toạ độ `x ∈ [0,120]`, `y ∈ [0,80]` `est 0.5h`

- [ ] **T3.2** `@A` `#eda` `#p1` `#todo` — Scatter toàn bộ shot + heatmap mật độ trên sơ đồ sân `est 2h`
      ↳ out: `figures/A_t3_shot_scatter.png`, `figures/A_t3_shot_heatmap.png` (dùng `mplsoccer`)

- [ ] **T3.3** `@A` `#eda` `#p0` `#todo` — **Bảng so sánh scale** giữa các feature `est 1h`
      ↳ out: `reports/tables/t3_feature_scales.csv` (min/max/mean/std từng cột)
      ↳ note: đây là **bằng chứng định lượng** biện minh cho thí nghiệm scaled vs unscaled → phải vào report

- [ ] **T3.4** `@A` `#eda` `#p0` `#todo` — Ma trận tương quan giữa feature ứng viên `est 1h`
      ↳ out: `figures/A_t3_corr_matrix.png`
      ↳ note: kỳ vọng `x` ↔ `distance_to_goal` tương quan rất cao → đề xuất bỏ bớt

- [ ] **T3.5** `@A` `#eda` `#p2` `#todo` — Sanity check `distance_to_goal` vs `xG`, `angle_to_goal` vs `xG` `est 0.5h`
      ↳ ⚠️ **chỉ để kiểm tra feature engineering đúng hướng** — KHÔNG dùng xG để chọn feature

- [ ] **T3.6** `@A` `#eda` `#p0` `#todo` — Chốt danh sách feature cuối cùng `est 1h`
      ↳ out: PR sửa `config.FEATURE_COLS` + cập nhật `DATA_CONTRACT.md` §6
      ↳ ⚠️ file `[SHARED]` → cần 1 approve; **báo B ngay trong ngày**

---

## NGÀY 3 — Nhánh UNSCALED

- [ ] **T5.1a** `@A` `#model` `#p0` `#todo` — K-Means trên `X_unscaled`, k=2..10 + Elbow `est 2h`
      ↳ dùng `clustering.run_kmeans_sweep()` của B — **không tự viết lại**
      ↳ out: `figures/A_t5_elbow_unscaled.png`

- [ ] **T5.1b** `@A` `#model` `#p0` `#todo` — Silhouette theo k `est 1h`
      ↳ out: `figures/A_t5_silhouette_unscaled.png`

- [ ] **T5.1c** `@A` `#model` `#p1` `#todo` — Gap Statistic `est 1h`
      ↳ dùng `selection_gap.gap_statistic()` của C
      ↳ blocked-by: C hoàn thành ở D2

- [ ] **T5.1d** `@A` `#model` `#p0` `#todo` — Bảng "3 phương pháp có đồng thuận k không?" `est 1.5h`
      ↳ out: `data/processed/labels_unscaled.csv` + `reports/tables/t5_k_selection_unscaled.csv`
      ↳ 🕑 **nộp trước 14:00** để B tính ARI

---

## NGÀY 4 — Tích hợp

- [ ] **T7.1** `@A` `#infra` `#p0` `#todo` — Chạy lại toàn bộ pipeline từ repo sạch `est 2h`
      ↳ check: số liệu khớp report; nếu lệch → có chỗ chưa cố định `random_state`

- [ ] **T7.2** `@A` `#docs` `#p1` `#todo` — Hoàn thiện figures, thống nhất style/nhãn trục `est 1.5h`

- [ ] **T7.3** `@A` `#docs` `#p1` `#todo` — Review PR của B và C, cấp số liệu EDA cho phần report `est 1.5h`
