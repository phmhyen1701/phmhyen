"""Nhận diện SFX và kiểu nhạc nền trong video mẫu bằng mô hình phân loại âm thanh AudioSet (AST).

Chạy trên stem "no_vocals" (đã tách voice bằng demucs), quét cửa sổ 1s, bước 0.25s.

Cách dùng:
    python tools/sfx_classify.py <no_vocals.wav> <shots.csv> <out_prefix>
Đầu ra:
    <out_prefix>_sfx.csv    mỗi dòng 1 SFX: bắt đầu, kết thúc, loại, điểm, cảnh, overlay, lệch so với cắt cảnh
    <out_prefix>_music.csv  điểm trung bình các nhãn nhạc (thể loại, cảm xúc)
"""
import csv
import sys

import librosa
import numpy as np
import torch
from transformers import ASTFeatureExtractor, ASTForAudioClassification

MODEL = "MIT/ast-finetuned-audioset-10-10-0.4593"
WIN, HOP, SR = 1.0, 0.25, 16000

# nhãn AudioSet → tên SFX dùng trong quy tắc
SFX = {
    "Whoosh, swoosh, swish": "whoosh", "Pop": "pop", "Ding": "ding", "Ding-dong": "ding",
    "Bell": "chuông", "Chime": "chuông", "Jingle bell": "chuông", "Tick": "tick",
    "Tick-tock": "tick", "Clock": "tick", "Camera": "chụp ảnh", "Single-lens reflex camera": "chụp ảnh",
    "Click": "click", "Cash register": "tiền", "Coin (dropping)": "tiền", "Boing": "boing",
    "Zing": "zing", "Sound effect": "sfx khác", "Beep, bleep": "beep", "Chink, clink": "leng keng",
    "Glass": "leng keng", "Laughter": "tiếng cười", "Giggle": "tiếng cười", "Baby laughter": "bé cười",
    "Baby cry, infant cry": "bé khóc", "Applause": "vỗ tay", "Cheering": "hò reo",
    "Blender": "máy xay (âm gốc)", "Water tap, faucet": "nước (âm gốc)", "Pour": "rót (âm gốc)",
    "Boiling": "sôi (âm gốc)", "Liquid": "nước (âm gốc)", "Splash, splatter": "nước (âm gốc)",
    "Gasp": "thốt lên", "Slam": "đập", "Thump, thud": "đập", "Knock": "gõ",
    "Typing": "gõ phím", "Computer keyboard": "gõ phím", "Notification": "thông báo",
    "Mechanisms": "cơ khí (âm gốc)", "Microwave oven": "lò (âm gốc)", "Dishes, pots, and pans": "bát đĩa (âm gốc)",
    "Cutlery, silverware": "dao thìa (âm gốc)", "Chopping (food)": "thái (âm gốc)",
}
MUSIC = ["Music", "Pop music", "Hip hop music", "Electronic music", "Dance music", "Funk", "Jazz",
         "Ukulele", "Piano", "Guitar", "Acoustic guitar", "Whistling", "Happy music", "Funny music",
         "Tender music", "Exciting music", "Sad music", "Background music", "Jingle (music)",
         "Theme music", "Christmas music", "Children's music", "Video game music", "Lullaby"]


def main():
    wav, shots_path, out = sys.argv[1:4]
    y, _ = librosa.load(wav, sr=SR, mono=True)
    fe = ASTFeatureExtractor.from_pretrained(MODEL)
    model = ASTForAudioClassification.from_pretrained(MODEL).eval()
    id2 = model.config.id2label
    name2id = {v: k for k, v in id2.items()}

    starts = np.arange(0, max(len(y) / SR - WIN, 0) + 1e-6, HOP)
    probs = []
    for i in range(0, len(starts), 16):
        batch = [y[int(s * SR):int((s + WIN) * SR)] for s in starts[i:i + 16]]
        x = fe(batch, sampling_rate=SR, return_tensors="pt")
        with torch.no_grad():
            probs.append(torch.sigmoid(model(**x).logits).numpy())
    P = np.concatenate(probs)
    np.savez_compressed(out + "_probs.npz", P=P, starts=starts,
                        labels=np.array([id2[i] for i in range(len(id2))]))

    shots = list(csv.DictReader(open(shots_path, encoding="utf-8")))
    cuts = [float(r["bat_dau"]) for r in shots][1:]

    def shot_at(t):
        return next((r for r in reversed(shots) if float(r["bat_dau"]) <= t + 0.05), shots[0])

    events = []
    for lab, short in SFX.items():
        if lab not in name2id:
            continue
        s = P[:, name2id[lab]]
        thr = 0.15
        i = 0
        while i < len(s):
            if s[i] >= thr:
                j = i
                while j + 1 < len(s) and s[j + 1] >= thr:
                    j += 1
                k = i + int(np.argmax(s[i:j + 1]))
                t0, t1 = starts[i], starts[j] + WIN
                tc = starts[k] + WIN / 2
                near = min(cuts, key=lambda c: abs(c - tc)) if cuts else tc
                sh = shot_at(tc)
                events.append({"bat_dau": round(t0, 2), "ket_thuc": round(t1, 2), "dinh": round(tc, 2),
                               "loai": short, "nhan_audioset": lab, "diem": round(float(s[k]), 2),
                               "lech_cat_canh_s": round(tc - near, 2), "canh": sh["stt"],
                               "nhom_source": sh.get("nhom_source", ""),
                               "overlay": sh.get("overlay_tinh_nang", ""),
                               "voice": sh.get("cau_voice", "")[:60]})
                i = j + 1
            else:
                i += 1
    events.sort(key=lambda e: e["dinh"])
    with open(out + "_sfx.csv", "w", newline="", encoding="utf-8") as f:
        fields = ["bat_dau", "ket_thuc", "dinh", "loai", "nhan_audioset", "diem", "lech_cat_canh_s",
                  "canh", "nhom_source", "overlay", "voice"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(events)

    with open(out + "_music.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["nhan", "diem_tb", "ty_le_cua_so_tren_0.2"])
        rows = []
        for lab in MUSIC:
            if lab in name2id:
                s = P[:, name2id[lab]]
                rows.append((lab, float(s.mean()), float((s > 0.2).mean())))
        for r in sorted(rows, key=lambda r: -r[1]):
            w.writerow([r[0], round(r[1], 3), round(r[2], 2)])
    print(f"{out}: {len(events)} SFX, {len(starts)} cửa sổ")


if __name__ == "__main__":
    main()
