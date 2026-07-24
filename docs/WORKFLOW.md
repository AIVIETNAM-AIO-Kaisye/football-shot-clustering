# Quy trình làm việc — Git + Kanban

## 1. Hệ thống tag Kanban

### Hai board — chia vai rõ ràng

Nhóm dùng **board UI** (5 cột) song song với **markdown** trong [`docs/board/`](board/), tách riêng 1 file
cho mỗi người để không bao giờ conflict. Cập nhật cả hai nơi thì chắc chắn lệch nhau sau vài ngày, nên
mỗi bên chỉ giữ đúng một vai:

| | Nguồn sự thật cho | Ai cập nhật | Nhịp |
|---|---|---|---|
| **Board UI** | **trạng thái** — ai đang làm gì, ai đang tắc | mỗi người, thẻ của mình | ngay khi đổi trạng thái |
| **`docs/board/*.md`** | **nội dung** — output, bẫy kỹ thuật, blocked-by, tham chiếu ADR | chủ file, qua commit | khi phạm vi công việc đổi |

Mã task `T<task>.<subtask>` là khoá nối hai bên — tra chéo lúc nào cũng được.

> ⚠️ **Tag trạng thái trong markdown đã ngừng dùng.** Các thẻ `.md` vẫn còn `#todo` từ lúc khởi tạo —
> đó là giá trị chết, **không đọc, không sửa**. Muốn biết trạng thái thì nhìn board UI.
> Tag ưu tiên (`#p0/#p1/#p2`) và loại việc (`#data/#eda/...`) vẫn còn giá trị.

### 5 cột board UI

| Cột | Vào cột này khi |
|---|---|
| **Chưa làm** | thẻ đã tạo, chưa ai cầm |
| **Đang làm** | đang code — **tối đa 2 thẻ/người** |
| **Đang gặp vấn đề** | bị chặn — mô tả **phải** ghi rõ đang chờ ai/cái gì |
| **Chờ duyệt** | đã mở PR, chưa merge |
| **Hoàn thành** | **đã merge vào `main`** — không phải "chạy được trên máy tôi" |

Chỉ tạo thẻ UI cho **ngày hiện tại**; thêm thẻ ngày mới ở standup 09:00. Đổ hết ~55 thẻ vào board
một lúc thì không ai đọc nổi, và sau mỗi gate nhiều thẻ sẽ đổi.

### Điền thẻ trên UI

UI không có ô người phụ trách và ô ưu tiên → nhét vào **tên thẻ**, giữ nguyên format của markdown:

```
T1.2 @phong #p0 — Lọc Shot + làm phẳng boolean flags
```

Mô tả theo 5 dòng cố định. Đây là *tin nhắn giao việc* — người nhận đọc xong phải làm được ngay
mà không cần hỏi lại:

```
🎯 Output:    file/hàm cụ thể — không ghi "làm xong task X"
✅ Done khi:  điều kiện kiểm chứng được, có số
⚠️ Bẫy:       cạm bẫy đã biết, ghi luôn hậu quả nếu dính
🔗 Chặn bởi:  thẻ + tên người, kèm giờ handoff
📄 Đọc:       file tài liệu + số mục
```

Nội dung 5 dòng này lấy từ thẻ tương ứng trong `docs/board/*.md` — đừng tự nghĩ lại.

### Cấu trúc một thẻ trong markdown

```
- [ ] T1.2 @phong #data #p0 #todo — Trích xuất field từ shot event  `est 3h`
      ↳ out: data/interim/shots_raw.csv
      ↳ blocked-by: —
```

| Thành phần | Ý nghĩa |
|---|---|
| `- [ ]` | checkbox — **không dùng nữa**, trạng thái nằm ở board UI |
| `T1.2` | mã task, khớp với Task 0–6 trong `PLAN.md` — khoá nối sang board UI |
| `@phong` | người phụ trách — `@phong` / `@thong` / `@loc` |
| `#data` | loại công việc |
| `#p0` | độ ưu tiên |
| `#todo` | ~~trạng thái~~ — **giá trị chết**, bỏ qua (xem phần trên) |
| `est 3h` | ước lượng thời gian |
| `↳ out:` | artifact đầu ra — chép vào dòng `🎯 Output` của thẻ UI |
| `↳ blocked-by:` | thẻ đang chặn — chép vào dòng `🔗 Chặn bởi` của thẻ UI |

> **Vì sao tag viết không dấu?** `@phong` `@thong` `@loc` thay vì `@Phong` `@Thông` `@Lộc`.
> Terminal Windows mặc định dùng codepage cp1252, `grep` ký tự có dấu dễ ra kết quả sai hoặc vỡ chữ.
> Tag là thứ được grep hàng chục lần mỗi ngày nên ưu tiên an toàn; tên đầy đủ có dấu vẫn dùng bình thường
> trong tiêu đề và bảng.

### Bộ tag chuẩn

| Nhóm | Tag | Ý nghĩa |
|---|---|---|
| **Trạng thái** | ~~`#todo` `#doing` `#review` `#done` `#blocked`~~ | **đã chuyển sang 5 cột board UI** |
| **Loại** | `#data` `#eda` `#model` `#eval` `#docs` `#infra` | phân loại công việc |
| **Ưu tiên** | `#p0` | nằm trên đường găng (critical path) — trễ là cả nhóm trễ |
| | `#p1` | quan trọng, không chặn người khác |
| | `#p2` | nice-to-have, cắt đầu tiên khi thiếu giờ |

### Tra cứu nhanh bằng grep

Grep chỉ còn dùng để tra **nội dung**; trạng thái xem trên board UI.

```bash
grep -rn "@phong"  docs/board/           # toàn bộ việc của Phong
grep -rn "#p0"     docs/board/           # toàn bộ việc trên đường găng
grep -rn "blocked-by" docs/board/        # các phụ thuộc chéo giữa 3 người
grep -rn "T1.2"    docs/ src/            # lần theo 1 mã task xuyên PLAN ↔ board ↔ code
```

### Luật vận hành

1. **WIP limit = 2.** Không quá 2 thẻ ở cột *Đang làm* cùng lúc. Muốn nhận thẻ mới → phải đẩy thẻ cũ sang *Chờ duyệt* hoặc *Đang gặp vấn đề*.
2. **Kéo thẻ ngay khi đổi trạng thái**, không dồn cuối ngày.
3. Thẻ ở cột *Đang gặp vấn đề* phải ghi rõ đang chờ ai/cái gì trong mô tả, và được nêu ở standup 09:00.
4. Chỉ kéo sang *Hoàn thành* khi **đã merge vào `main`**, không phải khi code chạy trên máy mình.
5. Nội dung thẻ UI chép từ `docs/board/*.md`. Nếu phát hiện phạm vi công việc khác thực tế → sửa file `.md` (commit), rồi mới sửa thẻ UI.

---

## 2. Git

### Branch

| Branch | Chủ | Ghi chú |
|---|---|---|
| `main` | — | luôn ở trạng thái chạy được; **không ai commit thẳng** |
| `data-eng` | Phong | |
| `ml-eng` | Thông | |
| `eval-eng` | Lộc | |

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
(`git checkout --theirs notebooks/phong_eda.ipynb`) rồi chạy lại — vì logic thật nằm ở `src/`, notebook chạy lại là có.

---

## 3. Checklist trước khi mở PR

- [ ] `pytest` pass
- [ ] Không commit file trong `data/raw/`
- [ ] Không hardcode đường dẫn tuyệt đối — dùng `config.py`
- [ ] Notebook đã `Restart & Run All` một lần trước khi commit
- [ ] Đã kéo thẻ sang cột **Chờ duyệt** trên board UI
- [ ] Nếu đổi file `[SHARED]` → đã báo trong nhóm chat
