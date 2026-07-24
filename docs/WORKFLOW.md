# Quy trình làm việc — Git + Kanban

## 1. Hệ thống tag Kanban

Board nằm ở [`docs/board/`](board/), **tách riêng 1 file cho mỗi người** để không bao giờ conflict.

### Cấu trúc một thẻ (card)

```
- [ ] T1.2 @A #data #p0 #doing — Trích xuất field từ shot event  `est 3h`
      ↳ out: data/interim/shots_raw.csv
      ↳ blocked-by: —
```

| Thành phần | Ý nghĩa |
|---|---|
| `- [ ]` / `- [x]` | checkbox — tick khi `#done` |
| `T1.2` | mã task, khớp với Task 0–6 trong `PLAN.md` |
| `@A` | người phụ trách |
| `#data` | loại công việc |
| `#p0` | độ ưu tiên |
| `#doing` | **trạng thái kanban** — mỗi thẻ có đúng 1 tag trạng thái |
| `est 3h` | ước lượng thời gian |
| `↳ out:` | artifact đầu ra — dùng để kiểm tra Definition of Done |
| `↳ blocked-by:` | thẻ đang chặn thẻ này |

### Bộ tag chuẩn

| Nhóm | Tag | Ý nghĩa |
|---|---|---|
| **Trạng thái** | `#todo` | chưa bắt đầu |
| | `#doing` | đang làm — **giới hạn WIP: tối đa 2 thẻ/người** |
| | `#review` | đã mở PR, chờ review |
| | `#done` | đã merge vào `main` |
| | `#blocked` | đang bị chặn — **phải nêu trong standup** |
| **Loại** | `#data` `#eda` `#model` `#eval` `#docs` `#infra` | phân loại công việc |
| **Ưu tiên** | `#p0` | nằm trên đường găng (critical path) — trễ là cả nhóm trễ |
| | `#p1` | quan trọng, không chặn người khác |
| | `#p2` | nice-to-have, cắt đầu tiên khi thiếu giờ |

### Tra cứu nhanh bằng grep

```bash
grep -rn "#blocked" docs/board/          # ai đang tắc?
grep -rn "#doing"   docs/board/          # ai đang làm gì? (kiểm tra WIP limit)
grep -rn "@A"       docs/board/          # toàn bộ việc của A
grep -rn "#p0.*#todo" docs/board/        # việc critical chưa ai đụng
grep -rc "#done"    docs/board/*.md      # đếm tiến độ từng người
```

### Luật vận hành

1. **WIP limit = 2.** Không được có quá 2 thẻ `#doing` cùng lúc. Muốn nhận thẻ mới → phải đẩy thẻ cũ sang `#review` hoặc `#blocked`.
2. **Cập nhật tag ngay khi đổi trạng thái**, không dồn cuối ngày.
3. Thẻ `#blocked` phải ghi rõ `blocked-by:` và được nêu ở standup 09:00.
4. Chỉ chuyển sang `#done` khi **đã merge vào `main`**, không phải khi code chạy trên máy mình.

---

## 2. Git

### Branch

| Branch | Chủ | Ghi chú |
|---|---|---|
| `main` | — | luôn ở trạng thái chạy được; **không ai commit thẳng** |
| `data-eng` | A | |
| `ml-eng` | B | |
| `eval-eng` | C | |

Branch tồn tại suốt 4 ngày (không xoá sau mỗi merge) — hợp với mô hình mỗi người sở hữu một vùng file riêng.

### Commit message

```
<type>(<module>): <mã task> <mô tả ngắn>

feat(ingest):     T1.1 tải events JSON từ open-data
feat(features):   T1.3 thêm distance_to_goal và angle_to_goal
fix(freeze):      T1.4 sửa lỗi đếm nhầm đồng đội vào n_defenders
docs(contract):   đóng băng schema shots_raw.csv
test(validation): thêm test cho ARI trên nhãn hoán vị
chore(deps):      ghim scikit-learn==1.5.2
```

`type` ∈ `feat` `fix` `docs` `test` `refactor` `chore`

### Nhịp đồng bộ — 2 merge window mỗi ngày

Gộp việc merge vào 2 khung giờ cố định để tránh `main` bị xáo trộn liên tục:

| Giờ | Việc |
|---|---|
| **09:00** | Mọi người `git pull origin main` + rebase branch của mình **trước khi code** |
| **16:00** | Merge window #1 — mở PR cho phần đã xong |
| **18:00** | Merge window #2 — chốt cuối ngày, `main` phải xanh trước khi nghỉ |

```bash
# Đầu ngày
git checkout main && git pull origin main
git checkout data-eng && git rebase main

# Cuối ngày
git push origin data-eng
gh pr create --base main --title "T1.1 ingest events" --body "..."
```

### Luật review PR

| Loại thay đổi | Yêu cầu |
|---|---|
| File trong vùng sở hữu của mình | tự merge sau khi CI/pytest xanh |
| File `[SHARED]` (`config.py`, `DATA_CONTRACT.md`, `requirements.txt`) | **cần 1 approve** từ người khác |
| File của người khác | **cần approve của chính chủ file đó** |

### Xử lý khi vẫn dính conflict

Nếu conflict xảy ra thì gần như chắc chắn là do vi phạm ma trận sở hữu → dừng lại, xác định ai là
chủ file theo [`STRUCTURE.md`](STRUCTURE.md), **giữ bản của chủ file**, người kia mở PR đề nghị thay đổi.

Riêng notebook (`.ipynb`) nếu lỡ conflict: **không merge tay**, lấy nguyên bản của chủ sở hữu
(`git checkout --theirs notebooks/A_eda.ipynb`) rồi chạy lại — vì logic thật nằm ở `src/`, notebook chạy lại là có.

---

## 3. Checklist trước khi mở PR

- [ ] `pytest` pass
- [ ] Không commit file trong `data/raw/`
- [ ] Không hardcode đường dẫn tuyệt đối — dùng `config.py`
- [ ] Notebook đã `Restart & Run All` một lần trước khi commit
- [ ] Đã cập nhật thẻ kanban của mình sang `#review`
- [ ] Nếu đổi file `[SHARED]` → đã báo trong nhóm chat
