# Log chạy thử skill `khung-dung-ads` (Lên khung dựng)

> Mỗi lần chạy trên việc thật ghi 1 mục. Lỗi nào lặp lại từ 2 lần thì đưa vào mục "Chỗ hay sai" trong `SKILL.md`.

## Lần 0: rút quy tắc từ việc đã làm (25/11/2026)

| Mục | Nội dung |
|---|---|
| Tài liệu | 7 video Yan đã dựng của 3 mã (5H02D24 V1, V2, D24 "Thí nghiệm 8 giây"; 045KN V3, V4; 5H12V78 V5, V6) + 2 kịch bản gốc (045KN V3, D24) |
| Đo được | Tốc độ voice 5,2–5,5 âm tiết/giây (045KN V4 là 4,3 vì hook inbox có khoảng chờ). Cảnh trung bình 2,0–2,5s, ngắn nhất 0,3s, dài nhất 5,6s. Video 47–69s, 19–34 cảnh. Hook kết thúc ở 2,3–5,0s; SP xuất hiện ở 9,5–13,7s; CTA bắt đầu 5,3–10,8s trước khi hết. Không video nào chèn ưu đãi ở giữa |
| Lệch kịch bản → final | 045KN V3: 4/9 đoạn đổi cảnh so với kịch bản (thiếu source hoặc voice có từ khoá cụ thể hơn), 1 câu voice bị lược. D24: 3 chỗ thiếu source, 2 cảnh gộp vì voice nhanh |
| Đưa vào skill | Quy tắc ước giây, vị trí hook / SP / CTA, bẫy #2, #3, #4, #7 |

## Lần 1: bình thủy điện EWB-5H50M54, bản mẹ bé (25/11/2026)

| Mục | Nội dung |
|---|---|
| Kịch bản | Ảnh Yan gửi, chỉ có cột Voice over (5 đoạn), **chưa có voice** |
| Mã SP | EWB-5H50M54, mã mới: chưa có kho chỉ mục, chưa có quy tắc riêng |
| TA + insight | Chạy `insight-bear` phiên bản 1 (Sube Hub): 3 nhóm, 5 insight, nguồn suy luận (thông tin SP lấy từ kịch bản, chưa có Base, chưa có lời khách) |
| Thời gian | `insight-bear` ~10 phút, bảng dựng ~8 phút |
| Kết quả | 14 cảnh (bản 1: 26 cảnh vụn; bản 2: 12 cảnh nhưng tả quá chi tiết). Cả 5 insight đều có cảnh thể hiện; 3 cảnh đầu (trước khi SP xuất hiện) đều gắn I1; 2 cảnh CTA không gắn insight |
| File | `output/M54 mẹ bé/insight-bear.md`, `output/M54 mẹ bé/bang-dung.md` |

### Bản nháp đầu bị Yan trả lại (25/11/2026)

| Yan nói | Vì sao sai | Đã sửa trong skill |
|---|---|---|
| Skill phải dùng được cho **mọi mã**, không cần lập chỉ mục từng file | Bản đầu dựa vào kho chỉ mục và quy tắc riêng từng mã trong repo của Yan; người khác trong team không có | Bỏ phụ thuộc kho; cột Source đổi thành 5 loại chung: CÓ SẴN / QUAY RIÊNG / UGC / QUAY MỚI / ĐỒ HOẠ. Quy tắc rút từ 7 video được viết thẳng vào skill |
| Chưa có voice thì **không cần giây**, chỉ cần lời đọc | Giây ước tính theo âm tiết dễ lệch khi voice thật lược câu / đọc nhanh hơn | Bỏ cột Giây khi chưa có voice; vị trí hook / SP / CTA ghi theo số cảnh (đo lại trên 7 video: hook 1–3 cảnh, SP ở cảnh 6–9, CTA 1–6 cảnh). Có voice thì thêm cột Giây đo theo voice |
| Chia lại cột: **góc máy thành 1 cột riêng** (toàn, trung, cận…) | Góc máy nằm lẫn cuối câu Hình ảnh, Editor khó lọc cảnh theo góc, khó soát lặp góc | Thêm cột Góc máy sau Hình ảnh, thang: Toàn / Trung / Cận / Đặc tả / Top-down, máy quay di chuyển ghi `Trung → Cận`. Quy tắc lặp góc giữ đúng ý Yan duyệt 22/11: không 3 cảnh top-down liền nhau |
| Bảng cảnh **hơi vụn**, muốn tối ưu hơn về cảnh quay | Chia mỗi câu voice thành 1 cảnh (26 cảnh), nhiều cảnh cùng bối cảnh bị tách rời, ê-kíp phải dựng máy nhiều lần | Chia theo **cảnh quay** (cùng bối cảnh, hành động nối tiếp = 1 cảnh), Hình ảnh ghi diễn biến bằng →, Góc máy ghi các góc cần quay, cảnh quay lại bối cảnh cũ ghi "cùng bối cảnh cảnh _". M54: 26 → 12 cảnh, 3 bối cảnh quay mới. Mẫu 045KN: 34 → 14, D24: 22 → 10 |
| **Không cần quá chi tiết**: "con quấy khóc, đòi sữa giữa đêm…" → **Cận bé khóc**, vậy thôi | Bản gộp 12 cảnh tả bối cảnh in đậm + chuỗi nhiều bước bằng → + nhiều góc máy, đọc nặng | Mỗi cảnh 1 hình 2–10 chữ + 1 góc máy cho 1–2 cụm lời đọc; ví dụ của Yan đưa thẳng vào bước 3. M54: 14 cảnh; mẫu 045KN 16, D24 12 |
| Đã có `insight-bear` trên Sube Hub | Bản đầu dùng ô nhập tay TA + insight tự đặt mã N/M/R, **trùng mã N** với nhóm khách của `insight-bear` | Bước 1 gọi `get_skill("insight-bear")`; cột insight ghi theo đúng mã `I_ (N_)` của `insight-bear`; dùng *Bối cảnh*, *Mâu thuẫn*, *Động lực thầm kín*, *Góc nội dung* để chọn hình |

### Mình tự thấy khi chạy

| # | Chỗ vướng | Cách đã xử lý | Đã đưa vào skill |
|---|---|---|---|
| 1 | Số, mã SP, ký hiệu ("5H50M54", "50%", "45–95°C") đếm theo chữ viết thì cảnh tưởng ngắn mà đọc dài | Đếm theo cách đọc khi chia cảnh | Bước 3 + bẫy #5 |
| 2 | Kịch bản chỉ có cột Voice, không có Mô tả cảnh | Lấy *Góc nội dung* của `insight-bear` làm hình (cảnh 10: ông pha trà, mẹ pha sữa) | Bước 0, bước 2 |
| 3 | Mã mới chưa có kho: nhiều cảnh QUAY MỚI | Gom thành 3 bối cảnh quay | Bước 4 + mẫu bảng |
| 4 | Cảnh mẹ con ban đêm có sẵn của mã khác nhưng lộ sản phẩm khác | Ghi ⚠ crop | Bẫy #8 |
| 5 | CTA là **nhắn tin Fanpage**, không phải giỏ hàng góc trái; CTA dài ~14s vì 5 ý khuyến mãi | Bỏ mũi tên ↙, giữ theo kịch bản | Bảng sticker + bẫy #9 |
| 6 | `insight-bear` soát ra mức nhiệt thấp nhất 45°C chưa rõ khớp pha sữa; kịch bản có "duy nhất" (luật lời cấm) | Đưa vào phần Cần xem | Bước 1 mục 4, bước 5 |
| 7 | Hook D24 là dạng thách thức, gắn Rào cản mua chứ không phải Nỗi đau | Cho phép ngoại lệ này | Bước 2 |

### Kết luận

- Yan duyệt bản 14 cảnh ngày 25/11/2026 ("Đúng ý").
- Yan trả 4 lần, cả 4 đều về **cách làm**, không sửa nội dung từng cảnh: (1) phải dùng được cho mọi mã + lấy insight từ `insight-bear`; (2) chưa có voice thì bỏ giây; (3) tách cột góc máy; (4) không chia vụn, không tả quá chi tiết.
- Đã đưa vào skill: bước 1, bước 3 (ví dụ chuẩn của Yan), cột Góc máy, chỗ hay sai #4, #5, #8, #9, #11.
- Còn chờ: chạy `insight-bear` lại khi có Base "Thông tin SP" và lời khách thật của M54; lần chạy sau ghi thêm cảnh Yan sửa nội dung (nếu có).

### Cảnh Yan sửa (sau khi duyệt bản 14 cảnh)

| Cảnh | Skill ra | Yan sửa thành | Vì sao |
|---|---|---|---|
| 06 | Ông pha trà, mẹ pha sữa (lấy từ *Góc nội dung* I3) · Trung · QUAY MỚI | Cận pha trà bằng bình thủy điện | Ưu tiên hình sản phẩm; câu nói về SP thì dùng nhiều hình trám SP |

| 10 | Đồ hoạ tự ngắt điện · ĐỒ HOẠ | Bấm rót nước nhưng nước không ra (đã khoá trẻ em / ngắt điện) · Cận | Tính năng "vô hình" vẫn quay được bằng kết quả của nó trên SP thật; đồ hoạ là cách cuối |

Rà lại theo quy tắc mới, đổi thêm 4 cảnh cùng lỗi: 07 (bế con chạm nút → chạm nút, nước chảy vào bình sữa), 08 (bé ngủ yên → đèn ngủ của bình bật sáng), 09 (bé bấm nút → bấm khoá trẻ em trên bình), 13 (chồng đặt hàng → bình cạnh hộp SP). Cảnh quay mới giảm từ 10 xuống 5 (chỉ còn đoạn nỗi đau + đặt bình đầu giường + cảnh chốt). Đưa vào skill: bước 2 + chỗ hay sai #12; cảnh 10 → bảng 5 loại source (ĐỒ HOẠ là cách cuối) + chỗ hay sai #13.
