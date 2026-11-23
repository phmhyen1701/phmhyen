"""Soát lần đọc lặp / đọc vấp trong voice thô trước khi làm sạch.

Cách dùng:
    py -3.12 tools/soat_lap.py voice.m4a whisper.json [--noise -48]
    py -3.12 tools/soat_lap.py voice.m4a whisper.json --chunks 22-29.5 31.5-36.8 [--prompt "Nồi Bear..."]

In ra:
  1. Từng câu whisper kèm mốc từng từ. Từ kéo dài > 0.9s đánh dấu !! (whisper hay gộp 2 lần đọc
     lặp thành 1 từ dài; từ cuối câu dài vì dính khoảng lặng thì không sao).
  2. Các cặp câu liền nhau giống nhau (nghi đọc lại cả câu).
  3. Khoảng lặng >= 0.25s và khoảng lặng ngắn >= 0.05s (dùng để chọn mốc --drop rơi vào chỗ lặng).
  4. Với --chunks: whisper riêng từng đoạn trên voice gốc (mốc tuyệt đối), để tách lần đọc bị gộp.
Chỉ đọc file voice, không sửa.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata
from difflib import SequenceMatcher

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ffbin import FFMPEG  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Git Bash trên Windows mặc định cp1252, in tiếng Việt sẽ lỗi


def norm(t):
    t = unicodedata.normalize("NFD", t.lower().replace("đ", "d"))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", "", t)


def silences(path, noise, d):
    err = subprocess.run([FFMPEG, "-nostdin", "-i", path, "-af", f"silencedetect=noise={noise}dB:d={d}",
                          "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8",
                         errors="ignore").stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(st, en))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("whisper_json")
    ap.add_argument("--noise", type=float, default=-48)
    ap.add_argument("--long-word", type=float, default=0.9)
    ap.add_argument("--chunks", nargs="*", default=[], help="đoạn a-b (giây, voice gốc) cần whisper lại riêng")
    ap.add_argument("--prompt", default="")
    a = ap.parse_args()

    segs = json.load(open(a.whisper_json, encoding="utf-8"))
    print("== 1. Mốc từng từ (!! = từ dài bất thường)")
    for g in segs:
        line = " ".join(f"{w[2]}[{w[0]:.2f}-{w[1]:.2f}]" + ("!!" if w[1] - w[0] > a.long_word else "")
                        for w in g["words"])
        print(f"-- [{g['start']:.2f}-{g['end']:.2f}] {line}")

    print("\n== 2. Câu liền nhau giống nhau (nghi đọc lại)")
    found = False
    for p, q in zip(segs, segs[1:]):
        x, y = norm(p["text"]), norm(q["text"])
        head = SequenceMatcher(None, x[:40], y[:40]).ratio()
        if head > 0.6 or SequenceMatcher(None, x, y).ratio() > 0.6:
            found = True
            print(f"  {p['start']:.2f}: {p['text']}\n  {q['start']:.2f}: {q['text']}\n")
    if not found:
        print("  (không có — vẫn phải xem các từ !! ở mục 1)")

    print(f"== 3. Khoảng lặng (ngưỡng {a.noise} dB)")
    print("  >=0.25s: " + " ".join(f"{s:.2f}-{e:.2f}" for s, e in silences(a.audio, a.noise, 0.25)))
    print("  >=0.05s: " + " ".join(f"{s:.2f}-{e:.2f}" for s, e in silences(a.audio, a.noise, 0.05)))

    if a.chunks:
        from faster_whisper import WhisperModel
        from transcribe import load_audio
        audio = load_audio(a.audio)
        model = WhisperModel("medium", device="cpu", compute_type="int8")
        print("\n== 4. Whisper lại từng đoạn (mốc theo voice gốc; mốc từ đầu tiên thường lệch về đầu đoạn)")
        for r in a.chunks:
            s, e = map(float, r.split("-"))
            out, _ = model.transcribe(audio[int(s * 16000):int(e * 16000)], language="vi",
                                      word_timestamps=True, condition_on_previous_text=False,
                                      initial_prompt=a.prompt or None)
            print(f"-- {r}")
            for g in out:
                print("   " + " ".join(f"{w.word.strip()}[{w.start + s:.2f}]" for w in g.words))


if __name__ == "__main__":
    main()
