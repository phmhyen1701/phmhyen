"""Bước 1 của lập chỉ mục: đọc thông tin kỹ thuật từng file trong kho source.

Cách dùng:
    python tools/source_probe.py 5H02D24 045KN 5H12V78

Ghi ra index/<mã>_files.csv: file, duration, width, height, fps, rotation, size_mb, created.
Chỉ đọc file source, không sửa gì.
"""
import csv
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from ffbin import FFPROBE

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "Source quay gốc"
INDEX = REPO / "index"
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mts", ".avi", ".mkv"}
FIELDS = ["file", "duration", "width", "height", "fps", "rotation", "size_mb", "created"]


def probe(path: Path) -> dict:
    out = subprocess.run(
        [FFPROBE, "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    row = {"file": "", "duration": "", "width": "", "height": "", "fps": "",
           "rotation": "", "size_mb": round(path.stat().st_size / 1e6, 1), "created": ""}
    try:
        info = json.loads(out.stdout or "{}")
    except json.JSONDecodeError:
        return row
    fmt = info.get("format", {})
    row["duration"] = round(float(fmt.get("duration", 0) or 0), 2)
    row["created"] = fmt.get("tags", {}).get("creation_time", "")
    for st in info.get("streams", []):
        if st.get("codec_type") != "video":
            continue
        row["width"], row["height"] = st.get("width", ""), st.get("height", "")
        num, _, den = (st.get("avg_frame_rate") or "0/1").partition("/")
        row["fps"] = round(float(num) / float(den or 1), 2) if float(den or 1) else ""
        rot = st.get("tags", {}).get("rotate", "")
        for sd in st.get("side_data_list", []) or []:
            if "rotation" in sd:
                rot = sd["rotation"]
        row["rotation"] = rot
        break
    return row


def main(codes):
    INDEX.mkdir(exist_ok=True)
    for code in codes:
        folder = SOURCE / code
        files = sorted(p for p in folder.rglob("*") if p.suffix.lower() in VIDEO_EXT)
        with ThreadPoolExecutor(max_workers=8) as pool:
            rows = list(pool.map(probe, files))
        for p, r in zip(files, rows):
            r["file"] = p.relative_to(folder).as_posix()
        out = INDEX / f"{code}_files.csv"
        with out.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            w.writerows(rows)
        total = sum(float(r["duration"] or 0) for r in rows)
        bad = sum(1 for r in rows if not r["duration"])
        print(f"{code}: {len(rows)} file, tổng {total/60:.1f} phút, lỗi đọc {bad} -> {out.name}")


if __name__ == "__main__":
    main(sys.argv[1:] or [p.name for p in SOURCE.iterdir() if p.is_dir()])
