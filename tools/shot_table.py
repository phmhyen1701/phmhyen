"""Tạo bảng phân cảnh nháp cho video mẫu: mốc cắt cảnh (ffmpeg) + lời voice (whisper).

Cách dùng:
    python tools/shot_table.py video.mp4 whisper.json out.csv [--thresh 0.12] [--min-gap 0.4]
Cột nhom_source / canh_source / overlay để trống cho người hoặc Claude điền sau khi xem khung hình.
"""
import argparse
import csv
import json
import re
import subprocess


def scene_cuts(video, thresh):
    p = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", video, "-vf",
         f"scale=270:-1,select='gt(scene,{thresh})',showinfo", "-an", "-f", "null", "-"],
        capture_output=True, text=True)
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", p.stderr)]


def duration(video):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", video], capture_output=True, text=True).stdout
    return float(out.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("whisper_json")
    ap.add_argument("out_csv")
    ap.add_argument("--thresh", type=float, default=0.12)
    ap.add_argument("--min-gap", type=float, default=0.4)
    a = ap.parse_args()

    cuts = []
    for t in scene_cuts(a.video, a.thresh):
        if not cuts or t - cuts[-1] >= a.min_gap:
            cuts.append(t)
    end = duration(a.video)
    bounds = [0.0] + [c for c in cuts if c > a.min_gap] + [end]

    words = [w for s in json.load(open(a.whisper_json, encoding="utf-8")) for w in s["words"]]
    rows = []
    for i in range(len(bounds) - 1):
        s, e = bounds[i], bounds[i + 1]
        # gán từ vào cảnh theo điểm giữa của từ
        txt = "".join(w[2] for w in words if s <= (w[0] + w[1]) / 2 < e).strip()
        rows.append({"stt": i + 1, "bat_dau": round(s, 1), "ket_thuc": round(e, 1),
                     "do_dai": round(e - s, 1), "phan": "", "cau_voice": txt,
                     "canh_source": "", "nhom_source": "", "overlay_tinh_nang": ""})
    with open(a.out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} cảnh -> {a.out_csv}")


if __name__ == "__main__":
    main()
