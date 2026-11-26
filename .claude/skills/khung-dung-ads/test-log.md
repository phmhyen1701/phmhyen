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
| File | `chay-thu/M54-me-be/insight-bear.md`, `chay-thu/M54-me-be/bang-dung.md` (bản Yan duyệt) |

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

## Lần 2: Bear V78 "Bé thứ 2 chỉ tốn hơn 1 củ" (25/11/2026)

| Mục | Nội dung |
|---|---|
| Kịch bản | Ảnh Yan gửi, **2 cột** (Cảnh quay / Voice), 7 dòng, chưa có voice |
| Mã SP | WW-5H12V78 |
| TA + insight | `insight-bear` **phiên bản 2** (chạy lại 26/11/2026): thông tin SP từ Base "Hồ sơ sản phẩm B2C" qua công cụ Sube Hub `ho_so_san_pham`; 3 nhóm, 4 insight; chưa có lời khách → suy luận trên thông tin SP. (Bản 25/11 dùng phiên bản 1, thông tin SP từ kịch bản + ghi chú 2 video cũ) |
| Kết quả | 14 cảnh. Cả 4 insight đều có cảnh thể hiện; 3 cảnh trước khi SP xuất hiện đều gắn I1; 1 cảnh CTA không gắn insight. 6 cảnh VJ quay riêng, 1 cảnh có sẵn cần kiểm kho |
| Cần xem nổi bật | Base **không có "FDA US"** (chỉ có chất liệu chuẩn y tế); "72 tiếng" Base xác nhận; câu so sánh "không nhiều máy làm được" không có căn cứ Base; hook "hơn 1 củ" chỉ khớp giá min TMĐT 1,59 triệu (niêm yết 2,59 triệu) |
| Đổi khi chạy lại theo Base (26/11) | Insight: **I2** đổi từ "không biết tin vào đâu, cần giấy kiểm nghiệm" sang "không phân biệt được chất liệu, sợ mùi nhựa, bình ố vàng" (Base: thủy tinh không chì, inox 316, silicone không keo dán; hơi nước hạn chế vàng bình hơn UV); N2, N3 thêm chi tiết bối cảnh; I3, I4 thêm căn cứ Base (bảng cảm ứng nghiêng, 2 vùng chạy cùng lúc). Bảng dựng: cảnh **08** hình → "Cận bình thủy tinh, mâm inox", chữ "Kiểm nghiệm FDA US + Ping giấy kiểm nghiệm" → "Thủy tinh không chì · Inox 316"; cảnh 04 mã đủ WW-5H12V78; cảnh 06, 07, 09 sửa nhãn insight. Cần xem: thêm 08 (FDA, "toàn bộ"), 11 ("chuẩn kiểm nghiệm"), từ Base cấm, giá, phía khoang ở 06 |
| File | `chay-thu/V78-be-thu-2/` |

## Lần 3: Nồi lẩu NL05F "Lẩu cho nhà 3 thế hệ" (25/11/2026)

| Mục | Nội dung |
|---|---|
| Kịch bản | Ảnh Yan gửi, 2 cột, 6 dòng, chưa có voice |
| Mã SP | NL05F, mã mới, không có thông tin SP nào ngoài kịch bản |
| TA + insight | `insight-bear` **phiên bản 2** (chạy lại 26/11/2026): thông tin SP từ Base "Hồ sơ sản phẩm B2C" qua công cụ Sube Hub `ho_so_san_pham`; 3 nhóm, 4 insight; chưa có lời khách → suy luận trên thông tin SP. (Bản 25/11 dùng phiên bản 1, thông tin SP chỉ có trong kịch bản) |
| Kết quả | 12 cảnh. Cả 4 insight đều có cảnh thể hiện; 2 cảnh CTA không gắn insight. Hook đặt SP ngay cảnh 01, nỗi đau ở 02–03 (khác vị trí thường gặp, giữ theo kịch bản) |
| Cần xem nổi bật | Base xác nhận 5L, 3–6 người, chiên/xào/canh/hầm, nồi rời đế bếp; **Base cấm ngâm đế nồi vào nước** (đụng cảnh rửa 08); câu so sánh "an toàn hơn nồi liền thân" không có căn cứ Base; "-50%" giá niêm yết thấp hơn giá min TMĐT; "giảm nửa giá 50%" lặp ý |
| Đổi khi chạy lại theo Base (26/11) | Insight: **I4** đổi từ "rửa nồi thoải mái, sợ nước vào điện" sang "ăn xong dọn nhanh, nhấc nồi khỏi đế rửa riêng, không ngâm" (Base: lòng nồi chống dính, đế hồng ngoại rời; cấm ngâm đế); N3 thêm bối cảnh; I2 có căn cứ 1500W; I3 bỏ ý hấp (Base: không có xửng). Bảng dựng: cảnh **05** chữ → "1500W bắt nhiệt nhanh"; cảnh **07** hình → "VJ nhấc nồi khỏi đế bếp", chữ → "Nồi nhấc rời đế"; cảnh **08** chữ "không lo nước vào điện" → "Rửa riêng, chống dính". Cần xem: bỏ dòng "cả bảng chờ Base"; thêm không ngâm nồi (08), 07, 05, không hấp (09), giá -50% (11), gợi ý bảo hành 18 tháng |
| File | `chay-thu/NL05F-lau-3-the-he/` |

### Mình tự thấy khi chạy lần 2–3 (gặp ở cả 2 kịch bản → đã đưa vào skill)

| # | Chỗ skill chưa ghi | Đã sửa |
|---|---|---|
| 1 | Kịch bản dạng 2 cột Cảnh quay / Voice | Bước 0: thêm dạng 2 cột; cột cảnh quay có sẵn là khung chính |
| 2 | Chữ "Ping" (ảnh nổi lên trên hình) | Bước 0 giải nghĩa; bước 4 ghi `Ping ảnh: …` ở cột Chữ trên hình |
| 3 | VJ thao tác SP ở thân video, không chỉ hook | Bảng source: `QUAY RIÊNG` gồm cả cảnh VJ ở thân video |

### Cảnh Yan sửa (chờ Yan soát)

| KB | Cảnh | Skill ra | Yan sửa thành | Vì sao |
|---|---|---|---|---|
| | | | | |

