---
description: Tổng hợp trạng thái cả nhóm cho standup 09:00
allowed-tools: Read, Grep, Bash(git log:*), Bash(git branch:*), Bash(git status:*), Bash(pytest:*)
---

Chuẩn bị nội dung standup 09:00 cho LEAD (**Phong**).

> ⚠️ Trạng thái thẻ nằm ở **board UI**, repo không đọc được. Đừng grep `#doing` / `#blocked`.
> Nếu LEAD dán nội dung board UI vào thì dùng nó cho cột *Hôm nay*; nếu không, chỉ báo cáo phần
> suy được từ repo và **nói rõ phần nào còn thiếu** thay vì đoán.

Thu thập từ repo:

1. **Commit 24h qua** — `git log --oneline --all --since="1 day ago"`, nhóm theo mã task và theo người.
2. **Việc đã thực sự xong** — `grep -rn "NotImplementedError" src/` để biết hàm nào còn là stub.
   Stub đã biến mất nhưng commit chưa có trên `main` ⇒ xong ở branch, **chưa merge** → chưa tính là done.
3. **Test** — `pytest -q -rx`. Nêu số fail, và mọi **XPASS** (hàm đã xong nhưng còn marker `xfail`).
4. **Artifact đã có** — kiểm tra sự tồn tại của `data/interim/shots_raw.csv`,
   `data/processed/X_scaled.csv` · `X_unscaled.csv` · `labels_*.csv`, `reports/tables/*`.
   Đây là bằng chứng gate cứng nhất, không phụ thuộc ai khai báo gì.
5. **Gate sắp tới** — đọc `docs/PLAN.md`, liệt kê mục Definition of Done chưa đạt.

Trình bày dạng bảng 3 cột (Hôm qua / Hôm nay / Blocked) đúng format `docs/STATE.md` §5 để LEAD dán thẳng vào.

Cuối cùng đánh giá rủi ro tiến độ: nếu gate sắp tới có nguy cơ trễ > 2h, nhắc lại **thẻ descope đầu tiên**
theo bảng trong `docs/PLAN.md` — cắt gì, tiết kiệm bao nhiêu giờ, ảnh hưởng ra sao.

Không tự sửa `docs/STATE.md` (thuộc LEAD) — chỉ đề xuất nội dung.
