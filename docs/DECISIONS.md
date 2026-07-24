# Nhật ký quyết định kỹ thuật (ADR)

Mỗi quyết định có ảnh hưởng tới kết quả hoặc cách làm việc đều phải ghi ở đây.
Khi bảo vệ report, đây là chỗ trả lời câu "tại sao nhóm chọn thế này?".

**Mẫu:** `ADR-xxx · Ngày · Trạng thái · Bối cảnh → Quyết định → Hệ quả`

---

## ADR-001 · D1 · ✅ Accepted — Chọn Euro 2024 + World Cup 2022

**Bối cảnh.** `hudl/open-data` có 80 cặp competition-season. Cần đủ mẫu cho K-Means (k≤10) và 5-fold CV,
đồng thời bối cảnh phải đồng nhất.

**Quyết định.** Dùng UEFA Euro 2024 (`55/282`, 51 trận) + FIFA World Cup 2022 (`43/106`, 64 trận) → ~2.600 shot.

**Lý do.**
- Cùng là giải quốc tế nam đỉnh cao → không lẫn confound "trình độ giải khác nhau".
- Cùng spec dữ liệu hiện đại.
- 115 file events (~350 MB) — tải được trong 1 buổi.
- Đã loại các phương án lệch mẫu: Bundesliga 23/24 chỉ 34 trận, MLS 2023 chỉ **6 trận**,
  La Liga 20/21 và Ligue 1 22/23 là subset xoay quanh Messi.

**Phương án thay thế đã cân nhắc.** Premier League 2015/16 (`2/27`) cho ~11.100 shot từ một giải một mùa
— đồng nhất hơn nữa, nhưng phải tải 380 file (~1 GB) và spec cũ hơn. **Giữ làm phương án mở rộng nếu dư thời gian.**

---

## ADR-002 · D1 · ✅ Accepted — Không clone toàn bộ repo open-data

**Bối cảnh.** `hudl/open-data` nặng **7.06 GB** (đo qua GitHub API).

**Quyết định.** Chỉ tải qua raw URL 3 loại file: `competitions.json`, `matches/{c}/{s}.json`,
và `events/{match_id}.json` của 115 trận đã chọn.

**Hệ quả.** Bỏ qua `data/three-sixty/` và `data/lineups/` — nơi chiếm phần lớn dung lượng.
Nếu vẫn muốn clone: `git clone --filter=blob:none --sparse` rồi `git sparse-checkout set data/events data/matches`.

---

## ADR-003 · D1 · ✅ Accepted — `shots_raw.csv` được commit, `data/raw/` thì không

**Bối cảnh.** 3 người cần cùng một dữ liệu để chạy song song từ Ngày 2.

**Quyết định.** `.gitignore` toàn bộ `data/raw/` (~350 MB), nhưng **commit** `data/interim/shots_raw.csv`
(~2.600 dòng, < 1 MB) và các file trong `data/processed/`.

**Hệ quả.** Ai clone repo cũng chạy được từ Task 2 trở đi mà không cần tải lại 350 MB.
Đây chính là điều kiện để Ngày 2 chạy song song 3 luồng.

---

## ADR-004 · D1 · ✅ Accepted — Loại penalty và loạt luân lưu

**Bối cảnh.** Euro 2024 có 36 penalty + 24 quả luân lưu (`period == 5`).

**Quyết định.** Lọc bỏ `shot.type.name == "Penalty"` và `period == 5`.

**Lý do.** Mọi penalty ở **cùng một toạ độ**, xG cố định ~0.78 → K-Means sẽ dành hẳn một cụm cho chúng.
Cụm đó không mang thông tin về "vùng sút" nào cả, mà còn bóp méo Elbow curve và Silhouette score.

**Hệ quả.** Euro 2024: 1.340 → **1.304** shot hợp lệ.

---

## ADR-005 · D1 · ✅ Accepted — Ghim phiên bản thư viện + `random_state=42`

**Bối cảnh.** K-Means khởi tạo ngẫu nhiên; 3 máy khác nhau dễ ra kết quả lệch nhau → không so sánh được.

**Quyết định.** Ghim cứng phiên bản trong `requirements.txt`; mọi hàm có yếu tố ngẫu nhiên đều nhận
`random_state = config.RANDOM_STATE = 42`; K-Means dùng `n_init=10`.

**Hệ quả.** Số liệu trong report tái lập được — điều kiện bắt buộc để Ngày 4 chạy lại pipeline mà vẫn khớp.

---

## ADR-006 · D1 · ✅ Accepted — Giấu `outcome`, `statsbomb_xg`, `end_location`

**Bối cảnh.** K-Means là unsupervised; đưa nhãn kết quả vào feature là data leakage.

**Quyết định.** 3 nhóm cột tách bạch: `X` / `Y_hidden` / `ID`. `preprocess.py` phải tách `Y_hidden` ra
file riêng ngay từ đầu, chỉ join lại ở Task 6.

**Lưu ý về `end_location`.** Nhiều người quên cột này — nó là vị trí bóng **sau khi sút** (vào lưới, ra ngoài…),
tức cũng là kết quả. Phải giấu cùng nhóm với `outcome`.

**Hệ quả.** Việc goal rate và xG trung bình xếp đúng thứ tự giữa các cụm trở thành **bằng chứng độc lập**
(external validation) chứ không phải hệ quả hiển nhiên.

---

## ADR-007 · D1 · ✅ Accepted — `angle_to_goal` dùng góc chắn 2 cột dọc

**Quyết định.** Dùng định lý cosin với 2 cột `(120, 36)` và `(120, 44)` thay vì góc tới tâm khung `(120, 40)`.

**Lý do.** Góc chắn phản ánh đúng "khung thành mở bao nhiêu" từ điểm sút — đây là feature chuẩn trong
các mô hình xG. Góc tới tâm không phân biệt được sút gần sát biên ngang với sút chính diện ở xa.

---

## ADR-008 · D1 · ✅ Accepted — Không cần 360 data để có `freeze_frame`

**Bối cảnh.** Kế hoạch ban đầu định giới hạn ở các giải có `match_available_360` để dùng `freeze_frame`.

**Quyết định.** Bỏ ràng buộc đó.

**Lý do.** `shot.freeze_frame` nằm **ngay trong chính event Shot**, độc lập với 360 data.
Kiểm chứng thực tế: Euro 2024 có **1304/1304** shot chứa `freeze_frame`; Premier League 2015/16
(không hề có 360) vẫn đạt 87/88.

**Hệ quả.** Tự do chọn giải theo kích thước mẫu; không phải tải thư mục `three-sixty/` (rất nặng).

---

## ADR-009 · D1 · ✅ Accepted — L2/Euclidean là biến **kiểm soát**, không phải biến thí nghiệm

**Quyết định.** Cố định distance metric = L2 cho cả K-Means lẫn KNN, ở **cả hai** nhánh scaled/unscaled.

**Lý do.** Thí nghiệm chỉ có một biến độc lập là *scaling*. Nếu đổi metric giữa hai nhánh thì không còn
quy được khác biệt cho scaling nữa.

**Hệ quả.** Report phải ghi rõ đây là điều kiện kiểm soát, tránh người đọc hiểu nhầm nhóm đang so sánh nhiều metric.

---

## ADR-010 · D1 · ✅ Accepted — Cả hai nhánh dùng chung `clustering.py`

**Bối cảnh.** Ngày 3, Phong chạy nhánh unscaled còn Thông chạy nhánh scaled.

**Quyết định.** Chỉ Thông sở hữu và sửa `clustering.py` + `selection.py`; Phong **gọi** hàm đó từ notebook của mình.

**Lý do kép.**
1. *Kỹ thuật:* hai người không sửa cùng file → không conflict.
2. *Khoa học:* hai nhánh đi qua **cùng một code path** → chênh lệch kết quả chắc chắn do scaling,
   không phải do implementation khác nhau.

---

## ADR-011 · D1 · ✅ Accepted — Cross-validation áp dụng gián tiếp qua KNN

**Bối cảnh.** CV vốn dành cho supervised learning, còn K-Means là unsupervised — không có nhãn thật để chia fold.

**Quyết định.** Lấy `cluster_id` do K-Means sinh ra làm nhãn giả, biến thành bài toán classification,
rồi chạy KNN + 5-fold CV trên cặp `(X, cluster_id)`.

**Diễn giải kết quả.** Accuracy cao ⇒ ranh giới cụm **nhất quán và tổng quát hoá được**, không phải
sản phẩm ngẫu nhiên của một lần khởi tạo. Accuracy thấp ⇒ cụm chồng lấn, cấu trúc yếu.

**Cảnh báo.** Đây **không** phải bằng chứng cụm "đúng" — nhãn vốn do chính K-Means sinh ra.
Bằng chứng về ý nghĩa thực tế phải lấy từ external validation ở Task 6.2 (goal rate + xG).

---

## Mẫu cho ADR tiếp theo

```markdown
## ADR-0xx · D? · 🟡 Proposed / ✅ Accepted / ❌ Superseded by ADR-0yy — Tiêu đề

**Bối cảnh.**
**Quyết định.**
**Lý do.**
**Hệ quả.**
```
