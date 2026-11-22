# Quy tắc chung: dựng video ads Sube

> Áp dụng cho **mọi mã sản phẩm**. Phần riêng của từng mã (từ khoá → nhóm source, overlay) nằm ở `rules/sp/<mã>.md`.
> Rút ra từ 6 video mẫu của 3 mã: 5H02D24, 045KN, 5H12V78 (22/11/2026). Gặp mã mới có cấu trúc khác thì cập nhật file này.

## 1. Khung video

| Phần | Thời lượng | Số cảnh | Nội dung hình |
|---|---|---|---|
| Hook + nỗi đau | 5–12s | 3–8 | Xem các kiểu hook bên dưới |
| Giới thiệu SP | ~2–4s | 1–2 | **Hero shot SP**, luôn có tên SP + mã |
| Thân video | 20–45s | 8–20 | Một trong các dạng thân bên dưới |
| Lợi ích/CTA | 5–10s | 2–6 | SP + thành phẩm hoặc cảnh mẹ con, mũi tên chỉ xuống góc trái (giỏ hàng) |

- Video dài 47–69s. Mã nhiều tính năng thì video dài hơn.
- Chuyển từ nỗi đau sang SP có thể chèn thẻ ❌ (khoảng 0.3s) hoặc hiệu ứng loé sáng/trượt.
- Quy tắc chọn source chỉ áp dụng **từ sau hook KOL**.

### Các kiểu hook đã gặp
| Kiểu | Mô tả | Ví dụ |
|---|---|---|
| KOL nói trước máy quay | Đặt câu hỏi gây tò mò, cầm SP lên | 5H02D24 V1 |
| B-roll nỗi đau | Cận cảnh vấn đề, không có người nói | 5H02D24 V2 |
| Vlog kể chuyện | KOL ở bếp nhà, tông tối viền phim, phụ đề trắng giữa màn hình | 045KN V3 |
| "Nổ inbox" | KOL cầm SP + chồng bong bóng chat câu hỏi của khách | 045KN V4 |
| UGC đời thường | Hình quay điện thoại: mẹ rửa bình, bé bú, mẹ thức đêm | 5H12V78 V5, V6 |

Hook KOL/vlog/inbox là **quay riêng từng video** (Yan đưa file). Hook B-roll/UGC thì lấy từ nhóm PAIN_* / LIFESTYLE_* trong kho.

### Các dạng thân video đã gặp
| Dạng | Cách dựng | Ví dụ |
|---|---|---|
| Danh sách tính năng | Mỗi tính năng 1–3 cảnh, nhãn ✅ cộng dồn | 5H02D24, 5H12V78 |
| Quy trình theo bước | Pill bậc thang có mũi tên, mỗi bước 1 cảnh top-down | 045KN |
| Hỏi–đáp (FAQ) | Mỗi đoạn mở bằng pill câu hỏi → cảnh demo trả lời | 045KN V4 |
| So sánh cũ/mới | Chia đôi màn hình, nhãn "Phiên bản mới / cũ" | 045KN V4 |
| Chia theo bộ phận | "Khoang trái / Khoang phải", ✅ cộng dồn riêng từng bộ phận | 5H12V78 V6 |

Một video có thể kết hợp nhiều dạng.

### CTA
- **Chọn lại source mỗi video**, vì chương trình khuyến mãi mỗi lần một khác.
- Cảnh: SP đứng riêng / SP + thành phẩm / tay đặt SP hoặc bát / cảnh mẹ con. Mỗi ý khuyến mãi một cảnh.
- **Sticker bám theo từng ý khuyến mãi trong voice:**

| Voice nói | Sticker |
|---|---|
| giảm X% | -X% |
| voucher X | Voucher X |
| freeship, giao hoả tốc | Free shipping |
| bảo hành X tháng | Bảo hành X tháng |
| tặng kèm | 🎁 Tặng kèm… |
| mua tại fanpage | Deal hời tại fanpage |
| giỏ hàng, góc trái, chốt | Chốt đơn tại đây + mũi tên ↙ |

Voice không nhắc ý nào thì không dùng sticker đó.

## 2. Quy tắc cắt

- **Mỗi cảnh khớp với một cụm ý của voice.** Cắt đúng chỗ ngắt câu hoặc dấu phẩy, không cắt giữa từ.
- Độ dài cảnh: **1–5s, trung bình 2.0–2.3s** (giống nhau ở cả 3 mã).
- Câu voice dài hơn 3.5s mà có 2 ý thì tách thành 2 cảnh.
- Cảnh demo kéo dài (bấm giờ, rửa, thao tác liên tục) được phép dài 3.5–5s.
- Cảnh CTA cuối dài nhất (4–5s), kéo đến hết voice.
- **Source là file quay dài:** chỉ lấy đúng đoạn hành động. Bỏ phần đầu/cuối lúc tay đưa vào/rút ra, máy quay rung hoặc lấy nét.

## 3. Nguyên tắc chọn source

### Thứ tự ưu tiên
1. **Cột "Mô tả cảnh" trong kịch bản** là khung chính: theo đúng thứ tự và ý của cột này. "Trám" = cảnh chèn (B-roll), "VJ" = người dẫn xuất hiện trong khung hình.
2. **Từ khoá cụ thể trong voice** thắng mô tả cảnh chung chung. Ví dụ kịch bản ghi "Trám bảng điều khiển" nhưng voice nói "nấc độ thô 8–10 tháng, trên 11 tháng" thì dùng cảnh 3 bát cháo 3 độ thô.
3. **Cảnh kịch bản yêu cầu mà kho không có** thì thay bằng cảnh minh hoạ từ khoá voice, và đánh dấu `can_xem`.
4. **Voice thu thực tế có thể lược bớt** so với kịch bản. Luôn căn theo voice thật.

### Khớp hình với voice
- **Hình phải minh hoạ đúng nghĩa đen từ khoá trong câu voice.** Ví dụ voice nói số liệu (dung tích, thời gian) thì hình phải cho thấy số liệu đó: cầm cối, đồng hồ bấm giờ…
- Mỗi câu voice → tìm từ khoá → tra bảng "từ khoá → nhóm" trong file SP → chọn một source trong nhóm.
- **Câu nói về cảm xúc/lợi ích** (giấc ngủ của mẹ, con ăn ngon, nhàn hơn) → dùng cảnh **LIFESTYLE**: em bé ăn, mẹ bế con, mẹ thức đêm.
- **Câu nói về chứng nhận/kiểm định** → dùng cảnh **bằng chứng**: ảnh giấy kiểm nghiệm có khoanh đỏ.
- **Câu nói về con số** (thời gian, dung tích, nhiệt độ, %) → hình phải cho thấy con số đó: đồng hồ bấm giờ, màn hình máy, nhãn số.
- Câu không có từ khoá nào khớp: dùng cảnh SP đang hoạt động hoặc cảnh ấn máy, và đánh dấu `can_xem` trong `edit_map.csv` để Yan kiểm tra.

## 4. Đa dạng hoá source

- Mỗi nhóm giữ nhiều source ứng viên.
- Ưu tiên source **chưa dùng ở video gần nhất**; hết ứng viên thì quay vòng.
- **Đồng bộ trong một video:** cùng một món/vật liệu xuyên suốt các cảnh demo (đã xay thịt thì cảnh sau cũng là thịt).
- Trong một video không dùng một đoạn source 2 lần. Lấy đoạn khác của cùng file thì được.
- Các nhóm cố định (hero, các tính năng chủ lực) được phép dùng lại giữa các video. Chỉ nên đổi bản quay khi có.

## 5. Phụ đề

- **Có phụ đề hay không tuỳ từng video, không tuỳ mã:**
  - Video **nhiều text overlay** (nhãn tính năng, pill câu hỏi, sticker): **không có phụ đề**.
  - Video **thuần storytelling** (kể chuyện, ít nhãn): **có phụ đề**.
  - Mình luôn xuất `.srt`, Yan quyết định có import hay không.
- Kiểu karaoke, 2–4 từ/dòng, đặt giữa phía dưới. Chữ trắng viền, một từ khoá to hơn, màu xanh lá/vàng.
- Xuất `.srt`: **chữ lấy từ kịch bản**, **thời gian lấy từ whisper** (`tools/make_srt.py`). Ngắt dòng ở dấu câu, tối đa 4 từ hoặc 1.6s.
- Yan import vào CapCut (Captions → Import) rồi áp style/animation hàng loạt. *Đang chờ Yan thử xem highlight theo từng từ có chạy với file .srt không.*

## 6. Nhãn overlay

- Kiểu nhãn dùng chung:
  - pill ✅ xanh lá, cộng dồn qua các tính năng liên tiếp
  - pill ❌ đỏ cho nỗi đau
  - chữ cong xanh lá bám theo vật thể
  - icon đồng hồ cho tốc độ
  - mũi tên/vòng tròn đỏ để chỉ chi tiết
  - tên SP chữ viết tay hồng/trắng ở cảnh hero, kết quả, CTA
- Yan lưu mỗi nhãn thành preset trong CapCut.
- Mình xuất `overlay_cues.csv` (thời điểm bắt đầu, kết thúc, tên nhãn) để Yan kéo preset vào.

## 7. Đầu vào cần cho một mã SP mới

| Đầu vào | Bắt buộc | Dùng để |
|---|---|---|
| 1–2 video final | Nên có | Soạn `rules/sp/<mã>.md` đúng gu chọn cảnh |
| Kịch bản (3 cột: Phần, Mô tả cảnh, Voice) | Có | Khung chọn cảnh + danh sách tính năng, từ khoá. Gửi dạng ảnh được; xuất Excel/CSV từ Lark Sheets thì chạy tự động tốt hơn |
| Folder source | Có | Lập chỉ mục một lần |
| Ghi chú đặc biệt | Không | Ngoại lệ so với quy tắc chung |
