# Board — C · Evaluation & Report

**Branch:** `eval-eng` · **WIP limit:** 2 thẻ `#doing`
**File được commit trực tiếp:** `freeze_frame.py` · `selection_gap.py` · `validation.py` · `evaluate.py` · `viz.py` · `scripts/06,07` · `tests/test_freeze_frame.py` · `tests/test_validation.py` · `notebooks/C_evaluation.ipynb` · `figures/C_*` · `reports/final_report.md` · file này

---

## NGÀY 1 — Freeze-frame parser *(GATE 1)*

- [ ] **T1.4a** `@C` `#data` `#p0` `#todo` — Parse `shot.freeze_frame`, tách đối phương / đồng đội / GK `est 2h`
      ↳ đối phương = `teammate == false`; GK nhận qua `position.name == "Goalkeeper"`
      ↳ ⚠️ lỗi kinh điển: đếm nhầm đồng đội thành hậu vệ chắn

- [ ] **T1.4b** `@C` `#data` `#p0` `#todo` — `n_defenders_in_cone` — điểm trong tam giác `S·P₁·P₂` `est 2.5h`
      ↳ dùng kiểm tra dấu tích có hướng (sign of cross product) cho 3 cạnh
      ↳ ⚠️ **loại GK ra** khỏi phép đếm này, đếm riêng

- [ ] **T1.4c** `@C` `#data` `#p1` `#todo` — `n_opponents_within_3y` + `gk_x`, `gk_y`, `gk_dist_to_goal` `est 1h`
      ↳ không tìm thấy GK → `NaN`, để T4.3 (@B) xử lý

- [ ] **T1.4d** `@C` `#data` `#p1` `#todo` — Unit test freeze-frame `est 1.5h`
      ↳ out: `tests/test_freeze_frame.py`
      ↳ case: freeze_frame rỗng · không có GK · cầu thủ nằm đúng trên cạnh tam giác
      ↳ note: Euro 2024 có **1304/1304** shot chứa freeze_frame → không cần fallback cho trường hợp thiếu hẳn

---

## NGÀY 2 — Harness kiểm định *(GATE 2)*

> 💡 Toàn bộ ngày này **test trên `sklearn.datasets.make_blobs`**, không chờ `X` thật của B.
> Đây là lý do 3 luồng chạy song song được.

- [ ] **T5.0c** `@C` `#model` `#p1` `#todo` — `selection_gap.py` — Gap Statistic `est 3h`
      ↳ sinh reference distribution uniform trong bounding box của dữ liệu, `B = 10` lần lặp
      ↳ out: `gap_statistic(X, k_range) -> DataFrame[k, gap, s_k]`
      ↳ tiêu chí chọn k: `gap(k) ≥ gap(k+1) − s_{k+1}` (k nhỏ nhất thoả)
      ↳ ⚠️ thẻ này nằm đầu danh sách **descope** nếu trễ GATE 2

- [ ] **T5.5a** `@C` `#eval` `#p0` `#todo` — `validation.py` — KNN + k-fold CV harness `est 2.5h`
      ↳ `knn_cv(X, labels, n_neighbors_grid, cv=5) -> DataFrame[k_neighbors, mean_acc, std_acc]`
      ↳ ⚠️ `StratifiedKFold` — cụm có thể lệch kích thước nhiều
      ↳ ⚠️ metric = L2 (`metric="minkowski", p=2`) — biến kiểm soát, ADR-009

- [ ] **T5.3a** `@C` `#eval` `#p0` `#todo` — Hàm so sánh 2 tập nhãn bằng ARI `est 1h`
      ↳ test: hoán vị nhãn (0↔1) phải cho ARI = 1.0 — chứng minh ARI bất biến với tên nhãn

- [ ] **T6.0** `@C` `#eval` `#p1` `#todo` — `viz.py` — hàm vẽ dùng chung `est 1.5h`
      ↳ `plot_elbow()`, `plot_silhouette()`, `plot_gap()`, `plot_clusters_on_pitch()`
      ↳ cố định bảng màu theo `cluster_id` để mọi figure trong report nhất quán

---

## NGÀY 3 — Kiểm định trên dữ liệu thật *(GATE 3)*

- [ ] **T5.5b** `@C` `#eval` `#p0` `#todo` — Chạy KNN-CV trên nhãn thật, thử `k_neighbors ∈ {3,5,7,9}` `est 2h`
      ↳ blocked-by: T5.4 (@B, handoff 14:00)
      ↳ out: `reports/tables/t5_knn_cv.csv`, `figures/C_t5_knn_tuning.png`

- [ ] **T6.1** `@C` `#eval` `#p0` `#todo` — Tổng hợp accuracy trung bình ± std `est 1h`
      ↳ ⚠️ diễn giải đúng: accuracy cao ⇒ ranh giới cụm **ổn định/tổng quát hoá được**,
        **không** phải bằng chứng cụm "đúng" (nhãn vốn do K-Means sinh ra) — ADR-011

- [ ] **T6.2** `@C` `#eval` `#p0` `#todo` — **External validation bằng field đã giấu** `est 2.5h`
      ↳ join `cluster_id` ↔ `y_hidden.csv`
      ↳ out: bảng `cluster_id · n_shots · dist TB · angle TB · **goal_rate** · **mean_xG**`
      ↳ 🎯 kiểm tra: cụm gần khung/góc mở → goal rate và xG **cùng xếp hạng cao**?
        Nếu thứ tự khớp ⇒ cụm có ý nghĩa thực tế, không chỉ đẹp về hình học

- [ ] **T6.3** `@C` `#eval` `#p1` `#todo` — Bảng tổng hợp scaled vs unscaled (ARI + Silhouette) `est 1h`

---

## NGÀY 4 — Report *(GATE 4)*

- [ ] **T6.4a** `@C` `#docs` `#p0` `#todo` — Viết `reports/final_report.md` `est 3h`
      ↳ bố cục: mục đích → EDA → thiết kế thí nghiệm → kết quả → kết luận + hạn chế
      ↳ 4 bảng bắt buộc: chọn K · ARI+Silhouette · CV accuracy · goal rate/xG theo cụm

- [ ] **T6.4b** `@C` `#docs` `#p0` `#todo` — Phần *Kết luận* `est 1h`
      ↳ trả lời thẳng: pipeline nào (scaled/unscaled, k nào) cho cụm **vừa ổn định** (CV cao)
        **vừa có ý nghĩa thực tế** (khớp xG/goal rate)

- [ ] **T6.4c** `@C` `#docs` `#p1` `#todo` — Phần *Hạn chế* `est 1h`
      ↳ mẫu chỉ từ 2 giải quốc tế → chưa chắc tổng quát cho giải VĐQG
      ↳ `statsbomb_xg` bản thân là output của model khác, không phải ground truth tuyệt đối
      ↳ nếu 3 phương pháp chọn K không đồng thuận → phân tích, **không coi là lỗi**
      ↳ CV chỉ đo tính nhất quán của ranh giới cụm, không đo tính "đúng"
