# Trạng thái Project

> LEAD (**Phong**) cập nhật file này sau standup 09:00 mỗi ngày. Thành viên **không sửa** file này —
> trạng thái công việc cá nhân cập nhật ở `docs/board/{tên}.md`.

**Cập nhật lần cuối:** _(chưa bắt đầu)_
**Ngày hiện tại:** D0 — chuẩn bị
**Gate gần nhất:** 🚦 GATE 1 — cuối Ngày 1

---

## 1. Bảng điều khiển

| Hạng mục | Trạng thái |
|---|---|
| Phạm vi dữ liệu | ✅ Đã chốt — World Cup 2018 + WC 2022, 128 trận |
| Data contract | 🟡 DRAFT (đóng băng tại GATE 1) |
| `shots_raw.csv` | ⬜ chưa có |
| `X_scaled` / `X_unscaled` | ⬜ chưa có |
| Nhãn cụm | ⬜ chưa có |
| Kết quả CV | ⬜ chưa có |
| Report | ⬜ chưa có |

## 2. Tiến độ theo gate

| Gate | Hạn | Trạng thái | Ghi chú |
|---|---|---|---|
| GATE 1 — `shots_raw.csv` + contract FROZEN | D1 18:00 | ⬜ | |
| GATE 2 — `X_*.csv` + harness pass synthetic | D2 18:00 | ⬜ | |
| GATE 3 — labels + ARI + CV accuracy | D3 18:00 | ⬜ | |
| GATE 4 — report hoàn chỉnh | D4 16:00 | ⬜ | |

Ký hiệu: ⬜ chưa tới · 🟡 đang làm · ✅ đạt · 🔴 trễ (kích hoạt descope)

## 3. Số liệu chốt (điền dần)

| Chỉ số | Giá trị | Nguồn |
|---|---|---|
| Số shot sau lọc | — | T1 |
| Goal rate | — | T2 |
| Số feature trong `X` | — | T3.6 |
| k chọn bởi Elbow / Silhouette / Gap (unscaled) | — / — / — | T5.1 |
| k chọn bởi Elbow / Silhouette / Gap (scaled) | — / — / — | T5.2 |
| **ARI** scaled vs unscaled | — | T5.3 |
| Silhouette nhánh chốt | — | T5.4 |
| **KNN CV accuracy ± std** | — | T5.5 |
| Cụm có goal rate cao nhất | — | T6.2 |

> Tham chiếu đối chiếu (đo sẵn trên World Cup 2018, chưa gộp WC 2022):
> 1.304 shot hợp lệ · goal rate 7,5% · Right Foot 676 / Left Foot 393 / Head 228 / Other 7 ·
> freeze_frame thiếu 0.

## 4. Rủi ro đang theo dõi

| Rủi ro | Mức | Dấu hiệu sớm | Phản ứng |
|---|---|---|---|
| Tải 128 file events chậm/lỗi mạng | Trung bình | GATE 1 trễ > 2h | Descope: bỏ WC 2022, chỉ dùng World Cup 2018 |
| Parse `freeze_frame` phức tạp hơn dự kiến | Cao | C chưa xong cuối D1 | Descope: bỏ nhóm feature freeze_frame |
| Gap Statistic khó implement đúng | Trung bình | C tắc ở D2 | Descope: giữ Elbow + Silhouette |
| 3 phương pháp chọn K không đồng thuận | Thấp | — | **Không phải lỗi** — đây là insight, phân tích trong report |
| Cụm không khớp thứ tự goal rate/xG | Trung bình | T6.2 | Ghi vào phần *hạn chế*, thử lại với k khác |

## 5. Nhật ký standup

### D1 — _(chưa diễn ra)_
| Người | Hôm qua | Hôm nay | Blocked |
|---|---|---|---|
| Phong | — | | |
| Thông | — | | |
| Lộc | — | | |
