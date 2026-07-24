---
description: Giải thích project cho thành viên mới và chỉ ra việc cần làm đầu tiên
argument-hint: "[Phong|Thông|Lộc] — vai trò của bạn (bỏ trống nếu chưa biết)"
allowed-tools: Read, Grep, Glob, Bash(git branch:*), Bash(git log:*), Bash(pytest:*)
---

Thành viên mới cần hiểu project này. Vai trò của họ: **$1** (nếu trống thì hỏi họ là Phong, Thông hay Lộc).

Hãy làm theo thứ tự:

1. Đọc `CLAUDE.md` để nắm bối cảnh tổng thể.
2. Đọc `docs/PLAN.md` để hiểu kế hoạch 4 ngày và vì sao pipeline vốn nối tiếp lại chạy song song được.
3. Đọc board tương ứng với vai trò của họ trong `docs/board/`.
4. Đọc `docs/STRUCTURE.md` phần ma trận sở hữu — xác định họ được commit trực tiếp vào file nào.

Sau đó trình bày cho họ, ngắn gọn:

- **Project làm gì** và câu hỏi nghiên cứu (2–3 câu, không dài dòng)
- **Vai trò của họ** trong 4 ngày, branch cần checkout
- **Thẻ đầu tiên họ nên làm**, kèm mã task và file cần tạo
- **Những file họ KHÔNG được sửa** (thuộc người khác) và cách xử lý nếu cần thay đổi
- **Bất biến nào họ dễ vô tình phá nhất** dựa trên vai trò cụ thể:
  - Phong → cạm bẫy boolean absent-when-true, lọc penalty, encoding
  - Thông → không đưa `Y_hidden` vào X, giữ nguyên chữ ký `run_kmeans_sweep` vì Phong cũng gọi
  - Lộc → tách GK khỏi `n_defenders_in_cone`, CV chỉ đo tính ổn định chứ không đo tính "đúng"

Kết thúc bằng đúng các lệnh họ cần chạy để bắt đầu (`pip install -e .`, `git checkout <branch>`, `pytest -q`).

Đừng liệt kê lại toàn bộ cây thư mục — họ tự xem được. Tập trung vào những gì phải đọc nhiều file mới hiểu.
