"""Cắt clip đánh số theo edit_map.csv và ghép preview.mp4.

Cách dùng:
    py -3.12 tools/build_clips.py <mã SP> <output\\tên video> [--preview] [--only 3,7] [--workers 2]

edit_map.csv (trong folder output) cần các cột:
    stt, phan, voice, start, end, src, nhom, overlay, can_xem, ghi_chu  [, toc_do]
- toc_do (tuỳ chọn, mặc định 1): tốc độ phát source, dùng cho hook KOL khi voice đã tăng tốc.
- start/end: giây trên voice_clean.wav (cảnh sau bắt đầu đúng ở end của cảnh trước).
- src: một hoặc nhiều đoạn source, cách nhau bằng ";", dạng  C6236.MP4@2.0-14.5
  Lấy lần lượt từng đoạn cho tới khi đủ độ dài cảnh (đoạn thiếu thì ghép đoạn kế, không slow-mo).
Đầu ra:
    clips/NN_<nhom>.mp4   1080x1920, 30 fps, H.264, không tiếng (rules: tắt âm gốc source)
    preview.mp4           clip nối nhau + voice_clean.wav (+ phụ đề overlay.srt nếu có), để duyệt nhanh
Số khung hình mỗi clip tính từ mốc tuyệt đối (round(t*30)) nên ghép lại không bị lệch tiếng.
Chỉ đọc source gốc, không sửa.
"""
import argparse
import csv
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ffbin import FFMPEG  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
FPS = 30
VF = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30"


def pick_encoder():
    test = subprocess.run(
        [FFMPEG, "-v", "error", "-f", "lavfi", "-i", "testsrc=size=1280x720:rate=30", "-t", "0.5",
         "-c:v", "h264_nvenc", "-f", "null", "-"], capture_output=True)
    if test.returncode == 0:
        return ["-c:v", "h264_nvenc", "-preset", "p5", "-cq", "19", "-b:v", "0"]
    return ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18"]


def parse_src(s):
    out = []
    for part in s.split(";"):
        part = part.strip()
        if not part:
            continue
        f, rng = part.rsplit("@", 1)
        a, b = rng.split("-")
        out.append((f.strip(), float(a), float(b)))
    return out


def clip_path(out_dir, r):
    return out_dir / "clips" / f"{int(r['stt']):02d}_{r['nhom'].split('|')[0]}.mp4"


def frames(r):
    return round(float(r["end"]) * FPS) - round(float(r["start"]) * FPS)


def build_one(r, src_dir, out_dir, enc):
    n = frames(r)
    spd = float(r.get("toc_do") or 1)  # hook KOL nói trực tiếp: chạy cùng tốc độ với voice
    need = n / FPS * spd
    pieces, got = [], 0.0
    for f, a, b in parse_src(r["src"]):
        take = min(b - a, need - got)
        pieces.append((src_dir / f, a, take))
        got += take
        if got >= need - 1e-3:
            break
    if got < need - 1e-3:
        # thiếu source: kéo dài khung cuối (Yan sẽ thấy can_xem)
        print(f"  ! cảnh {r['stt']}: source chỉ đủ {got:.2f}s / {need:.2f}s, giữ khung cuối")
    args = [FFMPEG, "-nostdin", "-v", "error", "-y"]
    for p, a, t in pieces:
        args += ["-ss", f"{a:.3f}", "-t", f"{t + 0.2:.3f}", "-i", str(p)]
    chains = [f"[{i}:v]trim=duration={t:.3f},setpts=(PTS-STARTPTS)/{spd},{VF}[v{i}]"
              for i, (_, _, t) in enumerate(pieces)]
    cat = "".join(f"[v{i}]" for i in range(len(pieces)))
    fc = ";".join(chains) + f";{cat}concat=n={len(pieces)}:v=1:a=0,tpad=stop_mode=clone:stop=-1[out]"
    dst = clip_path(out_dir, r)
    args += ["-filter_complex", fc, "-map", "[out]", "-frames:v", str(n), "-an", *enc,
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst)]
    subprocess.run(args, check=True)
    return dst


def preview(rows, out_dir, enc):
    work = out_dir / "work"
    work.mkdir(exist_ok=True)
    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{clip_path(out_dir, r).as_posix()}'\n" for r in rows), encoding="utf-8")
    vf = []
    srt = out_dir / "overlay.srt"
    if srt.exists():
        shutil.copy(srt, work / "sub.srt")
        vf = ["-vf", "subtitles=sub.srt:force_style='FontName=Arial,FontSize=13,Outline=2,MarginV=70'"]
    subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "concat.txt",
                    "-i", str(out_dir / "voice_clean.wav"), *vf, "-map", "0:v", "-map", "1:a",
                    *enc, "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    str(out_dir / "preview.mp4")], check=True, cwd=work)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ma")
    ap.add_argument("out_dir")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()

    out_dir = Path(a.out_dir).resolve()
    src_dir = REPO / "Source quay gốc" / a.ma
    rows = list(csv.DictReader(open(out_dir / "edit_map.csv", encoding="utf-8-sig")))
    (out_dir / "clips").mkdir(exist_ok=True)
    only = {int(x) for x in a.only.split(",") if x}
    todo = [r for r in rows if not only or int(r["stt"]) in only]
    if only:  # sửa một cảnh: xoá đúng clip cũ cùng số để không trùng tên
        for r in todo:
            for old in (out_dir / "clips").glob(f"{int(r['stt']):02d}_*.mp4"):
                old.unlink()
    enc = pick_encoder()
    with ThreadPoolExecutor(a.workers) as ex:
        for dst in ex.map(lambda r: build_one(r, src_dir, out_dir, enc), todo):
            print("  ->", dst.name, flush=True)
    if a.preview:
        preview(rows, out_dir, enc)
        print("  -> preview.mp4")


if __name__ == "__main__":
    main()
