"""Cắt mỗi đoạn trong index/<mã>.csv thành 1 file video riêng, xếp vào folder theo nhóm chính.

Cách dùng:
    python tools/index_cut.py 5H02D24 [--limit 3] [--workers 2] [--skip KHAC]

Đầu ra (cạnh "Source quay gốc"):
    Source đã cắt/<mã>/<NHÓM CHÍNH>/<tên file gốc>_<in>-<out>.mp4
    Source đã cắt/<mã>/danh_sach.csv   (clip -> file gốc, in, out, nhóm, mô tả...)

- Giữ nguyên độ phân giải và fps gốc, tự xoay đúng chiều, H.264 + AAC (mở thẳng trong CapCut).
- Cắt chính xác theo giây (mã hoá lại), không chép thêm vào nhóm phụ.
- Chỉ đọc file gốc, không sửa gì. Chạy lại sẽ bỏ qua clip đã có.
"""
import argparse
import csv
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from ffbin import FFMPEG

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "Source quay gốc"
OUT_ROOT = REPO / "Source đã cắt"
INDEX = REPO / "index"


def pick_encoder():
    test = subprocess.run(
        [FFMPEG, "-v", "error", "-f", "lavfi", "-i", "testsrc=size=1280x720:rate=30", "-t", "0.5",
         "-c:v", "h264_nvenc", "-f", "null", "-"], capture_output=True)
    if test.returncode == 0:
        return ["-c:v", "h264_nvenc", "-preset", "p5", "-cq", "19", "-b:v", "0"]
    return ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18"]


def clip_name(r):
    return f"{Path(r['file']).stem}_{float(r['in']):.1f}-{float(r['out']):.1f}.mp4"


def cut(job):
    src, dst, a, b, enc = job
    if dst.exists() and dst.stat().st_size > 0:
        return dst, "có sẵn"
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_suffix(".part.mp4")
    cmd = [FFMPEG, "-v", "error", "-y", "-ss", f"{a:.2f}", "-i", str(src), "-t", f"{b - a:.2f}",
           "-map", "0:v:0", "-map", "0:a:0?", *enc, "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(tmp)]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        tmp.unlink(missing_ok=True)
        return dst, "LỖI " + r.stderr.strip()[-300:]
    tmp.replace(dst)
    return dst, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("code")
    ap.add_argument("--limit", type=int, default=0, help="chỉ cắt N đoạn đầu (để thử)")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--skip", default="TRUNG", help="nhóm bỏ qua, cách nhau bằng dấu phẩy")
    a = ap.parse_args()

    skip = {s.strip() for s in a.skip.split(",") if s.strip()}
    rows = [r for r in csv.DictReader((INDEX / f"{a.code}.csv").open(encoding="utf-8-sig"))
            if r["nhom"].split("|")[0] not in skip]
    if a.limit:
        rows = rows[: a.limit]
    enc = pick_encoder()
    print("Bộ mã hoá:", enc[1], flush=True)

    out_dir = OUT_ROOT / a.code
    jobs, listing = [], []
    for r in rows:
        group = r["nhom"].split("|")[0]
        dst = out_dir / group / clip_name(r)
        jobs.append((SOURCE / a.code / r["file"], dst, float(r["in"]), float(r["out"]), enc))
        listing.append({"clip": f"{group}/{dst.name}", **r})

    done = errors = 0
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        for i, (dst, status) in enumerate(pool.map(cut, jobs), 1):
            done += status in ("ok", "có sẵn")
            if status.startswith("LỖI"):
                errors += 1
                print(f"  {dst.name}: {status}", flush=True)
            if i % 10 == 0 or i == len(jobs):
                print(f"  {i}/{len(jobs)} clip", flush=True)

    out_dir.mkdir(parents=True, exist_ok=True)
    fields = ["clip", "file", "in", "out", "dur", "nhom", "mo_ta", "goc_may", "mon", "chat_luong"]
    with (out_dir / "danh_sach.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(listing)
    print(f"{a.code}: {done}/{len(jobs)} clip xong, {errors} lỗi -> {out_dir}", flush=True)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
