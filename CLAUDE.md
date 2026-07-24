# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Toàn bộ tài liệu và comment trong repo viết bằng tiếng Việt — giữ nguyên ngôn ngữ này khi thêm code/doc mới.

## Project là gì

Phân cụm chất lượng cơ hội sút bóng (*shot quality*) từ StatsBomb open-data bằng K-Means, kiểm chứng
độ ổn định cụm bằng KNN + k-fold cross-validation. Đây là **project nghiên cứu có thời hạn 4 ngày, 3 người**,
không phải sản phẩm dài hạn — mọi quyết định cấu trúc đều nhắm vào *chạy song song không conflict*.

Câu hỏi nghiên cứu: feature scaling và cách chọn K ảnh hưởng thế nào đến kết quả phân cụm, và các cụm
tìm được có phản ánh khả năng ghi bàn thật hay không?

## Lệnh thường dùng

```bash
pip install -e .                      # bắt buộc chạy 1 lần — src layout, không dùng sys.path hack

pytest -q                             # toàn bộ test
pytest tests/test_features.py -q      # 1 file
pytest tests/test_features.py::test_angle_near_byline_is_tiny   # 1 test
pytest -q -rx                          # xem lý do các test đang xfail
```

Pipeline (chạy theo thứ tự, mỗi script là 1 Task trong `docs/PLAN.md`):

```bash
python scripts/01_download.py                # events JSON  -> data/raw/       (~350 MB)
python scripts/02_extract_shots.py           # shots_raw.csv                   (GATE 1)
python scripts/03_descriptive.py             # bảng thống kê -> reports/tables/
python scripts/04_preprocess.py              # X_scaled + X_unscaled + y_hidden (GATE 2)
python scripts/05_cluster.py --arm scaled    # K-Means 1 nhánh; --arm unscaled cho nhánh kia
python scripts/05_cluster.py --arm scaled --skip-gap   # khi Gap Statistic bị descope
python scripts/06_validate.py                # ARI + KNN-CV + external validation (GATE 3)
python scripts/07_report.py                  # gộp bảng -> reports/final_report.md (GATE 4)
```

Kanban — nhóm dùng **hai board chia vai**, đừng nhầm (`docs/WORKFLOW.md` §1):

- **Board UI 5 cột** = nguồn sự thật cho **trạng thái** (ai đang làm gì, ai tắc). Không truy cập được từ repo.
- **`docs/board/*.md`** = nguồn sự thật cho **nội dung** (output, bẫy, blocked-by). Tag `#todo` còn sót
  trong các thẻ là **giá trị chết** — đừng suy ra trạng thái từ đó, và đừng grep `#doing`/`#blocked` (luôn rỗng).

```bash
grep -rn "@phong"     docs/board/     # toàn bộ việc của một người
grep -rn "#p0"        docs/board/     # việc trên đường găng
grep -rn "blocked-by" docs/board/     # phụ thuộc chéo giữa 3 người
```

## Kiến trúc

### Luồng dữ liệu

```
open-data raw URL → data/raw/events/*.json  (gitignored, 350 MB)
                  → data/interim/shots_raw.csv   ← artifact chung, CÓ commit
                  → data/processed/  X_unscaled.csv ┐
                                     X_scaled.csv   ├─ hai nhánh thí nghiệm
                                     y_hidden.csv   ┘  🚫 không bao giờ vào model
                  → labels_unscaled.csv / labels_scaled.csv → ARI, KNN-CV, cluster profile
```

`shots_raw.csv` được commit dù là file sinh ra (ADR-003): nó nhỏ (<1 MB) và là điều kiện để 2/3 thành viên
bắt đầu làm việc từ Ngày 2 mà không phải tải lại 350 MB.

### Ba bất biến không được phá

**① Tách `X` / `Y_hidden` / `ID`.** `shot_outcome`, `is_goal`, `statsbomb_xg`, `end_x/y/z` **cấm** xuất hiện
trong input của K-Means hay KNN (ADR-006). Chúng chỉ được join lại ở `evaluate.py` để external validation.
`end_location` là chỗ hay bị quên — nó là vị trí bóng *sau* khi sút, cũng là leakage.
Danh sách chính thức nằm ở `config.HIDDEN_COLS`.

**② L2/Euclidean là biến kiểm soát, không phải biến thí nghiệm** (ADR-009). Thí nghiệm chỉ có một biến độc
lập là *scaling*. Không đổi distance metric giữa hai nhánh, nếu không thì không quy được khác biệt cho scaling.

**③ Hai nhánh dùng chung `clustering.py`** (ADR-010). Nhánh unscaled và scaled đi qua **cùng một code path**
— nếu ai đó copy code ra chạy riêng thì chênh lệch kết quả không còn quy được cho scaling nữa.

### Mô hình sở hữu file (quan trọng nhất khi sửa code)

Repo được thiết kế để 3 người commit song song mà không conflict: **mỗi file có đúng một chủ sở hữu**.

| Chủ | Module |
|---|---|
| **Phong** `data-eng` | `io_utils.py` `ingest.py` `descriptive.py` · scripts 01–03 |
| **Thông** `ml-eng` | `features.py` `preprocess.py` `clustering.py` `selection.py` · scripts 04–05 |
| **Lộc** `eval-eng` | `freeze_frame.py` `selection_gap.py` `validation.py` `evaluate.py` `viz.py` · scripts 06–07 |
| **SHARED** | `config.py` `docs/DATA_CONTRACT.md` `requirements.txt` — cần PR + 1 approve |

Hệ quả khi làm việc trong repo này:
- **Trước khi sửa một file, xác định chủ của nó** trong `docs/STRUCTURE.md`. Sửa file người khác → mở PR, không commit đè.
- Chữ ký hàm trong các stub **đã đóng băng từ Ngày 1** — đó là interface để 3 người code song song. Đổi chữ ký = phá việc của người khác.
- `ingest.py` (Phong) gọi `features.add_geometry_features` (Thông) và `freeze_frame.extract_all` (Lộc). Đây là điểm giao duy nhất giữa 3 người ở Ngày 1.
- Board kanban tách 3 file `docs/board/{A,B,C}_*.md` cũng vì lý do này — đừng gộp lại thành một file.
- Notebook: mỗi người một file riêng, **logic thật phải nằm trong `src/`**, notebook chỉ gọi hàm.

### Trạng thái hiện tại của code

Toàn bộ `src/shotquality/*` (trừ `config.py`) là **stub `raise NotImplementedError("T1.3a @thong")`** — mã task
trong thông báo lỗi trỏ thẳng tới thẻ kanban tương ứng. `config.py` là code thật và đã chạy được.

Test được viết trước (TDD) với `pytestmark = pytest.mark.xfail(raises=NotImplementedError)`. Nhờ đó `pytest`
xanh từ ngày 0; khi một hàm được implement, test chuyển thành **XPASS** — đó là tín hiệu xoá marker `xfail`
của module đó.

## Quy ước

**Mã task `T<task>.<subtask>`** (ví dụ `T1.3b`) là khoá liên kết xuyên suốt: `docs/PLAN.md` ↔ thẻ trong
`docs/board/` ↔ docstring trong code ↔ commit message. Khi làm việc, luôn nêu mã task.

**Commit:** `<type>(<module>): <mã task> <mô tả>` — ví dụ `feat(features): T1.3b thêm angle_to_goal`.

**Hằng số:** lấy hết từ `config.py`, không hardcode đường dẫn/tham số ở nơi khác.

**Quyết định kỹ thuật:** mọi lựa chọn ảnh hưởng kết quả phải ghi thành ADR trong `docs/DECISIONS.md`
(đã có ADR-001…011). Khi được hỏi "tại sao lại làm thế này", đọc file đó trước.

## Bốn cạm bẫy dữ liệu StatsBomb (đã kiểm chứng trên Euro 2024)

**① Boolean chỉ tồn tại trong JSON khi `True`.** `under_pressure` chỉ có ở 387/1304 shot, `one_on_one` 52,
`open_goal` 9. `pd.json_normalize` sinh `NaN` → bắt buộc `.fillna(0)` cho toàn bộ `config.BOOL_FLAGS`.
Quên bước này thì `dropna()` xoá ~70% dữ liệu.

**② Penalty tạo cụm suy biến.** Mọi penalty ở cùng một toạ độ, xG cố định ~0.78 → K-Means dành hẳn một cụm
vô nghĩa và bóp méo cả Elbow lẫn Silhouette. Lọc `shot.type.name == "Penalty"` và `period == 5` (luân lưu).

**③ `match_id` không nằm trong events JSON** — phải lấy từ tên file.

**④ Encoding.** Tên cầu thủ có dấu (Pavel Šulc, João Cancelo). Đọc JSON `encoding="utf-8"`, ghi CSV
`config.CSV_ENCODING` (utf-8-sig). Mọi I/O đi qua `io_utils.py` để thống nhất.

Thêm: `shot.freeze_frame` nằm ngay trong event Shot, **không phụ thuộc 360 data** (ADR-008) — Euro 2024 có
1304/1304 shot chứa freeze_frame. Đừng giới hạn việc chọn giải theo `match_available_360`.

## Đọc thêm

`docs/PLAN.md` (kế hoạch 4 ngày, gate, danh sách descope) · `docs/STRUCTURE.md` (ma trận sở hữu đầy đủ) ·
`docs/WORKFLOW.md` (git + hệ thống tag kanban) · `docs/DATA_CONTRACT.md` (schema, công thức `angle_to_goal`) ·
`docs/DECISIONS.md` (11 ADR) · `docs/STATE.md` (trạng thái hiện tại, do LEAD cập nhật).
