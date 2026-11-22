# Quy tắc chung: dựng video ads Sube

> Áp dụng cho **mọi mã sản phẩm**. Phần riêng của từng mã (từ khoá → nhóm source, overlay) nằm ở `rules/sp/<mã>.md`.
> Rút ra từ 2 video mẫu của mã 5H02D24 (22/11/2026). Gặp mã mới có cấu trúc khác thì cập nhật file này.

## 1. Khung video

| Phần | Thời lượng | Số cảnh | Nội dung hình |
|---|---|---|---|
| Hook | 3–5s | 1–2 | KOL nói trước máy quay (**quay riêng từng video, Yan đưa file**) hoặc B-roll lấy từ nhóm PAIN_* của SP |
| Nỗi đau | 3–9s | 2–4 | Minh hoạ đúng vấn đề khách gặp khi chưa có SP |
| Giới thiệu SP | ~2–3s | 1 | **Hero shot SP**, luôn có tên SP + mã |
| Tính năng | 20–28s | 8–12 | Mỗi tính năng một nhóm source (xem file SP) |
| Lợi ích/CTA | 7–9s | 2 | SP + thành phẩm/kết quả dùng, nền studio, mũi tên đỏ chỉ xuống góc trái (giỏ hàng) |

- Chuyển từ nỗi đau sang SP có thể chèn thẻ ❌ (khoảng 0.3s) hoặc hiệu ứng loé sáng/trượt.
- Quy tắc chọn source chỉ áp dụng **từ sau hook KOL**.

## 2. Quy tắc cắt

- **Mỗi cảnh khớp với một cụm ý của voice.** Cắt đúng chỗ ngắt câu hoặc dấu phẩy, không cắt giữa từ.
- Độ dài cảnh: **1.1–5.3s, trung bình khoảng 2.3s**.
- Câu voice dài hơn 3.5s mà có 2 ý thì tách thành 2 cảnh.
- Cảnh demo kéo dài (bấm giờ, rửa, thao tác liên tục) được phép dài 3.5–5s.
- Cảnh CTA cuối dài nhất (4–5s), kéo đến hết voice.
- **Source là file quay dài:** chỉ lấy đúng đoạn hành động. Bỏ phần đầu/cuối lúc tay đưa vào/rút ra, máy quay rung hoặc lấy nét.

## 3. Nguyên tắc chọn source

- **Hình phải minh hoạ đúng nghĩa đen từ khoá trong câu voice.** Ví dụ voice nói số liệu (dung tích, thời gian) thì hình phải cho thấy số liệu đó: cầm cối, đồng hồ bấm giờ…
- Mỗi câu voice → tìm từ khoá → tra bảng "từ khoá → nhóm" trong file SP → chọn một source trong nhóm.
- Câu không có từ khoá nào khớp: dùng cảnh SP đang hoạt động hoặc cảnh ấn máy, và đánh dấu `can_xem` trong `edit_map.csv` để Yan kiểm tra.

## 4. Đa dạng hoá source

- Mỗi nhóm giữ nhiều source ứng viên.
- Ưu tiên source **chưa dùng ở video gần nhất**; hết ứng viên thì quay vòng.
- **Đồng bộ trong một video:** cùng một món/vật liệu xuyên suốt các cảnh demo (đã xay thịt thì cảnh sau cũng là thịt).
- Trong một video không dùng một đoạn source 2 lần. Lấy đoạn khác của cùng file thì được.
- Các nhóm cố định (hero, các tính năng chủ lực) được phép dùng lại giữa các video. Chỉ nên đổi bản quay khi có.

## 5. Phụ đề

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
| Kịch bản | Có | Biết danh sách tính năng, từ khoá |
| Folder source | Có | Lập chỉ mục một lần |
| Ghi chú đặc biệt | Không | Ngoại lệ so với quy tắc chung |
