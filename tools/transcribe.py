"""Chạy faster-whisper (tiếng Việt) lấy mốc thời gian từng từ.

Cách dùng:
    py -3.12 tools/transcribe.py voice.m4a out.json [--model medium]
Đầu ra: list đoạn {"start", "end", "text", "words": [[start, end, word], ...]}
(cùng định dạng tools/make_srt.py đọc).
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ffbin import FFMPEG  # noqa: E402


def load_audio(path: str, sr: int = 16000) -> np.ndarray:
    """Giải mã bằng ffmpeg (tránh lỗi lệch phiên bản thư viện av của faster-whisper)."""
    raw = subprocess.run(
        [FFMPEG, "-nostdin", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr),
         "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("out_json")
    ap.add_argument("--model", default="medium")
    ap.add_argument("--prompt", default="Máy xay Bear, ăn dặm, cối thuỷ tinh, xay nhuyễn, gioăng.")
    a = ap.parse_args()

    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    segs, info = model.transcribe(
        load_audio(a.audio), language="vi", word_timestamps=True, vad_filter=False,
        initial_prompt=a.prompt, condition_on_previous_text=False,
    )
    out = []
    for s in segs:
        words = [[round(w.start, 3), round(w.end, 3), w.word.strip()] for w in (s.words or [])]
        out.append({"start": round(s.start, 3), "end": round(s.end, 3),
                    "text": s.text.strip(), "words": words})
        print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}", flush=True)
    json.dump(out, open(a.out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Thời lượng {info.duration:.1f}s, {len(out)} đoạn -> {a.out_json}")


if __name__ == "__main__":
    main()
