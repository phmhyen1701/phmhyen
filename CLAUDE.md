# Dự án: Tự động hoá dựng video ads Sube → CapCut

> Đọc toàn bộ file này trước khi làm. Cập nhật lần cuối: 23/11/2026.

## Người dùng
- Tên gọi: **Yan** (Hải Yến). Xưng **"mình"**, trả lời **tiếng Việt**.
- Video Editor tại Sube Việt Nam (bán hàng qua TikTok Shop / Shopee), team Media.
- Phong cách làm việc:
  - đi thẳng vào việc, không chào hỏi rườm rà
  - dùng gạch đầu dòng/bảng khi phân tích
  - **luôn báo thời gian ước tính trước khi làm một tác vụ**
  - **hỏi lại nếu yêu cầu chưa rõ**

## Bài toán
Video ads Sube có cấu trúc lặp lại, chủ yếu khác nhau ở phần hook. Mục tiêu: từ voice thô + kịch bản + kho source, tự động xuất ra bộ clip đã cắt đúng độ dài, đánh số thứ tự, cùng file phụ đề và bảng mốc text/SFX. Yan kéo vào CapCut rồi chỉnh tiếp.

## Cấu trúc folder trên máy Yan (Windows)
Repo nằm thẳng trong folder làm việc trên ổ mạng phòng Media (`Y:` = `\\192.168.70.10\Phòng Media`):
```
Y:\0. TÀI NGUYÊN MEDIA\Source Yến\Ads x Claude\   ← repo này, mở Claude ở đây
├── CLAUDE.md, rules\, tools\, docs\, analysis\
├── Source quay gốc\<mã SP>\  ← kho source gốc, KHÔNG sửa/xoá. Git bỏ qua (.git/info/exclude)
├── input\<tên video>\        ← voice thô + kịch bản của video cần dựng
└── output\<tên video>\       ← đầu ra
```
- Ổ mạng: git cần `safe.directory` cho folder này (đã thêm trên máy Yan). Đọc/ghi chậm hơn ổ trong máy, lập chỉ mục source sẽ lâu hơn.
- `Source quay gốc\` và file voice/video trong `input\`, `output\` là dữ liệu nặng, **không commit** lên GitHub.

## Trong repo này
| Đường dẫn | Nội dung |
|---|---|
| `rules/chung.md` | Quy tắc chung mọi mã: khung video, kiểu hook, dạng thân, cắt cảnh, ưu tiên chọn source, CTA, phụ đề, overlay |
| `rules/sp/<mã>.md` | Quy tắc riêng từng mã: từ khoá voice → nhóm source, nhãn overlay. Đã có: `5H02D24`, `045KN`, `5H12V78` |
| `rules/brand/` | Quy tắc text theo 2 nhãn: `chung.md` (font chung, so sánh, chọn nhãn theo mã), `bear.md` (Bear Official), `bear-me-be.md` (Bear mẹ bé). Nguồn ảnh/font gốc ở `Brand guildeline/` |
| `analysis/<mã>/` | Bảng phân cảnh video mẫu (`shots_video*.csv`), kết quả whisper, kịch bản đối chiếu |
| `tools/transcribe.py` | faster-whisper → JSON mốc từng từ. Giải mã bằng ffmpeg (thư viện `av` trên máy Yan lệch phiên bản, gọi thẳng file sẽ lỗi `metadata_errors`) |
| `tools/clean_voice.py` | Làm sạch voice: `--drop` bỏ lần đọc hỏng, rút khoảng lặng, -13 LUFS, `--prepend` ghép tiếng hook KOL lên đầu |
| `tools/retime.py` | Quy đổi mốc `edit_map`/overlay/SFX khi làm sạch lại voice (bỏ thêm câu, đổi tốc độ) |
| `tools/build_clips.py` | Đọc `edit_map.csv` → cắt `clips/NN_nhom.mp4` (1080x1920, 30fps, tắt tiếng) + `preview.mp4` có phụ đề |
| `tools/make_srt.py` | Tạo .srt: chữ lấy từ kịch bản, thời gian lấy từ whisper (so khớp mềm) |
| `tools/shot_table.py` | Tạo bảng phân cảnh nháp cho video mẫu (mốc cắt cảnh + lời voice) |
| `tools/sfx_classify.py` | Nhận diện SFX + kiểu nhạc trong video mẫu (cần tách voice bằng demucs trước) |
| `docs/huong-dan-cai-dat-windows.md` | Hướng dẫn cài đặt trên máy Yan |

## Các quyết định đã chốt
| Hạng mục | Cách làm |
|---|---|
| Audio | faster-whisper (tiếng Việt, model `medium`) → so khớp mềm với kịch bản → cắt đoạn thừa bằng ffmpeg. Whisper hay nhận sai: "xay"→"say", "Bear"→"bê", "gioăng"→"doong"; đoạn nhạc lớn có thể mất chữ |
| Kho source | File quay **dài**, phải cắt lấy đoạn. Lập chỉ mục **một lần** cho mỗi mã, theo **đoạn hành động**: `file, in, out, nhóm, mô tả`. Lưu ở `index/<mã>.csv` |
| Hook | Hook KOL/vlog/inbox **quay riêng từng video**, Yan đưa file. Hook B-roll/UGC lấy từ kho |
| Kịch bản | 3 cột: Phần, Mô tả cảnh, Voice. "Trám" = cảnh chèn (B-roll), "VJ" = người dẫn trong khung hình. Cột mô tả cảnh là khung chính, từ khoá voice cụ thể thắng mô tả chung. Voice thu thật có thể lược bớt so với kịch bản |
| Đưa vào CapCut | Xuất clip **đã cắt đúng độ dài, đánh số** (`01_...mp4`...) + voice sạch. Yan chọn tất cả, kéo vào timeline |
| Phụ đề | Tuỳ video: nhiều text overlay thì không có phụ đề, storytelling thì có. Luôn xuất `.srt`, Yan quyết định. Còn chờ Yan thử xem highlight theo từng từ có chạy với .srt import không |
| Text overlay | Mỗi mã SP chọn nhãn **Bear** hoặc **Bear mẹ bé** lúc dựng. Đề xuất: Yan lưu preset CapCut cho từng loại text, mình xuất `overlay_cues.csv` (thời điểm, preset, nội dung). Một nhãn đã có template CapCut |
| CTA | Chọn lại source mỗi video, sticker bám theo từng ý khuyến mãi trong voice |
| Nhạc + SFX | Dùng thư viện CapCut. Mình xuất danh sách mốc SFX theo `rules/chung.md` mục 7: ding khi nhãn bật lên, chuông/tiền khi có sticker deal, không whoosh, tắt âm gốc source, nhạc thấp hơn voice ~18–20 dB, voice -13 LUFS. Chờ Yan cho tên SFX hay dùng trong CapCut |

## Đầu ra mỗi video
```
output\<tên video>\
├── voice_clean.wav
├── clips\01_xxx.mp4, 02_xxx.mp4, ...
├── overlay.srt
├── overlay_cues.csv
├── sfx_cues.csv
├── edit_map.csv          # câu voice → source nào, từ giây nào đến giây nào, cột can_xem
└── preview.mp4
```

## Việc đang chờ (theo thứ tự)
1. ~~Yan cài đặt theo `docs/huong-dan-cai-dat-windows.md`~~ Đã cài xong 23/11/2026 (git, Python 3.12, ffmpeg 9.1, faster-whisper 1.2.1), repo chuyển sang folder Y: ở trên. Còn: kiểm tra Claude đọc được bối cảnh khi mở phiên mới.
2. ~~Yan gửi thông tin brand~~ Đã viết `rules/brand/` 23/11/2026. Còn thiếu: nhãn của 045KN và 5H12V78, quy ước tên preset.
3. Thử **tạo draft CapCut mới** bằng thư viện cộng đồng (VectCutAPI/CapCutAPI có kèm MCP server, hoặc pyCapCut / pyJianYingDraft): tạo draft nhỏ gồm 3 clip + voice + 1 text → chép vào thư mục draft của CapCut → mở bằng bản CapCut của Yan xem có chạy không. Lưu ý:
   - Đây là công cụ không chính thức, CapCut cập nhật có thể làm hỏng. Đọc code trước khi cài.
   - Bản mới mã hoá `draft_content.json`, nên **đọc/sửa project cũ** khó; **tạo draft mới** có thể vẫn được, cần thử.
   - Không dùng dịch vụ giải mã bên ngoài (phải tải project lên server lạ).
   - Không bao giờ ghi vào project gốc của Yan.
4. Kiểm tra computer use trong app Claude Desktop (Settings → System/Capabilities → Computer use). Thử đặt 3–5 nhãn text + 2–3 SFX trên project mẫu, đo tốc độ và độ chính xác.
5. Lập chỉ mục kho source cho mã làm thử đầu tiên (Yan chọn mã).
6. Dựng thử 1 video hoàn chỉnh: voice thô + kịch bản → đầu ra như trên. **23/11/2026: đã dựng `output\D24 Thí nghiệm 8 giây\`** (đầu vào ở `Source từng video\<tên video>\`), chờ Yan duyệt preview + kéo vào CapCut.
   Rút ra khi dựng:
   - Voice thô rất nhỏ (khoảng -41 LUFS): dùng ngưỡng lặng `--noise -48`, ngưỡng -35 cắt vào chữ.
   - Whisper hay **gộp 2 lần đọc lặp thành 1** (dấu hiệu: một chữ kéo dài >1s). Soát: chạy whisper lại trên `voice_clean.wav`, và whisper riêng từng đoạn nghi ngờ trên voice gốc. D24 có 4 chỗ lặp, lần đầu mình chỉ bắt được 1.
   - Voice **mặc định tăng tốc 1.07x cho mọi video** (Yan chốt 23/11/2026; `clean_voice.py` đã để mặc định, clip hook KOL ghi cột `toc_do` = 1.07).
   - Hook KOL nói trực tiếp: cắt tiếng từ clip, ghép vào đầu voice (`--prepend`). Mọi clip đều tắt tiếng, chỉ còn một track voice.
   - Cảnh bấm giờ: đọc đồng hồ trên khung hình, chọn điểm vào sao cho đồng hồ chạm 8s đúng lúc voice nói "8 giây".

## Cách đưa vào CapCut (thứ tự ưu tiên)
1. Ghi thẳng draft CapCut, nếu bước 3 cho thấy file không mã hoá.
2. Kết hợp: Yan kéo clip/voice/.srt (~1 phút) → Claude dùng computer use đặt text preset + SFX từ thư viện CapCut → Yan chỉnh tinh.
3. Yan tự làm hết theo `overlay_cues.csv`, `sfx_cues.csv`.
- Sửa một cảnh: Claude xuất lại đúng file, giữ số thứ tự. Yan dùng Replace (Thay thế) trong CapCut.

## Nguyên tắc khi làm
- **Không sửa/xoá file gốc** trong `Source quay gốc\` hay voice. Mọi đầu ra ghi vào `output\`.
- Viết script tái sử dụng được (Python + ffmpeg), lưu trong `tools/`.
- Báo thời gian ước tính trước mỗi bước lớn; hỏi lại khi quy tắc chưa rõ.
- Lập chỉ mục chạy lâu: nhắc Yan cắm sạc, tắt chế độ ngủ.
