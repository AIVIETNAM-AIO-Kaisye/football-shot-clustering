# Shot Quality Clustering

Phân cụm chất lượng cơ hội sút bóng (*shot quality*) từ **StatsBomb open-data** bằng **K-Means**,
kiểm chứng độ ổn định của cụm bằng **KNN + k-fold cross-validation**.

> **Câu hỏi nghiên cứu:** Feature scaling và cách chọn K ảnh hưởng thế nào đến việc phân cụm
> các cú sút theo chất lượng cơ hội, và các cụm tìm được có thực sự phản ánh khả năng ghi bàn thật hay không?

## Thiết kế thí nghiệm

| Thành phần | Vai trò |
|---|---|
| **Biến thí nghiệm** | Feature scaling (`X_unscaled` vs `X_scaled`) · Số cụm K (2–10) |
| **Biến kiểm soát** | Distance metric cố định L2/Euclidean · `random_state=42` |
| **Đo khác biệt** | Adjusted Rand Index (ARI) giữa 2 phiên bản clustering |
| **Internal validation** | Silhouette · Elbow · Gap Statistic |
| **External validation** | Goal rate thực tế + xG trung bình theo cụm (từ field đã giấu) |
| **Kiểm định ổn định** | KNN 5-fold CV dự đoán `cluster_id` → accuracy ± std |

## Dữ liệu

| Nguồn | `hudl/open-data` (StatsBomb) |
|---|---|
| Giải đấu | UEFA Euro 2024 (`comp=55, season=282`) + FIFA World Cup 2022 (`comp=43, season=106`) |
| Số trận | 115 |
| Số shot dự kiến | ~2.600 (sau khi loại penalty & luân lưu) |

⚠️ **Không clone toàn bộ repo open-data (7.06 GB).** Chỉ tải `data/events/{match_id}.json` cho 115 trận
đã chọn. Xem [`docs/DECISIONS.md`](docs/DECISIONS.md) ADR-002.

## Quickstart

```bash
python -m venv .venv && .venv/Scripts/activate     # Windows
pip install -r requirements.txt

python scripts/01_download.py        # tải events JSON  -> data/raw/
python scripts/02_extract_shots.py   # trích xuất shot  -> data/interim/shots_raw.csv
python scripts/03_descriptive.py     # thống kê mô tả   -> reports/
python scripts/04_preprocess.py      # X_scaled/X_unscaled -> data/processed/
python scripts/05_cluster.py         # K-Means + chọn K  -> data/processed/labels_*.csv
python scripts/06_validate.py        # ARI + KNN CV      -> reports/
python scripts/07_report.py          # bảng tổng hợp     -> reports/final_report.md
```

## Tài liệu

| File | Nội dung |
|---|---|
| [`docs/PLAN.md`](docs/PLAN.md) | Kế hoạch 4 ngày, phân việc theo người, gate & descope |
| [`docs/STRUCTURE.md`](docs/STRUCTURE.md) | Bản đồ thư mục + **ma trận sở hữu file** (chống conflict) |
| [`docs/WORKFLOW.md`](docs/WORKFLOW.md) | Quy ước Git branch, PR, và hệ thống tag Kanban |
| [`docs/DATA_CONTRACT.md`](docs/DATA_CONTRACT.md) | Schema `shots_raw.csv` — **đóng băng từ cuối Ngày 1** |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | Nhật ký quyết định kỹ thuật (ADR) |
| [`docs/STATE.md`](docs/STATE.md) | Trạng thái hiện tại của project (cập nhật mỗi standup) |
| [`docs/board/BOARD.md`](docs/board/BOARD.md) | Kanban board — tổng quan 3 thành viên |

## Team

| Vai trò | Branch | Phụ trách |
|---|---|---|
| **Phong** — Data Engineer *(kiêm LEAD)* | `data-eng` | Ingest, EDA, thống kê mô tả, nhánh unscaled |
| **Thông** — ML Engineer | `ml-eng` | Feature engineering, preprocessing, K-Means, chọn K |
| **Lộc** — Evaluation & Report | `eval-eng` | Freeze-frame, Gap statistic, KNN-CV, validation, report |
