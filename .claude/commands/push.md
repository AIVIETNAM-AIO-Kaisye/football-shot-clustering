---
description: Chạy toàn bộ kiểm tra trước khi push, rồi in ra lệnh push để tự chạy
allowed-tools: Read, Grep, Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(git ls-files:*), Bash(git branch:*), Bash(git rev-list:*), Bash(pytest:*)
---

Kiểm tra repo đã sẵn sàng push chưa.

> 🚫 **Command này KHÔNG tự push.** `Bash(git push:*)` cố ý không nằm trong `allowed-tools` —
> việc đẩy code lên remote luôn do người dùng tự bấm. Kết thúc bằng cách **in ra lệnh push** để copy.

Chạy lần lượt, báo ✅/❌ cho từng mục:

**1. Working tree sạch**
`git status --short` — còn file chưa commit thì liệt kê ra và **dừng lại**, hỏi có muốn commit không.

**2. Test xanh**
`pytest -q`. Kỳ vọng toàn `xfailed` (stub chưa implement) hoặc `passed`.
Có **XPASS** ⇒ hàm đã implement nhưng còn marker `xfail` → nhắc xoá marker trước khi push.
Có **failed** ⇒ ❌ dừng, không push.

**3. Không lọt dữ liệu thô** *(bảo vệ giới hạn 100 MB của GitHub)*
- `git ls-files data/raw/` — chỉ được phép có đúng `data/raw/.gitkeep`, không gì khác.
- `git ls-files -s data/ | wc -l` và liệt kê file > 1 MB trong index.
  Chỉ `data/interim/shots_raw.csv` (<1 MB, ADR-003) được commit; mọi file lớn khác là ❌.

**4. Không rò nhãn** *(lỗi nghiêm trọng nhất của project này — nó fail âm thầm)*
Đọc `src/shotquality/config.py`, đối chiếu `HIDDEN_COLS` với `FEATURE_COLS`:
giao của hai tập **phải rỗng**. Nếu `preprocess.py` đã được implement, kiểm tra thêm là nó
không đưa `shot_outcome` · `is_goal` · `statsbomb_xg` · `end_x/y/z` vào `X`.

**5. Commit message đúng format**
`git log --oneline origin/main..HEAD` — mỗi commit phải khớp `<type>(<module>): <mã task> <mô tả>`
với `type` ∈ `feat` `fix` `docs` `test` `refactor` `chore`. Nêu commit nào lệch format.

**6. Tác giả commit**
`git log --format="%an <%ae>" origin/main..HEAD | sort -u` — cảnh báo nếu thấy tác giả lạ
(vd `team@local`). Commit đã push rồi thì sửa phải force-push, nên bắt ở đây.

**7. Trạng thái 3 branch**
`git branch -v` + `git rev-list --left-right --count main...<branch>` cho `data-eng`, `ml-eng`, `eval-eng`.
Báo branch nào tụt sau `main` và cần rebase.

**8. File `[SHARED]`**
`git diff --name-only origin/main..HEAD` — nếu đụng `config.py`, `docs/DATA_CONTRACT.md`
hoặc `requirements.txt` thì nhắc: cần **PR + 1 approve**, và phải báo nhóm chat
(`docs/WORKFLOW.md` §2 — luật review PR).

---

Nếu tất cả ✅, in ra **đúng lệnh push cần chạy** cho branch hiện tại, ví dụ:

```cmd
git push origin main
```

Nếu 3 branch cùng cần đẩy:

```cmd
git push origin main data-eng ml-eng eval-eng
```

Cuối cùng nhắc: sau khi push xong, kéo các thẻ tương ứng sang cột **Chờ duyệt** (nếu mở PR)
hoặc **Hoàn thành** (nếu đã merge vào `main`) trên board UI.
