"""Làm sạch voice thô: bỏ đoạn đọc lại, rút khoảng lặng, chuẩn hoá -13 LUFS.

Cách dùng:
    py -3.12 tools/clean_voice.py voice.m4a whisper.json out_dir [--drop 12.3-18.9 --drop ...]
        [--keep-gap 0.12] [--min-gap 0.25] [--noise -35] [--lufs -13] [--speed 1.07 (mặc định)]
        [--prepend hook.MP4@a-b --prepend-json hook.json]
    Voice thô Sube thường rất nhỏ (~-41 LUFS): dùng --noise -48, ngưỡng -35 cắt vào chữ.

- --drop: các khoảng (giây, theo voice gốc) cần bỏ, ví dụ lần đọc hỏng trước lần đọc trọn vẹn cuối.
- Khoảng lặng (ffmpeg silencedetect) dài hơn --min-gap được rút về --keep-gap (theo rules/chung.md mục 2).
- Nối các đoạn bằng crossfade 8ms để không bị tiếng tách.
Đầu ra trong out_dir:
    voice_clean.wav       48 kHz mono, -13 LUFS, đỉnh <= -1 dBTP
    whisper_clean.json    mốc từng từ đã quy đổi sang thời gian của voice_clean
    voice_map.json        bảng quy đổi [gốc_bắt_đầu, gốc_kết_thúc, mới_bắt_đầu]
Chỉ đọc file voice gốc, không sửa.
"""
import argparse
import json
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ffbin import FFMPEG  # noqa: E402

SR = 48000


def decode(path):
    raw = subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def silences(path, noise, min_d):
    err = subprocess.run([FFMPEG, "-nostdin", "-i", path, "-af",
                          f"silencedetect=noise={noise}dB:d={min_d}", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="ignore").stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(starts, ends))


def subtract(spans, cuts):
    """spans - cuts (đều là list [a, b])."""
    out = []
    for a, b in spans:
        cur = [(a, b)]
        for c, d in cuts:
            nxt = []
            for x, y in cur:
                if d <= x or c >= y:
                    nxt.append((x, y))
                    continue
                if c > x:
                    nxt.append((x, c))
                if d < y:
                    nxt.append((d, y))
            cur = nxt
        out += cur
    return [s for s in out if s[1] - s[0] > 0.01]


def loudness(x):
    p = subprocess.run([FFMPEG, "-nostdin", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                        "-af", "ebur128=peak=true", "-f", "null", "-"],
                       input=x.tobytes(), capture_output=True)
    err = p.stderr.decode("utf-8", "ignore")
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", err)[-1])
    return i


def remap(t, vmap):
    for a, b, n in vmap:
        if t < a:
            return n  # rơi vào đoạn đã bỏ: dồn về đầu đoạn giữ tiếp theo
        if t <= b:
            return n + (t - a)
    a, b, n = vmap[-1]
    return n + (b - a)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("whisper_json")
    ap.add_argument("out_dir")
    ap.add_argument("--drop", action="append", default=[])
    ap.add_argument("--keep-gap", type=float, default=0.12)
    ap.add_argument("--min-gap", type=float, default=0.25)
    ap.add_argument("--noise", type=float, default=-35)
    ap.add_argument("--lufs", type=float, default=-13.0)
    ap.add_argument("--prepend", help="hook KOL nói trực tiếp: file@a-b, ghép lên đầu voice")
    ap.add_argument("--prepend-json", help="whisper.json của file hook (để có mốc từng từ)")
    ap.add_argument("--prepend-gap", type=float, default=0.12)
    ap.add_argument("--speed", type=float, default=1.07,
                    help="tăng tốc cả voice (gồm hook), giữ cao độ; mặc định 1.07x (Yan chốt 23/11/2026). "
                         "Clip hook KOL phải chạy cùng tốc độ (cột toc_do trong edit_map)")
    a = ap.parse_args()

    x = decode(a.audio)
    dur = len(x) / SR
    drops = [tuple(float(v) for v in d.split("-")) for d in a.drop]
    # khoảng lặng dài: bỏ phần giữa, giữ keep_gap/2 ở mỗi bên
    sil_cuts = []
    for s, e in silences(a.audio, a.noise, a.min_gap):
        h = a.keep_gap / 2
        if e - s > a.keep_gap:
            sil_cuts.append((s + h, e - h))
    keep = subtract([(0.0, dur)], drops + sil_cuts)

    fade = int(0.008 * SR)
    parts, vmap, pos = [], [], 0.0
    for s, e in keep:
        seg = x[int(s * SR):int(e * SR)].copy()
        if len(seg) > 2 * fade:
            ramp = np.linspace(0, 1, fade, dtype=np.float32)
            seg[:fade] *= ramp
            seg[-fade:] *= ramp[::-1]
        parts.append(seg)
        vmap.append([round(s, 4), round(e, 4), round(pos, 4)])
        pos += len(seg) / SR
    y = np.concatenate(parts)

    gain_db = a.lufs - loudness(y)
    y = y * (10 ** (gain_db / 20))

    # hook KOL: chuẩn hoá riêng (mic máy quay khác mic thu voice) rồi ghép lên đầu
    hook_len, hook_words = 0.0, []
    if a.prepend:
        hp, rng = a.prepend.rsplit("@", 1)
        h0, h1 = (float(v) for v in rng.split("-"))
        hx = decode(hp)[int(h0 * SR):int(h1 * SR)].copy()
        ramp = np.linspace(0, 1, fade, dtype=np.float32)
        hx[:fade] *= ramp
        hx[-fade:] *= ramp[::-1]
        hx = hx * (10 ** ((a.lufs - loudness(hx)) / 20))
        hx = np.concatenate([hx, np.zeros(int(a.prepend_gap * SR), np.float32)])
        hook_len = len(hx) / SR
        y = np.concatenate([hx, y])
        if a.prepend_json:
            for sg in json.load(open(a.prepend_json, encoding="utf-8")):
                hook_words += [[round(w[0] - h0, 3), round(w[1] - h0, 3), w[2]] for w in sg["words"]
                               if h0 <= (w[0] + w[1]) / 2 <= h1]
        vmap = [[v[0], v[1], round(v[2] + hook_len, 4)] for v in vmap]
        pos += hook_len

    peak_lim = 10 ** (-1 / 20)
    os.makedirs(a.out_dir, exist_ok=True)
    out_wav = os.path.join(a.out_dir, "voice_clean.wav")
    tempo = f"atempo={a.speed:.4f}," if abs(a.speed - 1) > 1e-6 else ""  # giữ cao độ giọng
    subprocess.run([FFMPEG, "-nostdin", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1",
                    "-i", "-", "-af", f"{tempo}alimiter=limit={peak_lim:.4f}:level=disabled",
                    "-c:a", "pcm_s16le", out_wav], input=y.astype(np.float32).tobytes(), check=True)
    sp = a.speed

    segs = json.load(open(a.whisper_json, encoding="utf-8"))
    out = []
    if hook_words:
        hw = [[round(w[0] / sp, 3), round(w[1] / sp, 3), w[2]] for w in hook_words]
        out.append({"start": hw[0][0], "end": hw[-1][1], "hook": True,
                    "text": " ".join(w[2] for w in hw), "words": hw})
    for sg in segs:
        if any(c <= sg["start"] and sg["end"] <= d for c, d in drops):
            continue  # cả câu nằm trong đoạn bỏ
        words = [[round(remap(w[0], vmap) / sp, 3), round(remap(w[1], vmap) / sp, 3), w[2]]
                 for w in sg["words"] if not any(c <= (w[0] + w[1]) / 2 <= d for c, d in drops)]
        if words:
            out.append({"start": words[0][0], "end": words[-1][1],
                        "text": " ".join(w[2] for w in words), "words": words})
    json.dump(out, open(os.path.join(a.out_dir, "whisper_clean.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    # mới = (n + t - a) / speed
    json.dump({"speed": sp, "map": vmap}, open(os.path.join(a.out_dir, "voice_map.json"), "w"), indent=0)
    if hook_len:
        print(f"Hook ghép đầu voice: clip hook bắt đầu ở 0, dài {hook_len / sp:.2f}s, tốc độ {sp}x")
    pos /= sp
    print(f"Tốc độ {sp}x. Voice gốc {dur:.1f}s -> sạch {pos:.1f}s ({len(keep)} đoạn, bỏ {len(drops)} khoảng đọc lại, "
          f"rút {len(sil_cuts)} khoảng lặng), chỉnh {gain_db:+.1f} dB -> {out_wav}")


if __name__ == "__main__":
    main()
