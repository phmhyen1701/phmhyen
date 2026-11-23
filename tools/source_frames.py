"""Bước 2 của lập chỉ mục: trích khung hình nhỏ từ mỗi file source rồi ghép thành tờ xem nhanh (contact sheet).

Cách dùng:
    python tools/source_frames.py 5H02D24 045KN 5H12V78 [--step 2]

- Đọc index/<mã>_files.csv (chạy tools/source_probe.py trước).
- Mỗi file lấy 1 khung mỗi --step giây (mặc định 2s), cao 320px, tự xoay đúng chiều.
- Khung lưu ở bộ nhớ đệm trên ổ máy (không ghi lên ổ mạng):
      %LOCALAPPDATA%\\sube_index\\frames\\<mã>\\<file>\\t000.0.jpg
- Tờ xem nhanh: %LOCALAPPDATA%\\sube_index\\sheets\\<mã>\\<số>.jpg, mỗi tờ tối đa 24 khung,
  có ghi tên file + giây ở từng khung. Danh sách tờ: sheets\\<mã>\\sheets.csv
- Chỉ đọc file source, không sửa gì. Chạy lại sẽ bỏ qua khung đã có.
"""
import argparse
import csv
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from ffbin import FFMPEG

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "Source quay gốc"
INDEX = REPO / "index"
CACHE = Path(os.environ.get("SUBE_INDEX_CACHE", Path(os.environ["LOCALAPPDATA"]) / "sube_index"))

THUMB_H = 320
COLS, ROWS = 8, 3          # 24 khung / tờ
CELL_W, CELL_H = 180, 320  # khung dọc 9:16
LABEL_H = 22


def timestamps(duration: float, step: float):
    if duration <= 0:
        return []
    ts, t = [], min(0.3, duration / 2)
    while t < duration - 0.2:
        ts.append(round(t, 1))
        t += step
    last = round(max(duration - 0.3, 0), 1)
    if not ts or last - ts[-1] > step / 2:
        ts.append(last)
    return ts


def frame_path(code, rel, t):
    return CACHE / "frames" / code / rel.replace("/", "__") / f"t{t:06.1f}.jpg"


def grab(job):
    src, out, t = job
    if out.exists() and out.stat().st_size > 0:
        return True
    out.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        [FFMPEG, "-v", "error", "-y", "-ss", str(t), "-i", str(src), "-frames:v", "1",
         "-vf", f"scale=-2:{THUMB_H}", "-q:v", "5", str(out)],
        capture_output=True,
    )
    return r.returncode == 0 and out.exists()


def font(size):
    for name in ("arialbd.ttf", "arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def build_sheets(code, items):
    """items: list of (rel, t, path). Một file không bị chia đôi giữa 2 tờ nếu vừa 1 tờ."""
    out_dir = CACHE / "sheets" / code
    out_dir.mkdir(parents=True, exist_ok=True)
    per = COLS * ROWS
    groups, cur = [], []
    by_file = {}
    for it in items:
        by_file.setdefault(it[0], []).append(it)
    for rel, frames in by_file.items():
        if cur and len(cur) + len(frames) > per and len(frames) <= per:
            groups.append(cur)
            cur = []
        for f in frames:
            cur.append(f)
            if len(cur) == per:
                groups.append(cur)
                cur = []
    if cur:
        groups.append(cur)

    f_small, rows_csv = font(14), []
    for gi, grp in enumerate(groups, 1):
        sheet = Image.new("RGB", (COLS * CELL_W, ROWS * (CELL_H + LABEL_H)), "white")
        d = ImageDraw.Draw(sheet)
        for i, (rel, t, p) in enumerate(grp):
            x, y = (i % COLS) * CELL_W, (i // COLS) * (CELL_H + LABEL_H)
            try:
                im = Image.open(p).convert("RGB")
                im.thumbnail((CELL_W, CELL_H))
                sheet.paste(im, (x + (CELL_W - im.width) // 2, y + LABEL_H))
            except OSError:
                pass
            name = Path(rel).stem
            d.rectangle([x, y, x + CELL_W - 1, y + LABEL_H - 1], fill="black")
            d.text((x + 4, y + 3), f"{name} {t:.1f}s", fill="yellow", font=f_small)
        path = out_dir / f"{gi:03d}.jpg"
        sheet.save(path, quality=80)
        files = sorted({r for r, _, _ in grp}, key=lambda r: [i for i, g in enumerate(grp) if g[0] == r][0])
        rows_csv.append({"sheet": path.name, "files": ";".join(files)})
    with (out_dir / "sheets.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["sheet", "files"])
        w.writeheader()
        w.writerows(rows_csv)
    return len(groups)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("codes", nargs="+")
    ap.add_argument("--step", type=float, default=2.0)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    for code in a.codes:
        rows = list(csv.DictReader((INDEX / f"{code}_files.csv").open(encoding="utf-8-sig")))
        jobs, items = [], []
        for r in rows:
            src = SOURCE / code / r["file"]
            for t in timestamps(float(r["duration"] or 0), a.step):
                p = frame_path(code, r["file"], t)
                jobs.append((src, p, t))
                items.append((r["file"], t, p))
        with ThreadPoolExecutor(max_workers=a.workers) as pool:
            ok = 0
            for i, res in enumerate(pool.map(grab, jobs), 1):
                ok += res
                if i % 200 == 0:
                    print(f"  {code}: {i}/{len(jobs)} khung", flush=True)
        n = build_sheets(code, items)
        print(f"{code}: {ok}/{len(jobs)} khung, {n} tờ xem nhanh", flush=True)


if __name__ == "__main__":
    main()
