# Hướng dẫn cài đặt trên Windows

> Mục tiêu: chạy Claude Code ngay trên máy của Yan, đọc trực tiếp kho source, xuất clip thẳng ra folder để kéo vào CapCut.
> Thời gian: khoảng **30–45 phút**. Phần lớn là chờ tải và cài.

---

## Bước 1. Tạo folder làm việc (~2 phút)

Tạo cấu trúc sau. Ổ đĩa nào cũng được, chọn ổ còn nhiều chỗ trống:

```
D:\Sube\
├── source\
│   ├── 5H02D24\
│   ├── 045KN\
│   └── 5H12V78\
├── input\
└── output\
```

- Chép (copy, **không cắt**) kho source của từng mã vào đúng folder mang tên mã đó.
- **Không** đặt folder ngay trong `C:\Users\<tên>\` hoặc trong thư mục ẩn.

---

## Bước 2. Cài Git (~5 phút)

Claude Code trên Windows cần Git để chạy.

1. Bấm phím **Windows**, gõ `PowerShell`, chọn **Windows PowerShell**.
2. Dán lệnh sau rồi Enter:
   ```powershell
   winget install --id Git.Git -e
   ```
3. Nếu máy hỏi quyền (UAC) thì bấm **Yes**.
4. **Đóng PowerShell, mở lại**, rồi kiểm tra:
   ```powershell
   git --version
   ```
   Hiện ra dòng `git version 2.x.x` là được.

> Nếu báo lỗi không có `winget`, tải Git tại https://git-scm.com/download/win, bấm Next liên tục đến hết để cài.

---

## Bước 3. Cài app Claude Desktop (~5 phút)

1. Tải tại **https://claude.ai/download**, chọn bản **Windows**.
2. Cài đặt, rồi đăng nhập bằng tài khoản Claude Yan đang dùng.
3. Trong app, mở tab **Code** (Claude Code).
4. Khi được hỏi chọn folder làm việc, chọn **`D:\Sube`**.

---

## Bước 4. Để Claude tự cài phần còn lại (~15–20 phút)

Trong phiên Claude Code vừa mở ở `D:\Sube`, **dán nguyên đoạn này** rồi gửi:

```
Cài đặt môi trường cho dự án dựng video Sube trên máy này:
1. Clone repo github.com/phmhyen1701/phmhyen vào D:\Sube\phmhyen, nhánh claude/nifty-faraday-bbnx5u
2. Tạo file D:\Sube\CLAUDE.md chỉ có 1 dòng: @phmhyen/CLAUDE.md
3. Cài Python 3.12 và ffmpeg bằng winget (Python.Python.3.12, Gyan.FFmpeg) nếu máy chưa có
4. Cài faster-whisper bằng pip
5. Kiểm tra lại: git, python, ffmpeg, faster-whisper đều chạy được. Báo mình kết quả từng mục
Báo thời gian ước tính trước khi làm.
```

Trong lúc chạy:
- Claude sẽ **xin phép trước mỗi lệnh**. Đọc qua rồi bấm cho phép.
- Khi clone repo, có thể bật trình duyệt để **đăng nhập GitHub**. Đăng nhập bằng tài khoản `phmhyen1701`.
- Nếu máy hỏi quyền (UAC) khi cài Python/ffmpeg thì bấm **Yes**.

---

## Bước 5. Chỉnh máy để chạy lâu không bị ngắt (~2 phút)

Lập chỉ mục 1000+ clip mất **1–3 tiếng**, máy không được ngủ giữa chừng.

1. **Settings → System → Power & battery → Screen and sleep**
2. Mục *When plugged in, put my device to sleep after* → chọn **Never**
3. Laptop thì **cắm sạc** trong lúc chạy.

Xong việc thì có thể đặt lại như cũ.

---

## Bước 6. Kiểm tra lần cuối

Đóng app Claude, mở lại phiên Code ở `D:\Sube`, rồi gửi:

```
Tóm tắt dự án này và các việc đang chờ.
```

Nếu Claude trả lời đúng (nhắc đến 3 mã 5H02D24, 045KN, 5H12V78 và việc đang chờ thông tin brand) là đã nhận đủ bối cảnh. **Cài đặt hoàn tất.**

---

## Cách dùng hằng ngày

| Việc | Làm gì |
|---|---|
| Có source mới cho một mã | Chép vào `D:\Sube\source\<mã>\`, rồi nhắn Claude: *"Cập nhật chỉ mục source mã <mã>"* |
| Dựng video mới | Tạo `D:\Sube\input\<tên video>\`, bỏ voice thô + kịch bản vào, nhắn: *"Dựng video <tên video>, mã <mã>, nhãn Bear/Bear mẹ bé"* |
| Lấy kết quả | Mở `D:\Sube\output\<tên video>\`, chọn hết các clip trong `clips\`, kéo vào CapCut |

---

## Gặp lỗi thì sao?

| Lỗi | Cách xử lý |
|---|---|
| `git` / `python` / `ffmpeg` *is not recognized* | Đóng hết cửa sổ PowerShell và app Claude rồi mở lại (máy cần nạp lại PATH). Vẫn lỗi thì khởi động lại máy |
| Clone repo báo *Repository not found* | Chưa đăng nhập đúng tài khoản GitHub `phmhyen1701`. Nhắn Claude: *"đăng nhập lại GitHub"* |
| Cài faster-whisper báo lỗi | Gửi nguyên nội dung lỗi cho Claude |
| Claude không nhắc gì đến dự án ở Bước 6 | Kiểm tra file `D:\Sube\CLAUDE.md` có đúng dòng `@phmhyen/CLAUDE.md` không |

---

## Cách khác: Remote Control (không bắt buộc)

Nếu muốn tiếp tục từ phiên Claude trên web/điện thoại mà vẫn dùng file trên máy:
- Trong app Claude Desktop vào **Settings → Claude Code → Remote Control** và thêm folder `D:\Sube`.
- Tính năng này **chưa mở cho mọi tài khoản**. Không thấy mục này thì cứ dùng cách ở trên, kết quả như nhau.
