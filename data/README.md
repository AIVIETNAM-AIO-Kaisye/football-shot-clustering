# Thư mục dữ liệu

| Thư mục | Nội dung | Git |
|---|---|---|
| `raw/` | `events/{match_id}.json` tải từ open-data (~350 MB) | 🚫 **gitignored** |
| `interim/` | `shots_raw.csv`, `match_ids.json` | ✅ commit |
| `processed/` | `X_scaled.csv`, `X_unscaled.csv`, `y_hidden.csv`, `labels_*.csv` | ✅ commit |

## Vì sao commit `interim/` và `processed/`? — ADR-003

`shots_raw.csv` chỉ ~2.600 dòng (< 1 MB) nhưng là **artifact chung của cả nhóm**.
Commit nó ⇒ B và C bắt đầu làm việc từ Ngày 2 mà không phải tải lại 350 MB events JSON.
Đây chính là điều kiện để 3 luồng chạy song song.

## Luồng dữ liệu

```
open-data (raw URL)
   │  scripts/01_download.py
   ▼
data/raw/events/*.json                    350 MB · gitignored
   │  scripts/02_extract_shots.py         lọc Shot · bỏ penalty & luân lưu
   ▼
data/interim/shots_raw.csv                ~2.600 dòng · GATE 1
   │  scripts/04_preprocess.py            tách X / Y_hidden / ID
   ├──────────────────────┬───────────────────────────┐
   ▼                      ▼                           ▼
X_unscaled.csv        X_scaled.csv               y_hidden.csv
   │                      │                     🚫 KHÔNG đưa vào model
   │ (A) K-Means          │ (B) K-Means                │
   ▼                      ▼                           │
labels_unscaled.csv   labels_scaled.csv               │
   └──────── ARI ────────┘                            │
                          │                           │
                          ├──► KNN + 5-fold CV        │
                          │    (ổn định cụm)          │
                          └──► join ◄─────────────────┘
                               (goal rate + xG theo cụm)
```

## ⚠️ Đừng bao giờ

- commit `data/raw/` — 350 MB, đã có trong `.gitignore`
- đưa cột trong `y_hidden.csv` vào `X` — data leakage (ADR-006)
- sửa `shots_raw.csv` bằng tay — sinh lại bằng `scripts/02_extract_shots.py`
