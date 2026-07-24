---
description: Kiểm tra Definition of Done của một gate trước khi chốt
argument-hint: "[1|2|3|4] — số gate"
allowed-tools: Read, Grep, Glob, Bash(pytest:*), Bash(git log:*), Bash(git status:*), Bash(python:*)
---

Kiểm tra GATE **$1** đã thực sự đạt chưa. Đọc mục Definition of Done tương ứng trong `docs/PLAN.md`,
rồi **kiểm chứng bằng cách chạy thật**, không chỉ đọc code:

**GATE 1** — `data/interim/shots_raw.csv`
- File tồn tại? Số dòng có nằm trong 2.500–2.700?
- Đủ cột theo `config.ID_COLS + FEATURE_COLS + HIDDEN_COLS`?
- `x ∈ [0,120]`, `y ∈ [0,80]`? Còn penalty hay `period == 5` sót lại không?
- Các cột `config.BOOL_FLAGS` còn NaN không?
- Tên cầu thủ có dấu đọc lên có đúng không (kiểm tra mojibake)?
- `docs/DATA_CONTRACT.md` đã đánh dấu FROZEN chưa?

**GATE 2** — `X_scaled.csv` / `X_unscaled.csv`
- Hai file cùng số dòng, cùng thứ tự cột, join được với `shot_id`?
- 🚨 **Kiểm tra rò rỉ:** không cột nào trong `config.HIDDEN_COLS` xuất hiện trong X. Đây là lỗi nghiêm trọng nhất có thể xảy ra ở project này.
- `pytest -q` xanh?

**GATE 3** — kết quả thí nghiệm
- Có đủ bảng chọn K cho **cả hai** nhánh?
- Có con số ARI? Được tính ở **cùng một k** cho hai nhánh chứ?
- Có CV accuracy ± std?
- Bảng `cluster_profile` có đủ `goal_rate` và `mean_xg` theo cụm?

**GATE 4** — report
- `reports/final_report.md` có đủ 4 bảng bắt buộc + 3 biểu đồ?
- Số liệu trong report khớp với file trong `reports/tables/`?
- `docs/DECISIONS.md` đã ghi mọi lựa chọn kỹ thuật phát sinh?

Báo cáo dạng checklist ✅/❌ kèm **bằng chứng cụ thể** (số dòng thật, tên cột thật, output lệnh thật).
Với mục ❌, nêu rõ thẻ nào trong `docs/board/` cần hoàn thành và ước lượng thời gian còn thiếu.

Nếu gate không đạt và đã trễ, nhắc thẻ descope tương ứng trong `docs/PLAN.md`.
