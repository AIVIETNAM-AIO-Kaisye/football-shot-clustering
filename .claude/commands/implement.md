---
description: Implement một thẻ task theo đúng ma trận sở hữu và test đã đặc tả
argument-hint: "<mã task> — ví dụ T1.3b"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(pytest:*), Bash(git status:*), Bash(git diff:*)
---

Implement task **$1**.

Trước khi viết code, bắt buộc làm đủ 4 bước sau:

1. **Tìm thẻ** — grep `$1` trong `docs/board/` để lấy mô tả, output mong đợi, và các cảnh báo ⚠️.
2. **Xác định chủ sở hữu file** — đối chiếu `docs/STRUCTURE.md`. Nếu task này chạm vào file thuộc người khác,
   **dừng lại và báo**, đừng sửa. Nếu chạm file `[SHARED]` (`config.py`, `DATA_CONTRACT.md`) thì nhắc rằng
   cần PR + 1 approve.
3. **Đọc stub** — docstring trong `src/shotquality/` đã ghi sẵn công thức, cạm bẫy và ràng buộc.
   **Không đổi chữ ký hàm** — đó là interface đã đóng băng cho 2 người còn lại (xem `CLAUDE.md`).
4. **Đọc test đặc tả** — grep trong `tests/` xem có test nào đang `xfail` cho hàm này. Test chính là spec;
   implement để nó pass chứ không sửa test cho khớp code.

Sau khi implement:

- Chạy `pytest <file test liên quan> -q`. Khi test chuyển sang **XPASS**, xoá dòng `pytestmark = pytest.mark.xfail(...)`
  của module đó rồi chạy lại để xác nhận thật sự xanh.
- Kiểm tra không hardcode: mọi hằng số phải lấy từ `config.py`.
- Nếu quá trình implement phát sinh quyết định kỹ thuật (chọn cách xử lý missing, chọn ngưỡng, đổi công thức…)
  thì nhắc người dùng thêm ADR vào `docs/DECISIONS.md`.
- Đề xuất commit message đúng format: `<type>(<module>): $1 <mô tả>`.
- Nhắc kéo thẻ sang cột **Chờ duyệt** trên board UI (trạng thái không nằm trong repo).

Nếu task liên quan tới `X` hoặc preprocessing, kiểm tra lại lần cuối: không có cột nào trong
`config.HIDDEN_COLS` lọt vào feature.
