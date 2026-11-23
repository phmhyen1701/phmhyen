---
name: xu-ly-voice-sub
description: Xử lý voice thô cho video ads Sube và tạo phụ đề .srt để kéo vào CapCut. Bỏ lần đọc lặp/đọc vấp, rút khoảng lặng, tăng tốc 1.07x, chuẩn -13 LUFS, xuất MP4 (hình đen + voice) và file sub 4–6 chữ/dòng. Dùng skill này mỗi khi Yan đưa file voice (.m4a/.wav/.mp3) và nhờ "xử lý voice", "làm sạch voice", "cắt voice", "voice theo tiêu chuẩn", "tạo sub", "làm phụ đề", "xuất srt", "subtext", "kéo vào CapCut", kể cả khi chỉ nói đường dẫn folder voice, hoặc nhờ sửa nhịp nghỉ / cách ngắt dòng của voice và sub đã làm.
---

# Xử lý voice + phụ đề cho ads Sube

Đầu vào: một file voice thô (thường là `.m4a` thu điện thoại, rất nhỏ ~-41 LUFS, có đọc lặp/đọc vấp), có hoặc không kèm kịch bản.
Đầu ra trong `output\<tên voice>\`:

| File | Dùng làm gì |
|---|---|
| `<tên>_voice.mp4` | Hình đen 1080x1920 + voice sạch, Yan kéo vào CapCut |
| `<tên>_sub.srt` | Phụ đề, Captions → Import trong CapCut |
| `voice_clean.wav` | Voice sạch chất lượng gốc |
| `loi_voice.txt` | Lời chuẩn có dấu `\|` ngắt dòng; Yan sửa chữ ở đây rồi xuất lại sub |
| `whisper.json`, `whisper_check.json`, `whisper_clean.json`, `voice_map.json` | Mốc thời gian, dùng cho bước dựng clip sau |

Tiêu chuẩn chi tiết nằm ở `rules/chung.md` mục 2 (làm sạch voice) và mục 5 (phụ đề). Công cụ đã để sẵn mặc định đúng chuẩn Yan chốt, nên **không truyền tham số khoảng nghỉ / số chữ** trừ khi Yan yêu cầu khác cho riêng video đó.

## Trước khi bắt đầu

- Báo Yan thời gian ước tính: voice ~1 phút mất khoảng 8–12 phút cả voice lẫn sub (mỗi lần whisper ~2–3 phút trên CPU).
- Không sửa/xoá file voice gốc. Mọi đầu ra ghi vào `output\<tên voice>\`.
- Chạy lệnh từ gốc repo bằng `py -3.12`. Trong Git Bash đặt `export PYTHONIOENCODING=utf-8` trước, nếu không `transcribe.py` sẽ lỗi `UnicodeEncodeError` khi in tiếng Việt.
- Có kịch bản thì đọc trước. Voice thật là chuẩn: câu kịch bản có mà voice không đọc thì bỏ.

## Bước 1: Whisper voice gốc

```bash
O="output/<tên voice>"; mkdir -p "$O"
py -3.12 tools/transcribe.py "<voice gốc>" "$O/whisper.json" --prompt "<tên SP + vài từ khoá riêng của SP>"
```

`--prompt` mặc định nói về máy xay. Đổi theo sản phẩm (ví dụ "Nồi Bear, nồi lẩu điện, chống dính, nấu cơm, hầm.") để whisper nghe đúng tên riêng.

## Bước 2: Soát lần đọc lặp / đọc vấp

Đây là bước dễ sót nhất: voice D24 có 4 chỗ lặp, lần đầu chỉ bắt được 1. Phải soát kỹ rồi mới cắt.

```bash
py -3.12 tools/soat_lap.py "<voice gốc>" "$O/whisper.json"
```

Đọc kết quả theo 3 dấu hiệu:
1. **Cặp câu liền nhau giống nhau** (mục 2 của báo cáo): đọc lại cả câu.
2. **Từ có `!!`** (kéo dài >0.9s) ở giữa câu: whisper đã gộp 2 lần đọc thành 1 từ dài. Từ cuối câu dài vì dính khoảng lặng thì bỏ qua.
3. **Câu cụt / lặp một phần**: ví dụ "Vỏ nồi cách nhiệt an toàn, ăn xong lại nhấc khay rời" rồi câu sau lại "Ăn xong lại nhấc rời khay nấu ra khỏi bếp…".

Với mỗi chỗ nghi ngờ, whisper riêng đoạn đó để tách các lần đọc:

```bash
py -3.12 tools/soat_lap.py "<voice gốc>" "$O/whisper.json" --chunks 22-29.5 31.5-36.8 --prompt "<như bước 1>"
```

Nếu kết quả còn mập mờ, chia nhỏ đoạn hơn, cắt ngay tại các khoảng lặng. Một chỗ có thể đọc tới 3 lần.

### Chọn mốc `--drop`

- **Giữ lần đọc trọn vẹn cuối cùng**, bỏ các lần trước.
- Đặt điểm đầu và điểm cuối của `--drop` **trong khoảng lặng** (dùng danh sách lặng ≥0.05s), cách chữ ít nhất ~0.05s. Mốc whisper của từ đầu tiên hay lệch, nên tin danh sách khoảng lặng hơn.
- Điểm cuối `--drop` nên rơi vào khoảng lặng ngay trước lần đọc giữ lại, để còn ~0.1–0.2s hơi thở trước câu.
- Câu cụt đứng riêng mà nghĩa không ăn với câu sau (ví dụ "Nồi lẩu điện" chen giữa "…chống bỏng" và "Vỏ nồi cách nhiệt") thì coi là đọc vấp và bỏ, nhưng **ghi vào báo cáo để Yan nghe lại**.

## Bước 3: Làm sạch voice

```bash
py -3.12 tools/clean_voice.py "<voice gốc>" "$O/whisper.json" "$O" --noise -48 \
  --drop 22.35-25.65 --drop 31.85-34.20 ...
```

- `--noise -48` cho voice thu điện thoại nhỏ (-35 sẽ cắt vào chữ). Voice to/thu mic tốt thì đo lại bằng `soat_lap.py` xem khoảng lặng có hợp lý không.
- Mặc định đã đúng chuẩn: tốc độ 1.07x giữ cao độ, nghỉ ngắn ~0.2s và hết câu ~0.3s (đo sau khi tăng tốc), -13 LUFS (tự đo lại sau bộ giới hạn đỉnh và bù gain), đỉnh ≤ -1 dBTP.
- Hook KOL nói trực tiếp: thêm `--prepend hook.MP4@a-b --prepend-json hook.json` (xem docstring của tool).

## Bước 4: Kiểm tra voice sạch

```bash
py -3.12 tools/transcribe.py "$O/voice_clean.wav" "$O/whisper_check.json" --prompt "<như bước 1>"
ffmpeg -nostdin -i "$O/voice_clean.wav" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
```

Kiểm tra:
- Đọc lại toàn bộ lời: liền mạch từ hook đến CTA, không còn câu lặp, không mất câu.
- Không còn từ nào kéo dài bất thường giữa câu.
- Độ lớn -13 ± 0.3 LUFS.

Sót chỗ nào thì thêm `--drop` và chạy lại bước 3.

## Bước 5: Xuất MP4

```bash
cd "$O"; D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 voice_clean.wav)
ffmpeg -nostdin -v error -y -f lavfi -i color=c=black:s=1080x1920:r=30 -i voice_clean.wav -t $D \
  -c:v libx264 -tune stillimage -pix_fmt yuv420p -c:a aac -b:a 320k -ar 48000 -movflags +faststart "<tên>_voice.mp4"
```

Dùng `-t $D`, không dùng `-shortest`: `-shortest` với nguồn lavfi làm dư ~2s hình đen ở cuối.

## Bước 6: Tạo phụ đề

### 6a. Viết `loi_voice.txt`

- Có kịch bản: chép lời kịch bản, bỏ câu voice không đọc, sửa theo đúng câu chữ voice thật nói.
- Không có kịch bản: lấy chữ từ `whisper_check.json` rồi **sửa tay lỗi whisper**. Đọc theo ngữ cảnh quảng cáo (cấu trúc sáng/trưa/tối, câu CTA quen thuộc) để đoán đúng chữ.

Whisper hay nghe sai (thêm vào đây khi gặp lỗi mới):

| Whisper nghe | Đúng |
|---|---|
| say, bê, doong | xay, Bear, gioăng |
| Điêu hời, mua co fanpage, giao hàng tặng nhà | Deal hời, mua qua fanpage, giao hàng tận nhà |
| em chút đơn, ắp chọn yêu đãi | em chốt đơn, áp trọn ưu đãi |
| đình cháo mềm như | ninh cháo mềm nhừ |
| mất hưởng | mất hứng |
| chờ đến / tới cả nhà (đoạn kể sáng–trưa–tối) | trưa đến / tối cả nhà |
| Nội dung tích, nồi linh/lưng nhiệt | Nồi dung tích, nồi lên nhiệt |
| nhóc khay, cánh nhiệt, có thể cầm | nhấc khay, cách nhiệt, có tay cầm |

Chữ nào không chắc thì vẫn chọn phương án hợp lý nhất, nhưng **liệt kê vào báo cáo** (thời điểm, mình ghi, whisper nghe) để Yan nghe lại.

### 6b. Ngắt dòng bằng dấu `|`

Chuẩn: **4–6 chữ/dòng**, ngắt theo cụm nghĩa. Dấu chấm/hỏi và chỗ voice ngừng hơi tự xuống dòng, dấu phẩy thì không.

- Đặt `|` giữa các cụm, mỗi cụm tối đa 6 chữ. Cụm >6 chữ công cụ sẽ tự chia đôi và hay cắt ngang từ ("ninh | cháo", "ưu | đãi").
- **Không cắt ngang từ ghép**: nấu nướng, nồi lẩu, quây quần, đều đặn, cách nhiệt, nhấc rời, màn hình, chốt đơn, ưu đãi, giao hàng, tận nhà…
- Tránh dòng 1–2 chữ lẻ (2–4 chữ/dòng Yan đã chê vụn), trừ khi đó là cả một câu ngắn.

Ví dụ:
```
Hội mê nấu nướng tại gia, | đừng mua nồi lẩu | chỉ chờ dịp đông người.
Anh chị nhấn ngay | vào góc phải màn hình | để em chốt đơn và áp trọn | ưu đãi cho mình nha.
```

### 6c. Xuất và soát

```bash
py -3.12 tools/make_srt.py "$O/loi_voice.txt" "$O/whisper_check.json" "$O/<tên>_sub.srt"
awk 'NR%4==2{split($1,a,/[:,]/);split($3,b,/[:,]/);d=(b[2]*60+b[3]+b[4]/1000)-(a[2]*60+a[3]+a[4]/1000)} NR%4==3{n=split($0,x," "); printf "%.2fs %d | %s\n", d, n, $0}' "$O/<tên>_sub.srt"
```

- Luôn dùng `whisper_check.json` (whisper trên chính voice sạch) cho mốc thời gian. Mốc này khớp với MP4 khi đặt voice ở giây 0.
- Tỉ lệ khớp nên ≥95%. Thấp hơn nghĩa là lời trong `loi_voice.txt` lệch nhiều so với voice.
- Soát từng dòng: không có dòng cắt ngang từ, dòng >6 chữ, hay dòng hiện <0.3s. Sửa `|` rồi chạy lại. Dòng ngắn do voice ngừng hơi thật thì chấp nhận.
- Dùng Edit/Write để sửa `loi_voice.txt`, không dùng `sed -i` (công cụ sẽ đòi đọc lại file trước khi ghi tiếp).

## Báo cáo cho Yan

Trả lời bằng tiếng Việt, xưng "mình", đi thẳng vào kết quả:
1. Đường dẫn file MP4 và SRT (link markdown), cách import vào CapCut.
2. Bảng trước/sau: thời lượng, LUFS, tốc độ, khoảng nghỉ.
3. Danh sách chỗ đã bỏ: thời điểm trên voice gốc + câu bị bỏ + lý do. **Chỗ nào mình đoán thì in đậm, nhờ Yan nghe lại.**
4. Bảng chữ không chắc trong sub (nếu có).
5. Nếu có sửa công cụ trong `tools/` thì nói rõ đã sửa gì, và hỏi Yan có muốn commit không.

## Khi Yan nhờ chỉnh sau khi nghe

- "Nghỉ gấp quá / dài quá" cho riêng video này: chạy lại bước 3 với `--keep-gap` (nghỉ ngắn) và `--keep-gap-long` (hết câu), giá trị tính trước khi tăng tốc. Sau đó **làm lại bước 4–6**, vì mốc thời gian đã đổi, sub cũ sẽ lệch.
- "Sub vụn / dài quá": sửa `|` trong `loi_voice.txt`, hoặc đổi `--max-words`. Chỉ cần chạy lại 6c.
- Muốn đổi thành chuẩn cho mọi video: sửa mặc định trong tool, cập nhật `rules/chung.md` và mục "Rút ra khi dựng" trong `CLAUDE.md`, rồi chạy lại không truyền tham số để xác nhận ra đúng file Yan đã duyệt.
