# Cấu trúc thư mục & Ma trận sở hữu

> **Nguyên tắc vàng chống conflict:** mỗi file có **đúng một** chủ sở hữu.
> Muốn sửa file của người khác → mở PR, không tự commit đè.

## 1. Bản đồ thư mục

```
football-shot-clustering/
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
│       ├── phong_data.md             [Phong]       ⬅ chỉ A sửa
│       ├── thong_model.md            [Thông]       ⬅ chỉ B sửa
│       └── loc_eval.md             [Lộc]       ⬅ chỉ C sửa
│
├── data/
│   ├── raw/                      [gitignored] events JSON tải về (~350 MB)
│   ├── interim/shots_raw.csv     [A tạo]   artifact chung Ngày 1
│   └── processed/                          X_scaled, X_unscaled, labels_*
│
├── src/shotquality/
│   ├── __init__.py               [SHARED]
│   ├── config.py                 [SHARED]  ⚠ hằng số chung — đổi phải báo cả nhóm
│   ├── io_utils.py               [Phong]       đọc/ghi file, đường dẫn
│   ├── ingest.py                 [Phong]       tải + lọc + làm phẳng shot event
│   ├── descriptive.py            [Phong]       Task 2 — thống kê mô tả
│   ├── features.py               [Thông]       distance/angle/one-hot
│   ├── preprocess.py             [Thông]       Task 4 — tách X/Y_hidden, scaler
│   ├── clustering.py             [Thông]       Task 5 — K-Means runner
│   ├── selection.py              [Thông]       Elbow + Silhouette
│   ├── freeze_frame.py           [Lộc]       đếm hậu vệ trong nón sút
│   ├── selection_gap.py          [Lộc]       Gap Statistic
│   ├── validation.py             [Lộc]       ARI + KNN k-fold CV
│   ├── evaluate.py               [Lộc]       Task 6 — validate bằng field giấu
│   └── viz.py                    [Lộc]       toàn bộ hàm vẽ
│
├── scripts/                      CLI mỏng, chỉ gọi src/
│   ├── 01_download.py            [Phong]
│   ├── 02_extract_shots.py       [Phong]
│   ├── 03_descriptive.py         [Phong]
│   ├── 04_preprocess.py          [Thông]
│   ├── 05_cluster.py             [Thông]
│   ├── 06_validate.py            [Lộc]
│   └── 07_report.py              [Lộc]
│
├── notebooks/                    mỗi người 1 notebook riêng → 0 conflict
│   ├── phong_eda.ipynb               [Phong]
│   ├── thong_modeling.ipynb          [Thông]
│   └── loc_evaluation.ipynb        [Lộc]
│
├── reports/
│   ├── figures/                  quy ước tên: {owner}_{task}_{name}.png
│   └── final_report.md           [Lộc]
│
└── tests/
    ├── test_features.py          [Thông]
    ├── test_freeze_frame.py      [Lộc]
    └── test_validation.py        [Lộc]
```

## 2. Ma trận sở hữu (quick reference)

| Chủ sở hữu | Được commit trực tiếp vào |
|---|---|
| **Phong** | `io_utils.py` · `ingest.py` · `descriptive.py` · `scripts/01,02,03` · `notebooks/phong_*` · `docs/board/phong_data.md` · `figures/phong_*` |
| **Thông** | `features.py` · `preprocess.py` · `clustering.py` · `selection.py` · `scripts/04,05` · `tests/test_features.py` · `notebooks/thong_*` · `docs/board/thong_model.md` · `figures/thong_*` |
| **Lộc** | `freeze_frame.py` · `selection_gap.py` · `validation.py` · `evaluate.py` · `viz.py` · `scripts/06,07` · `tests/test_freeze_frame.py` · `tests/test_validation.py` · `notebooks/loc_*` · `docs/board/loc_eval.md` · `figures/loc_*` · `final_report.md` |
| **LEAD** = Phong | toàn bộ `docs/*.md` (trừ `DATA_CONTRACT.md`) — vai trò LEAD nằm ngoài phần việc Data Engineer |
| **SHARED** | `config.py` · `DATA_CONTRACT.md` · `requirements.txt` · `README.md` → **bắt buộc PR + 1 approve** |

## 3. Ba quy tắc chống conflict

**① Notebook không bao giờ dùng chung.**
File `.ipynb` là JSON có output nhúng — git gần như luôn conflict. Mỗi người một notebook riêng,
và **logic thật phải nằm trong `src/`**, notebook chỉ gọi hàm + hiển thị.

**② Kanban tách file theo người.**
Nếu 3 người cùng sửa một `KANBAN.md` thì conflict mỗi lần cập nhật trạng thái. Vì vậy board được
tách thành `phong_data.md` / `thong_model.md` / `loc_eval.md` — mỗi người chỉ sửa file của mình.

**③ Không hai người cùng sửa một module.**
Ví dụ Ngày 3 cả Phong và Thông đều chạy K-Means, nhưng **chỉ B sửa `clustering.py`**; Phong chỉ *gọi* hàm đó
từ notebook của mình. Lợi ích kép: không conflict, và hai nhánh thí nghiệm dùng chung một code path
→ khác biệt kết quả chắc chắn đến từ scaling chứ không phải do implementation khác nhau.

## 4. Quy ước đặt tên output

| Loại | Mẫu | Ví dụ |
|---|---|---|
| Figure | `{owner}_{task}_{name}.png` | `phong_t3_shot_heatmap.png` |
| Bảng kết quả | `reports/tables/{task}_{name}.csv` | `t5_k_selection_summary.csv` |
| Nhãn cụm | `data/processed/labels_{arm}.csv` | `labels_scaled.csv` |
