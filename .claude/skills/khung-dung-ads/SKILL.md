---
name: khung-dung-ads
description: Lên khung dựng (bảng dựng từng cảnh) cho video ads Sube từ kịch bản + mã SP, dùng được cho mọi mã. Lấy TA + insight của SP bằng skill insight-bear trên Sube Hub, đánh dấu cảnh phải thể hiện khoảnh khắc / nỗi đau của khách, rồi ra bảng từng cảnh có hình ảnh, lời đọc, chữ trên hình, insight gắn với cảnh, loại source cần lấy, vị trí hook / ưu đãi / CTA. Editor nhìn vào là dựng được. Dùng khi ai trong team Media đưa kịch bản (ảnh Lark Sheet, bảng dán, file Excel/CSV, đoạn chữ) kèm mã SP và nhờ "lên khung dựng", "lên bảng dựng", "phân cảnh", "chia cảnh", "bóc kịch bản ra cảnh", "kịch bản này dựng thế nào", "cảnh nào cần source gì", kể cả khi chỉ gửi kịch bản mà không nói rõ, hoặc gửi nhiều kịch bản một lúc.
---

# Lên khung dựng từ kịch bản

**Làm gì:** biến kịch bản thành **bảng dựng từng cảnh** để Editor dựng ngay, không phải hỏi lại người viết kịch bản. Mỗi cảnh ghi rõ nó chạm vào insight nào của khách, để video không dựng chung chung.

**Dùng khi:** đã có kịch bản + mã SP, **trước khi** quay bổ sung / thu voice, hoặc ngay sau khi có voice. Dùng được cho **mọi mã SP**, không cần kho source đã lập chỉ mục.

**Không dùng để:** đào insight (dùng `insight-bear`), viết kịch bản mới, xử lý voice, cắt clip.

**Đầu ra:** mỗi kịch bản 1 bảng dựng theo mẫu `templates/bang-dung.md`. Không giới hạn số kịch bản: đưa bao nhiêu kịch bản thì ra bấy nhiêu bảng, dùng chung 1 lần chạy `insight-bear` nếu cùng mã.

---

## Bước 0. Gom đầu vào (thiếu thì hỏi 1 câu, gom hết chỗ thiếu vào câu đó)

| Đầu vào | Bắt buộc | Ghi chú |
|---|---|---|
| Kịch bản | Có | Hay gặp: **3 cột** (Phần / Mô tả cảnh / Voice), **5 cột** (Phần / Hành động / Voice over / Text Overlay / Note), hoặc **chỉ cột Voice**. Ảnh chụp đọc được |
| Mã + tên SP | Có | Để chạy `insight-bear` |
| Kết quả `insight-bear` của mã này | Không | Có sẵn thì dùng luôn, không chạy lại |
| Thông tin SP, lời khách thật | Không | Đưa cho `insight-bear`. Không có thì `insight-bear` vẫn chạy, ghi nguồn "suy luận" |
| Voice đã thu | Không | Chưa có voice thì bảng **không có cột Giây**, chỉ có lời đọc. Có voice thì thêm cột Giây đo theo voice thật |

Báo thời gian trước khi làm: chạy `insight-bear` khoảng 5–10 phút, bảng dựng 1 kịch bản ~60s khoảng 5–8 phút.

## Bước 1. Lấy TA + insight bằng `insight-bear`

1. Gọi `get_skill("insight-bear")` trên Sube Hub, làm **đúng theo bản vừa lấy về** (không dùng bản nhớ).
2. Chạy với mã SP. Mặc định 3 nhóm khách. Kết quả có:
   - **Nhóm khách N1, N2, N3…**: mỗi nhóm có *Bối cảnh* (khoảnh khắc cụ thể) và *Câu nói thầm*.
   - **Insight I1, I2…**: mỗi insight có *Loại* (Nỗi đau / Mong muốn / Rào cản mua / Rào cản dùng / So sánh / Tâm lý), *Mâu thuẫn*, *Động lực thầm kín*, *Góc nội dung*.
3. Đặt **Bảng tóm tắt** của `insight-bear` lên đầu bảng dựng. Mọi cảnh bên dưới chỉ được gắn về các mã I/N trong bảng này.
4. Đọc mục *Soát thông tin SP* của `insight-bear`: chỗ nào đụng tới kịch bản (claim lạ, thông số "cần kiểm") thì chép vào phần "Cần xem" cuối bảng dựng.

> `insight-bear` không chạy được (chưa có quyền, Hub lỗi): hỏi người dùng TA + 2–3 nỗi đau cụ thể, ghi theo cùng khuôn I1, I2… với `Nguồn: nhập tay`. Bước 2–4 giữ nguyên.

## Bước 2. Gắn từng câu voice vào insight, chọn cảnh khoảnh khắc

(Làm theo từng câu để không sót insight; sang bước 3 mới gom câu thành cảnh. Một cảnh chạm 2 insight thì ghi `I1 → I2` theo thứ tự lời đọc.)

Tách kịch bản theo câu / cụm ý của voice, rồi với mỗi cụm hỏi: câu này **chạm** insight nào?

| Câu voice nói về | Lấy từ `insight-bear` | Hình phải thể hiện |
|---|---|---|
| Cái khổ hiện tại, khoảnh khắc đau | *Bối cảnh* của nhóm + *Mâu thuẫn* của insight Loại Nỗi đau | **Đúng khoảnh khắc** trong *Bối cảnh*, ghi ngắn. Đồ vật → **cận vào vấn đề** (bát dính, ấm đun lại). Cảm xúc → **cảnh người** (mẹ ngủ gật, bé khóc) |
| Sản phẩm, tính năng | *Mâu thuẫn* mà tính năng đó gỡ | **Hình trám SP**: cận SP đang làm đúng việc voice nói (vd "Pha trà bằng bình thủy điện"). Ghi "gỡ I_" ở cột insight, **không** dựng tình huống người để minh hoạ insight |
| Cảm xúc sau khi dùng (câu không nhắc SP / tính năng) | *Động lực thầm kín* | Cảnh **người được hưởng**: con ăn ngon, mẹ thảnh thơi. Câu vẫn nhắc SP thì dùng hình trám SP |
| Lo ngại khi mua / khi dùng | Insight Loại Rào cản mua / Rào cản dùng | Cảnh **bằng chứng**: thao tác an toàn, đồng hồ bấm giờ, chứng nhận, so sánh cũ/mới |
| Con số (8 giây, 5L, 45–95°C, 18 tháng) | theo ý câu | Hình **phải cho thấy con số**: đồng hồ, màn hình máy, vạch dung tích |

- **Hook + nỗi đau** (từ cảnh 1 đến lúc SP xuất hiện): mọi cảnh phải gắn một insight Loại *Nỗi đau* hoặc *Tâm lý*. Riêng hook dạng **thách thức / thí nghiệm** ("8 giây thật không?") gắn insight *Rào cản mua* mà cả video sẽ chứng minh. Đây là phần giữ người xem.
- **Ưu tiên hình sản phẩm** (Yan chốt 25/11): từ lúc SP xuất hiện, câu nào nói về SP / tính năng thì dùng **hình trám SP**, nhiều hình trám. Cảnh có người chỉ dùng cho đoạn nỗi đau ở đầu và câu thuần cảm xúc.
- *Góc nội dung* của `insight-bear` dùng cho đoạn **nỗi đau** (trước khi SP xuất hiện). Sang đoạn SP thì không lấy *Góc nội dung* có người làm hình.
- *Câu nói thầm* dùng làm chữ trên hình cảnh hook **chỉ khi** voice nói đúng ý đó.
- Câu không chạm insight nào: ghi `—`. Hơn ~1/4 số cảnh là `—` thì kịch bản đang lệch insight: báo người dùng, chỉ ra đoạn nào.
- Kịch bản có nỗi đau mà `insight-bear` không có: ghi `ngoài insight` và báo, không tự đẻ insight mới.

## Bước 3. Chia cảnh

**Mỗi cảnh = 1 hình ngắn đi với 1–2 cụm lời đọc.** Viết gọn, đủ để Editor biết lấy cảnh gì; chi tiết quay / dựng để Editor tự quyết.

Ví dụ đúng mức (Yan chốt 25/11, kịch bản M54):

| Lời đọc | Hình ảnh | Góc máy |
|---|---|---|
| Đã thiếu ngủ vì chăm con, mẹ còn phải tất bật đun nước, canh nhiệt độ | Mẹ bế bé ngủ gật, mệt mỏi | Trung |
| rồi chờ nước nguội mới pha được một bình sữa cho bé, | Bật ấm đun nước, đổ nước ra tay test nhiệt độ | Cận |
| nhất là những hôm con quấy khóc, đòi sữa ngay giữa đêm thì càng thêm sốt ruột. | Bé khóc | Cận |

- **Hình ảnh: 2–10 chữ**, ai làm gì. Không tả bối cảnh, ánh sáng, trang phục; không viết chuỗi nhiều bước.
- **Góc máy: 1 góc chính** (thang ở bước 4).
- Gom các cụm voice liền nhau vào 1 cảnh khi dùng chung 1 hình; hình đổi thì tách cảnh. Không chia vụn mỗi dấu phẩy 1 cảnh.
- Một kịch bản ~50–70 giây thường ra **12–16 cảnh**.
- **Không để 3 cảnh top-down liền nhau** (Yan duyệt 22/11).
- **Không ghi giây khi chưa có voice.** Voice thật hay lược câu và đọc nhanh / chậm khác kịch bản, giây đoán trước sẽ sai. Có voice rồi thì thêm cột Giây (từ–đến) sau cột Cảnh, đo theo voice.

## Bước 4. Điền bảng dựng

| Cột | Cách điền |
|---|---|
| **Cảnh** | 01, 02… |
| **Giây** | Chỉ có khi đã có voice: từ–đến, đo theo voice thật |
| **Hình ảnh** | 2–10 chữ, ai làm gì. Viết "Bé khóc", "Bé bấm nút, nước không chảy" chứ không viết "show sản phẩm", cũng không tả bối cảnh chi tiết |
| **Góc máy** | Một trong: **Toàn** (thấy cả người + bối cảnh, vd mẹ trong phòng ngủ) · **Trung** (nửa người, hoặc SP + mặt bàn) · **Cận** (tay + vật, hoặc mặt) · **Đặc tả** (chi tiết nhỏ: lưỡi dao, số trên màn hình, giọt nước) · **Top-down** (máy quay nhìn thẳng từ trên xuống). Ghi 1 góc chính |
| **Lời đọc** | Chép đúng đoạn voice của cảnh (có thể nhiều câu) |
| **Chữ trên hình** | **Rút từ khoá, 2–6 chữ**, giữ con số. Không chép nguyên lời đọc. Tên SP + mã ở cảnh SP xuất hiện. Nhãn ✅ cộng dồn qua các tính năng liền nhau. Kịch bản có cột Text Overlay thì lấy từ đó |
| **Khoảnh khắc / nỗi đau** | `I_ · 2–5 chữ`. Ví dụ `I1 · chờ nước nguội`, `gỡ I4 · con táy máy`. Cảnh không chạm insight ghi `—` |
| **Source** | Một trong 5 loại dưới đây |
| **Hook / Ưu đãi / CTA** | `HOOK`, `SP XUẤT HIỆN`, `ƯU ĐÃI: <ý>`, `CTA` |

**5 loại source** (không cần biết trước kho có gì; Editor đối chiếu kho của mã):

| Loại | Khi nào | Ví dụ |
|---|---|---|
| `CÓ SẴN` | Cảnh SP: hero, demo tính năng, thành phẩm. Thường đã quay khi ra mã | Lắp cối, bấm nút, màn hình nhiệt độ, đổ cháo ra bát |
| `QUAY RIÊNG` | Hook KOL / VJ nói, vlog, "nổ inbox": quay theo từng video | KOL cầm SP nói câu hook |
| `UGC` | Cảnh đời thường quay điện thoại: mẹ con, bé ăn, đêm | Bé ăn cháo, mẹ bế con ngồi giường |
| `QUAY MỚI` | Kịch bản cần mà gần như chắc kho không có: khoảnh khắc nỗi đau cụ thể, cảnh có người dùng SP trong bối cảnh nhà | Mẹ đứng bếp lắc bình 2h sáng |
| `ĐỒ HOẠ` | **Cách cuối**, chỉ khi không quay được: vi khuẩn, so sánh số liệu. Tính năng "vô hình" (tự ngắt, khoá, chống tràn) thì quay **kết quả của nó** trên SP thật, không dùng đồ hoạ | Hiệu ứng vi khuẩn trên bình sữa |

Cảnh `CÓ SẴN` mà chưa chắc kho có góc đó thì thêm `⚠`. Cuối bảng gom các cảnh `QUAY MỚI` theo bối cảnh (chỉ ghi bối cảnh + số cảnh) để quay một lượt.

**Vị trí cố định (đo trên 7 video Sube đã chạy, ghi theo cảnh):**
- **HOOK:** câu đầu của voice, **cảnh 01–02** (2–5 giây đầu khi lên video).
- **Hook + nỗi đau:** từ cảnh 01 đến hết đoạn nỗi đau, thường **2–4 cảnh** (khoảng 10 giây đầu).
- **SP XUẤT HIỆN:** cảnh ngay sau đoạn nỗi đau, câu voice đầu tiên gọi tên SP, thường **cảnh 03–05**. Hook KOL cầm SP thì SP xuất hiện sớm hơn. Cảnh hero có tên SP + mã.
- **ƯU ĐÃI + CTA:** **2–4 cảnh cuối**. Một cảnh có thể chứa 2 ý khuyến mãi, mỗi ý 1 sticker hiện lần lượt theo lời đọc:

| Voice nói | Sticker |
|---|---|
| giảm X% | -X% |
| voucher X | Voucher X |
| freeship, miễn phí vận chuyển, giao hoả tốc | Free shipping |
| bảo hành X tháng | Bảo hành X tháng |
| 1 đổi 1 trong X ngày | 1 đổi 1 trong X ngày |
| cho X khách đầu tiên | Chỉ X khách đầu tiên |
| tặng kèm | 🎁 Tặng kèm… |
| mua tại fanpage | Deal hời tại fanpage |
| giỏ hàng góc trái (TikTok / Shopee) | Chốt đơn tại đây + mũi tên ↙ |
| nhắn tin Fanpage, nhấn góc phải để tư vấn (Facebook) | Nhắn tin ngay + mũi tên theo đúng góc voice nói |

Voice không nói ý nào thì **không** đặt sticker đó. 7 video mẫu không chèn ưu đãi giữa video; kịch bản có thì làm theo kịch bản.

## Bước 5. Soát trước khi giao

- [ ] Bảng tóm tắt `insight-bear` ở đầu, ghi ngày chạy và nguồn (lời khách thật / suy luận).
- [ ] Mọi cảnh từ cảnh 1 đến lúc SP xuất hiện đều gắn insight Nỗi đau / Tâm lý (hook thách thức: Rào cản mua).
- [ ] Mỗi insight của `insight-bear` mà kịch bản có nhắc đều có ít nhất 1 cảnh thể hiện.
- [ ] Cảnh có số liệu thì hình cho thấy số liệu.
- [ ] Từ lúc SP xuất hiện: câu nói về SP / tính năng đều là hình trám SP, không phải tình huống người.
- [ ] Mỗi cảnh 1 hình ngắn (2–10 chữ) + 1 góc máy; không chia vụn, không tả quá chi tiết (thường 12–16 cảnh).
- [ ] Không có 3 cảnh top-down liền nhau.
- [ ] Sticker CTA khớp từng ý khuyến mãi trong voice, đúng hướng mũi tên.
- [ ] Có phần **Cần xem**: cảnh `QUAY MỚI`, `⚠`, claim lạ, từ bị luật lời của `insight-bear` cấm ("duy nhất", "tuyệt đối", "100%"…) mà kịch bản đang dùng.

Giao xong, hỏi người dùng cảnh nào phải sửa và vì sao; ghi vào `test-log.md`. Lỗi lặp từ 2 lần thì đưa vào "Chỗ hay sai". Người dùng sửa kết quả thì hỏi có muốn gửi đề xuất cải tiến skill lên Sube Hub không.

---

## Chỗ hay sai

Rút từ video Yan đã dựng (045KN V3, 5H02D24 "Thí nghiệm 8 giây") và lần chạy thử EWB-5H50M54.

| # | Sai | Ví dụ thật | Làm đúng |
|---|---|---|---|
| 1 | Cột insight ghi chung chung ("mẹ bận rộn", "an toàn cho bé") | Không chứng minh được cảnh bám insight | Ghi mã I/N + khoảnh khắc cụ thể lấy từ *Bối cảnh* |
| 2 | Theo đúng chữ "Mô tả cảnh" dù voice có từ khoá cụ thể hơn | 045KN V3: kịch bản ghi "Trám bảng điều khiển", voice nói "nấc độ thô 8–10 tháng, trên 11 tháng" → Yan dùng 3 bát cháo 3 độ thô | **Từ khoá cụ thể trong voice thắng mô tả chung** |
| 3 | Ghi cảnh mà không ai có source | 045KN: "em bé không chịu ăn", "máy đang nấu"; D24: "nhấp nhả cháo", "em bé > 11 tháng" → Yan phải thay lúc dựng | Đánh `QUAY MỚI` hoặc `⚠` và ghi cảnh thay thế ngay trong bảng |
| 4 | Ghi giây khi chưa có voice | Voice thật **lược câu** (045KN V3 bỏ "Có mẹ nào như em không") và **đọc nhanh hơn** (D24 phải gộp 2 cảnh tổng kết); Yan chốt 25/11: chưa có voice thì không cần giây | Chỉ ghi lời đọc; có voice mới thêm cột Giây |
| 5 | Đếm độ dài cảnh theo chữ viết | M54: "5H50M54", "50%", "45–95°C" viết 3 chữ, đọc 21 âm: cảnh tưởng ngắn mà đọc dài | Đếm theo cách đọc |
| 6 | Chép nguyên lời đọc vào chữ trên hình | Màn hình chật, trùng phụ đề | 2–6 chữ từ khoá, giữ con số |
| 7 | Cảnh nói số liệu nhưng hình không thấy số | "8 giây" mà không có đồng hồ | Chọn hình có con số; cảnh bấm giờ thì đồng hồ chạm số đúng lúc voice nói |
| 8 | Dùng cảnh mẹ con của mã khác mà lộ sản phẩm khác | M54: cảnh mẹ bế con ban đêm có sẵn nhưng trong khung có máy hâm sữa mã khác | Ghi `⚠ crop` hoặc `QUAY MỚI` |
| 9 | Dùng sticker CTA quen tay | CTA TikTok là giỏ hàng góc trái ↙; CTA Facebook M54 là "nhắn tin Fanpage", có bản "góc phải" | Đọc đúng voice, đúng kênh, đúng hướng |
| 10 | 3 cảnh top-down liền nhau | Hình lặp, người xem lướt | Xen Cận / Trung |
| 11 | Chia vụn, hoặc tả hình quá chi tiết | M54 lần 1 ra 26 cảnh (vụn); lần 2 gộp 12 cảnh nhưng ô Hình ảnh tả bối cảnh + chuỗi nhiều bước. Yan trả cả 2 lần (25/11), chốt mẫu "Bé khóc · Cận" | 1 hình ngắn + 1 góc máy cho 1–2 cụm lời đọc: M54 còn 14 cảnh |
| 12 | Dựng tình huống người cho câu nói về SP | M54 cảnh 06 "không cần mất công đun đi đun lại": skill lấy *Góc nội dung* của I3 ra "Ông pha trà, mẹ pha sữa"; Yan sửa thành **cận pha trà bằng bình thủy điện** (25/11) | Câu nói về SP → hình trám SP, cận SP đang dùng |
| 13 | Dùng đồ hoạ cho tính năng quay được | M54 cảnh 10 "tự động ngắt điện khi cạn nước hoặc quá nhiệt": skill ra "Đồ hoạ tự ngắt điện"; Yan sửa thành **bấm rót nước nhưng nước không ra** vì đã khoá / ngắt điện (25/11) | Quay kết quả của tính năng trên SP thật; đồ hoạ là cách cuối |

---

## Mẫu đầu ra tốt (việc thật)

- `examples/mau-tot-01.md`: **BFM-045KN V3**, kịch bản 3 cột, hook vlog kể chuyện, quy trình 3 bước.
- `examples/mau-tot-02.md`: **5H02D24 "Thí nghiệm 8 giây"**, kịch bản 5 cột có Text Overlay, hook VJ, thí nghiệm theo món.

Đọc 1 mẫu gần nhất với kịch bản đang làm trước khi viết bảng.

## Log chạy thử

Xem `test-log.md`. Kết quả chạy thử trên việc thật (kịch bản M54 bản mẹ bé, Yan duyệt 25/11): `chay-thu/M54-me-be/bang-dung.md` + `chay-thu/M54-me-be/insight-bear.md`.
