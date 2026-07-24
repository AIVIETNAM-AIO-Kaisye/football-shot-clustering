# Kanban Board — Tổng quan

> Board được **tách 3 file theo người** để không bao giờ conflict.
> Mỗi người **chỉ sửa file của mình**. File này do LEAD (**Phong**) tổng hợp.
>
> ⚠️ **Các file `.md` ở đây là nguồn sự thật cho *nội dung* công việc** (output, bẫy kỹ thuật,
> blocked-by), **không phải cho trạng thái**. Ai đang làm gì / ai đang tắc → xem **board UI**.
> Tag `#todo` còn sót trong các thẻ là giá trị chết từ lúc khởi tạo, bỏ qua.
> Luật đầy đủ ở [`WORKFLOW.md`](../WORKFLOW.md) §1.

| Người | File board | Branch | Vai trò |
|---|---|---|---|
| **Phong** | [`phong_data.md`](phong_data.md) | `data-eng` | Ingest · Thống kê mô tả · EDA · nhánh **unscaled** |
| **Thông** | [`thong_model.md`](thong_model.md) | `ml-eng` | Geometry · Preprocessing · K-Means · nhánh **scaled** |
| **Lộc** | [`loc_eval.md`](loc_eval.md) | `eval-eng` | Freeze-frame · Gap statistic · KNN-CV · Validation · Report |

## Tra cứu nhanh (chạy lệnh)

```bash
grep -rn "@phong"     docs/board/    # toàn bộ việc của một người
grep -rn "#p0"        docs/board/    # toàn bộ việc trên đường găng
grep -rn "blocked-by" docs/board/    # các phụ thuộc chéo giữa 3 người
```

Trạng thái (đang làm / tắc / chờ duyệt) **không grep được** — xem board UI.

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

## Khối lượng thẻ theo ngày

Dùng để cân tải và lập thẻ UI mỗi sáng — **không phải bảng tiến độ**.
Tiến độ xem board UI; số liệu chốt của project xem [`STATE.md`](../STATE.md).

| Ngày | Phong | Thông | Lộc | Gate |
|---|---|---|---|---|
| D1 | 4 thẻ | 4 thẻ | 4 thẻ | 🚦 GATE 1 |
| D2 | 11 thẻ | 7 thẻ | 4 thẻ | 🚦 GATE 2 |
| D3 | 4 thẻ | 4 thẻ | 4 thẻ | 🚦 GATE 3 |
| D4 | 3 thẻ | 3 thẻ | 3 thẻ | 🚦 GATE 4 |

## Bảng tag nhanh

`#data` `#eda` `#model` `#eval` `#docs` `#infra` — loại việc
`#p0` đường găng · `#p1` quan trọng · `#p2` cắt trước khi thiếu giờ

Trạng thái **không còn là tag** — nó là 5 cột trên board UI. Xem [`WORKFLOW.md`](../WORKFLOW.md) §1.
