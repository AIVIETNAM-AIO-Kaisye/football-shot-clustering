---
description: Hiển thị công việc của một người và gợi ý thẻ tiếp theo nên làm
argument-hint: "[Phong|Thông|Lộc]"
allowed-tools: Read, Grep, Bash(git branch:*), Bash(git status:*), Bash(git log:*), Bash(pytest:*)
---

Hiển thị tình hình công việc của thành viên **$1**.

> ⚠️ Trạng thái thẻ (đang làm / tắc / chờ duyệt) nằm ở **board UI**, không có trong repo.
> Đừng grep `#doing` / `#blocked` — luôn rỗng. Ở đây suy tiến độ từ **bằng chứng trong repo**,
> đáng tin hơn trạng thái tự khai báo.

1. Đọc file board của $1 trong `docs/board/` → danh sách thẻ + mã task + cảnh báo.
2. Suy trạng thái thật của từng mã task:
   - **chưa làm** — hàm tương ứng vẫn là stub `raise NotImplementedError("<mã task> @<ai>")`
     → `grep -rn "NotImplementedError" src/`
   - **đang dở / xong trên branch** — stub đã biến mất nhưng chưa có commit trên `main`
   - **đã merge** — có commit mang mã task đó và commit nằm trong `main`
3. Chạy `pytest -q -rx`. Test **XPASS** = hàm đã implement nhưng **chưa xoá marker `xfail`** →
   nêu ra, đây là việc còn sót của chủ module.

Sau đó **gợi ý đúng một thẻ tiếp theo** nên làm, ưu tiên `#p0` → `#p1` → `#p2`.
Bỏ qua thẻ mà dòng `blocked-by:` trỏ tới task chưa xong — nói rõ đang chờ ai.

Với thẻ được gợi ý, nêu:
- mã task và mô tả
- file cần tạo/sửa — **phải nằm trong vùng sở hữu của $1**, đối chiếu `docs/STRUCTURE.md`
- các cảnh báo ⚠️ đã ghi sẵn trong thẻ
- test nào trong `tests/` đang đặc tả cho thẻ đó

Không tự sửa file board. Nhắc $1 tự kéo thẻ sang cột *Đang làm* trên board UI (WIP limit ≤ 2).
