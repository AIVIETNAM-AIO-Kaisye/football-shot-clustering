# Board — Thông · ML Engineer

**Branch:** `ml-eng` · **WIP limit:** 2 thẻ `#doing`
**File được commit trực tiếp:** `features.py` · `preprocess.py` · `clustering.py` · `selection.py` · `scripts/04,05` · `tests/test_features.py` · `notebooks/thong_modeling.ipynb` · `figures/thong_*` · file này

---

## NGÀY 1 — Geometry features *(GATE 1)*

- [ ] **T1.3a** `@thong` `#data` `#p0` `#todo` — `distance_to_goal` `est 1h`
      ↳ `hypot(120 − x, 40 − y)`, đơn vị **yard** (không phải mét)

- [ ] **T1.3b** `@thong` `#data` `#p0` `#todo` — `angle_to_goal` bằng định lý cosin `est 2.5h`
      ↳ 2 cột dọc `P₁=(120,36)`, `P₂=(120,44)`, `c = 8`
      ↳ `angle = arccos((a² + b² − c²) / (2ab))` — xem `DATA_CONTRACT.md` §4
      ↳ ⚠️ **không** dùng góc tới tâm khung `(120,40)` — xem ADR-007
      ↳ ⚠️ chặn chia 0 khi sút từ ngay trên vạch cầu môn

- [ ] **T1.3c** `@thong` `#data` `#p1` `#todo` — Unit test cho geometry `est 1.5h`
      ↳ out: `tests/test_features.py`
      ↳ case: chấm phạt đền (108, 40) · sút sát biên ngang → góc ≈ 0 · sút chính diện gần → góc lớn nhất

- [ ] **T1.3d** `@thong` `#data` `#p1` `#todo` — Helper one-hot dùng chung `est 1h`
      ↳ note: `drop_first=False` để cụm dễ diễn giải; cố định thứ tự cột để 3 máy ra giống nhau

---

## NGÀY 2 — Preprocessing + thư viện K-Means *(GATE 2)*

- [ ] **T4.1** `@thong` `#model` `#p0` `#todo` — Tách 3 nhóm cột `X` / `Y_hidden` / `ID` `est 1h`
      ↳ ⚠️ `Y_hidden` gồm cả `end_x/end_y/end_z` — dễ quên, xem ADR-006
      ↳ out: `data/processed/y_hidden.csv`

- [ ] **T4.2** `@thong` `#model` `#p0` `#todo` — One-hot `body_part`, `technique`, `shot_type` `est 1h`

- [ ] **T4.3** `@thong` `#model` `#p1` `#todo` — Xử lý missing `est 1h`
      ↳ ghi rõ **số dòng bị ảnh hưởng** vào `DECISIONS.md`
      ↳ note: `gk_*` thiếu khi freeze_frame không có GK — quyết định impute hay bỏ cột

- [ ] **T4.4** `@thong` `#model` `#p0` `#todo` — `StandardScaler` → 2 phiên bản X `est 1.5h`
      ↳ out: `data/processed/X_scaled.csv` + `X_unscaled.csv` ← artifact GATE 2
      ↳ ⚠️ ghi rõ scaler fit trên toàn bộ hay chỉ train — nêu cách tránh leakage trong report

- [ ] **T4.5** `@thong` `#model` `#p1` `#todo` — Lưu file kèm `shot_id` để join ngược `Y_hidden` `est 0.5h`
      ↳ check: 2 file cùng số dòng, cùng thứ tự

- [ ] **T5.0a** `@thong` `#model` `#p0` `#todo` — `clustering.py`: runner K-Means quét k `est 1.5h`
      ↳ `run_kmeans_sweep(X, k_range) -> {k: (labels, inertia, model)}`
      ↳ ⚠️ API này **Phong cũng dùng** ở D3 → đóng băng chữ ký hàm, đổi phải báo Phong

- [ ] **T5.0b** `@thong` `#model` `#p0` `#todo` — `selection.py`: Elbow + Silhouette `est 1.5h`
      ↳ `elbow_curve()`, `silhouette_by_k()`, `suggest_k_elbow()` (knee detection)

---

## NGÀY 3 — Nhánh SCALED + so sánh *(GATE 3)*

- [ ] **T5.2** `@thong` `#model` `#p0` `#todo` — K-Means trên `X_scaled`, k=2..10, cả 3 phương pháp `est 2.5h`
      ↳ out: `figures/thong_t5_elbow_scaled.png`, `thong_t5_silhouette_scaled.png`, `thong_t5_gap_scaled.png`
      ↳ out: `reports/tables/t5_k_selection_scaled.csv`

- [ ] **T5.3** `@thong` `#model` `#p0` `#todo` — Tính **ARI** giữa nhãn scaled và unscaled `est 1h`
      ↳ blocked-by: T5.1d (@phong, nộp 14:00)
      ↳ ⚠️ so sánh ở **cùng một k** thì mới có nghĩa
      ↳ diễn giải: ARI ≈ 0 ⇒ scaling đổi hoàn toàn kết quả · ARI ≈ 1 ⇒ hầu như không đổi

- [ ] **T5.4** `@thong` `#model` `#p0` `#todo` — Chốt phiên bản cụm chính thức `est 1h`
      ↳ out: **`data/processed/labels_scaled.csv`**
      ↳ 🕑 **handoff cho C lúc 14:00** — C cần nhãn này để chạy KNN-CV
      ↳ mặc định chọn bản scaled, trừ khi ARI cho thấy không khác biệt đáng kể

- [ ] **T5.4b** `@thong` `#model` `#p1` `#todo` — Mô tả centroid từng cụm `est 1.5h`
      ↳ out: `reports/tables/t5_centroids.csv` — bảng "cụm này là vùng sút nào"
      ↳ ⚠️ nhớ **inverse_transform** centroid về đơn vị gốc thì mới đọc được

---

## NGÀY 4 — Tích hợp

- [ ] **T7.4** `@thong` `#docs` `#p0` `#todo` — Viết phần *Thiết kế thí nghiệm* + *Preprocessing* cho report `est 2h`
      ↳ nhấn: L2 là **biến kiểm soát**, không phải biến thí nghiệm (ADR-009)

- [ ] **T7.5** `@thong` `#infra` `#p1` `#todo` — Review PR của Phong và Lộc `est 1.5h`

- [ ] **T7.6** `@thong` `#docs` `#p1` `#todo` — Rà lại figures nhánh model, thống nhất bảng màu theo cụm `est 1h`
