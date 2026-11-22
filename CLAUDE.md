# Dự án: Tự động hoá dựng video ads Sube → CapCut

> Đọc toàn bộ file này trước khi làm. Cập nhật lần cuối: 22/11/2026.

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
```
D:\Sube\                      ← mở Claude ở đây
├── CLAUDE.md                 ← chỉ chứa dòng @phmhyen/CLAUDE.md
├── phmhyen\                  ← repo này
├── source\<mã SP>\           ← kho source gốc, KHÔNG sửa/xoá
├── input\<tên video>\        ← voice thô + kịch bản của video cần dựng
└── output\<tên video>\       ← đầu ra
```

## Trong repo này
| Đường dẫn | Nội dung |
|---|---|
| `rules/chung.md` | Quy tắc chung mọi mã: khung video, kiểu hook, dạng thân, cắt cảnh, ưu tiên chọn source, CTA, phụ đề, overlay |
| `rules/sp/<mã>.md` | Quy tắc riêng từng mã: từ khoá voice → nhóm source, nhãn overlay. Đã có: `5H02D24`, `045KN`, `5H12V78` |
| `rules/brand/` | *(chưa có)* Quy tắc text theo 2 nhãn **Bear** và **Bear mẹ bé**. Chờ Yan gửi guideline, font, màu, template |
| `analysis/<mã>/` | Bảng phân cảnh video mẫu (`shots_video*.csv`), kết quả whisper, kịch bản đối chiếu |
| `tools/make_srt.py` | Tạo .srt: chữ lấy từ kịch bản, thời gian lấy từ whisper (so khớp mềm) |
| `tools/shot_table.py` | Tạo bảng phân cảnh nháp cho video mẫu (mốc cắt cảnh + lời voice) |
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
| Nhạc + SFX | Dùng thư viện CapCut. Mình xuất danh sách mốc SFX |

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

## Việc đang chờ
1. Yan gửi thông tin brand (guideline, mã màu, font, ảnh cài đặt template CapCut, quy ước tên preset) → viết `rules/brand/bear.md`, `rules/brand/bear-me-be.md`.
2. Lập chỉ mục kho source cho mã làm thử đầu tiên (Yan chọn mã).
3. Dựng thử 1 video hoàn chỉnh: voice thô + kịch bản → đầu ra như trên.

## Nguyên tắc khi làm
- **Không sửa/xoá file gốc** trong `source\` hay voice. Mọi đầu ra ghi vào `output\`.
- Viết script tái sử dụng được (Python + ffmpeg), lưu trong `tools/`.
- Báo thời gian ước tính trước mỗi bước lớn; hỏi lại khi quy tắc chưa rõ.
- Lập chỉ mục chạy lâu: nhắc Yan cắm sạc, tắt chế độ ngủ.
