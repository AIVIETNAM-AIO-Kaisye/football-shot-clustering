# Cấu trúc thư mục & Ma trận sở hữu

> **Nguyên tắc vàng chống conflict:** mỗi file có **đúng một** chủ sở hữu.
> Muốn sửa file của người khác → mở PR, không tự commit đè.

## 1. Bản đồ thư mục

```
shot-quality-clustering/
├── README.md                     [SHARED]  giới thiệu, quickstart
├── requirements.txt              [SHARED]  đóng băng phiên bản
├── .gitignore                    [SHARED]
│
├── docs/
│   ├── PLAN.md                   [LEAD]    kế hoạch 4 ngày
│   ├── STRUCTURE.md              [LEAD]    file này
│   ├── WORKFLOW.md               [LEAD]    quy ước git + tag kanban
│   ├── STATE.md                  [LEAD]    trạng thái, cập nhật mỗi standup
│   ├── DECISIONS.md              [LEAD]    nhật ký ADR
│   ├── DATA_CONTRACT.md          [SHARED]  schema — ĐÓNG BĂNG cuối Ngày 1
│   └── board/
│       ├── BOARD.md              [LEAD]    tổng quan kanban
│       ├── A_data.md             [A]       ⬅ chỉ A sửa
│       ├── B_model.md            [B]       ⬅ chỉ B sửa
│       └── C_eval.md             [C]       ⬅ chỉ C sửa
│
├── data/
│   ├── raw/                      [gitignored] events JSON tải về (~350 MB)
│   ├── interim/shots_raw.csv     [A tạo]   artifact chung Ngày 1
│   └── processed/                          X_scaled, X_unscaled, labels_*
│
├── src/shotquality/
│   ├── __init__.py               [SHARED]
│   ├── config.py                 [SHARED]  ⚠ hằng số chung — đổi phải báo cả nhóm
│   ├── io_utils.py               [A]       đọc/ghi file, đường dẫn
│   ├── ingest.py                 [A]       tải + lọc + làm phẳng shot event
│   ├── descriptive.py            [A]       Task 2 — thống kê mô tả
│   ├── features.py               [B]       distance/angle/one-hot
│   ├── preprocess.py             [B]       Task 4 — tách X/Y_hidden, scaler
│   ├── clustering.py             [B]       Task 5 — K-Means runner
│   ├── selection.py              [B]       Elbow + Silhouette
│   ├── freeze_frame.py           [C]       đếm hậu vệ trong nón sút
│   ├── selection_gap.py          [C]       Gap Statistic
│   ├── validation.py             [C]       ARI + KNN k-fold CV
│   ├── evaluate.py               [C]       Task 6 — validate bằng field giấu
│   └── viz.py                    [C]       toàn bộ hàm vẽ
│
├── scripts/                      CLI mỏng, chỉ gọi src/
│   ├── 01_download.py            [A]
│   ├── 02_extract_shots.py       [A]
│   ├── 03_descriptive.py         [A]
│   ├── 04_preprocess.py          [B]
│   ├── 05_cluster.py             [B]
│   ├── 06_validate.py            [C]
│   └── 07_report.py              [C]
│
├── notebooks/                    mỗi người 1 notebook riêng → 0 conflict
│   ├── A_eda.ipynb               [A]
│   ├── B_modeling.ipynb          [B]
│   └── C_evaluation.ipynb        [C]
│
├── reports/
│   ├── figures/                  quy ước tên: {owner}_{task}_{name}.png
│   └── final_report.md           [C]
│
└── tests/
    ├── test_features.py          [B]
    ├── test_freeze_frame.py      [C]
    └── test_validation.py        [C]
```

## 2. Ma trận sở hữu (quick reference)

| Chủ sở hữu | Được commit trực tiếp vào |
|---|---|
| **A** | `io_utils.py` · `ingest.py` · `descriptive.py` · `scripts/01,02,03` · `notebooks/A_*` · `docs/board/A_data.md` · `figures/A_*` |
| **B** | `features.py` · `preprocess.py` · `clustering.py` · `selection.py` · `scripts/04,05` · `tests/test_features.py` · `notebooks/B_*` · `docs/board/B_model.md` · `figures/B_*` |
| **C** | `freeze_frame.py` · `selection_gap.py` · `validation.py` · `evaluate.py` · `viz.py` · `scripts/06,07` · `tests/test_freeze_frame.py` · `tests/test_validation.py` · `notebooks/C_*` · `docs/board/C_eval.md` · `figures/C_*` · `final_report.md` |
| **LEAD** | toàn bộ `docs/*.md` (trừ `DATA_CONTRACT.md`) |
| **SHARED** | `config.py` · `DATA_CONTRACT.md` · `requirements.txt` · `README.md` → **bắt buộc PR + 1 approve** |

## 3. Ba quy tắc chống conflict

**① Notebook không bao giờ dùng chung.**
File `.ipynb` là JSON có output nhúng — git gần như luôn conflict. Mỗi người một notebook riêng,
và **logic thật phải nằm trong `src/`**, notebook chỉ gọi hàm + hiển thị.

**② Kanban tách file theo người.**
Nếu 3 người cùng sửa một `KANBAN.md` thì conflict mỗi lần cập nhật trạng thái. Vì vậy board được
tách thành `A_data.md` / `B_model.md` / `C_eval.md` — mỗi người chỉ sửa file của mình.

**③ Không hai người cùng sửa một module.**
Ví dụ Ngày 3 cả A và B đều chạy K-Means, nhưng **chỉ B sửa `clustering.py`**; A chỉ *gọi* hàm đó
từ notebook của mình. Lợi ích kép: không conflict, và hai nhánh thí nghiệm dùng chung một code path
→ khác biệt kết quả chắc chắn đến từ scaling chứ không phải do implementation khác nhau.

## 4. Quy ước đặt tên output

| Loại | Mẫu | Ví dụ |
|---|---|---|
| Figure | `{owner}_{task}_{name}.png` | `A_t3_shot_heatmap.png` |
| Bảng kết quả | `reports/tables/{task}_{name}.csv` | `t5_k_selection_summary.csv` |
| Nhãn cụm | `data/processed/labels_{arm}.csv` | `labels_scaled.csv` |
