# Kanban Board — Tổng quan

> Board được **tách 3 file theo người** để không bao giờ conflict khi cùng cập nhật trạng thái.
> Mỗi người **chỉ sửa file của mình**. File này do LEAD tổng hợp.

| Người | File board | Branch | Vai trò |
|---|---|---|---|
| **A** | [`A_data.md`](A_data.md) | `data-eng` | Ingest · Thống kê mô tả · EDA · nhánh **unscaled** |
| **B** | [`B_model.md`](B_model.md) | `ml-eng` | Geometry · Preprocessing · K-Means · nhánh **scaled** |
| **C** | [`C_eval.md`](C_eval.md) | `eval-eng` | Freeze-frame · Gap statistic · KNN-CV · Validation · Report |

## Xem board dạng cột (chạy lệnh)

```bash
grep -rn "#doing"    docs/board/     # cột DOING  — kiểm tra WIP limit ≤ 2/người
grep -rn "#review"   docs/board/     # cột REVIEW — có PR nào đang chờ?
grep -rn "#blocked"  docs/board/     # ai đang tắc → nêu ở standup
grep -rc "#done"     docs/board/*.md # đếm tiến độ
```

## Đường găng (critical path)

Các thẻ `#p0` dưới đây trễ là **cả nhóm trễ**:

```
T1.1 ─┐
T1.3 ─┼─► T1.5 shots_raw.csv ─► T3.6 chốt feature ─► T4.4 X_scaled ─┬─► T5.1 unscaled ─┐
T1.4 ─┘        (GATE 1)                                (GATE 2)      └─► T5.2 scaled ───┴─► T5.3 ARI
                                                                                             │
                                                              T5.4 chốt cụm ◄────────────────┘
                                                                     │
                                                       T5.5 KNN-CV ◄─┴─► T6.2 external validation
                                                              (GATE 3)          │
                                                                                ▼
                                                                        T6.4 report (GATE 4)
```

## Bảng tiến độ tổng (LEAD cập nhật mỗi standup)

| Ngày | A | B | C | Gate |
|---|---|---|---|---|
| D1 | ⬜ 0/4 | ⬜ 0/4 | ⬜ 0/4 | 🚦 GATE 1 ⬜ |
| D2 | ⬜ 0/11 | ⬜ 0/7 | ⬜ 0/4 | 🚦 GATE 2 ⬜ |
| D3 | ⬜ 0/4 | ⬜ 0/4 | ⬜ 0/4 | 🚦 GATE 3 ⬜ |
| D4 | ⬜ 0/3 | ⬜ 0/3 | ⬜ 0/3 | 🚦 GATE 4 ⬜ |

## Bảng tag nhanh

`#todo` `#doing` `#review` `#done` `#blocked` — trạng thái (mỗi thẻ đúng 1 tag)
`#data` `#eda` `#model` `#eval` `#docs` `#infra` — loại việc
`#p0` đường găng · `#p1` quan trọng · `#p2` cắt trước khi thiếu giờ
