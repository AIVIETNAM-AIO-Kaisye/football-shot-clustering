---
description: Thêm một quyết định kỹ thuật mới vào DECISIONS.md
argument-hint: "<tóm tắt quyết định>"
allowed-tools: Read, Grep, Edit
---

Ghi quyết định kỹ thuật mới vào `docs/DECISIONS.md`: **$ARGUMENTS**

1. Đọc `docs/DECISIONS.md`, lấy số ADR tiếp theo.
2. Kiểm tra xem quyết định này có **mâu thuẫn hoặc thay thế** ADR nào đang có không.
   Nếu có, đánh dấu ADR cũ là `❌ Superseded by ADR-0xx` thay vì xoá đi.
3. Viết ADR mới theo đúng mẫu ở cuối file: **Bối cảnh → Quyết định → Lý do → Hệ quả**.

Yêu cầu về nội dung:
- *Bối cảnh* phải nêu vấn đề thật đã gặp, không viết chung chung.
- *Lý do* là phần quan trọng nhất — đây là chỗ trả lời câu "tại sao nhóm chọn thế này" khi bảo vệ report.
  Nếu có phương án thay thế đã cân nhắc và loại bỏ, ghi rõ vì sao loại.
- *Hệ quả* nêu cả mặt được lẫn mặt mất, và ảnh hưởng tới file/task nào.
- Nếu quyết định dựa trên số liệu thật (số dòng, tỷ lệ, kết quả đo), **trích số liệu cụ thể** vào ADR.

Nếu quyết định làm thay đổi schema hoặc danh sách feature, nhắc người dùng cập nhật thêm:
`docs/DATA_CONTRACT.md` §6 (nhật ký thay đổi hợp đồng) và `config.py` — cả hai đều là file `[SHARED]`,
cần PR + 1 approve và phải báo cả nhóm trong ngày.
