"""Tạo file .srt từ kịch bản (chữ chuẩn) + mốc thời gian của faster-whisper.

Chữ lấy từ kịch bản (không lỗi chính tả), thời gian lấy từ whisper.
Hai bên được so khớp mềm từng từ (bỏ dấu, chấp nhận nhận sai gần đúng).

Cách dùng:
    python tools/make_srt.py script.txt whisper.json out.srt [--max-words 4] [--max-dur 1.6]
Trong script.txt có thể đặt dấu | để ép xuống dòng (giữ nguyên từ ghép như "nấu nướng", "màn hình").
whisper.json: list các đoạn, mỗi đoạn có "words": [[start, end, word], ...]
"""
import argparse
import json
import re
import unicodedata
from difflib import SequenceMatcher

PUNCT_BREAK = re.compile(r"[,.?!;:…]$")


def norm(w: str) -> str:
    w = w.lower().replace("đ", "d")
    w = unicodedata.normalize("NFD", w)
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", w)


def sim(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    return SequenceMatcher(None, a, b).ratio()


def align(script_toks, asr_toks):
    """Needleman-Wunsch: trả về dict chỉ_số_kịch_bản -> chỉ_số_whisper."""
    n, m = len(script_toks), len(asr_toks)
    GAP = -0.4
    score = [[0.0] * (m + 1) for _ in range(n + 1)]
    back = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0] = i * GAP
        back[i][0] = 1
    for j in range(1, m + 1):
        score[0][j] = j * GAP
        back[0][j] = 2
    for i in range(1, n + 1):
        a = script_toks[i - 1]
        for j in range(1, m + 1):
            s = sim(a, asr_toks[j - 1])
            diag = score[i - 1][j - 1] + (s * 2 - 0.8)
            up = score[i - 1][j] + GAP
            left = score[i][j - 1] + GAP
            best = max(diag, up, left)
            score[i][j] = best
            back[i][j] = 0 if best == diag else (1 if best == up else 2)
    mapping = {}
    i, j = n, m
    while i > 0 or j > 0:
        b = back[i][j]
        if i > 0 and j > 0 and b == 0:
            if sim(script_toks[i - 1], asr_toks[j - 1]) >= 0.5:
                mapping[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif i > 0 and (j == 0 or b == 1):
            i -= 1
        else:
            j -= 1
    return mapping


def word_times(script_words, asr_words):
    s_norm = [norm(w) for w in script_words]
    a_norm = [norm(w[2]) for w in asr_words]
    mp = align(s_norm, a_norm)
    times = [None] * len(script_words)
    for si, ai in mp.items():
        times[si] = [asr_words[ai][0], asr_words[ai][1]]
    # nội suy cho từ không khớp được
    known = [i for i, t in enumerate(times) if t]
    for i, t in enumerate(times):
        if t:
            continue
        prev = max([k for k in known if k < i], default=None)
        nxt = min([k for k in known if k > i], default=None)
        start = times[prev][1] if prev is not None else 0.0
        end = times[nxt][0] if nxt is not None else start + 0.3
        span_ids = list(range((prev or -1) + 1, nxt if nxt is not None else len(times)))
        k = span_ids.index(i)
        step = max(end - start, 0.05) / len(span_ids)
        times[i] = [start + k * step, start + (k + 1) * step]
    return times, len(mp)


def group_cues(words, times, max_words, max_dur, pause=0.25, forced=frozenset()):
    """Tách cụm ở dấu câu / chỗ nghỉ / dấu | trong file lời, rồi chia đều mỗi cụm
    (tránh dòng chỉ còn 1 chữ lẻ). forced: chỉ số từ có dấu | ngay sau."""
    phrases, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        last = i == len(words) - 1
        gap = (times[i + 1][0] - times[i][1]) if not last else 0
        if last or i in forced or PUNCT_BREAK.search(w) or gap >= pause:
            phrases.append(cur)
            cur = []
    cues = []
    for ph in phrases:
        k = -(-len(ph) // max_words)  # số dòng tối thiểu
        while True:
            size, extra = divmod(len(ph), k)
            parts, pos = [], 0
            for j in range(k):
                n = size + (1 if j < extra else 0)
                parts.append(ph[pos:pos + n])
                pos += n
            too_long = any(times[p[-1]][1] - times[p[0]][0] > max_dur and len(p) > 2 for p in parts)
            if not too_long or k >= len(ph):
                break
            k += 1
        cues += parts
    return cues


def fmt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("whisper_json")
    ap.add_argument("out_srt")
    ap.add_argument("--max-words", type=int, default=4)
    ap.add_argument("--max-dur", type=float, default=1.6)
    a = ap.parse_args()

    text = open(a.script, encoding="utf-8").read()
    # dấu | trong file lời = ép xuống dòng (không hiện ra), để không cắt ngang từ ghép
    words, forced = [], set()
    for tok in text.replace("|", " | ").split():
        if tok == "|":
            if words:
                forced.add(len(words) - 1)
        else:
            words.append(tok)
    segs = json.load(open(a.whisper_json, encoding="utf-8"))
    asr = [w for s in segs for w in s["words"] if norm(w[2])]
    times, matched = word_times(words, asr)
    cues = group_cues(words, times, a.max_words, a.max_dur, forced=frozenset(forced))

    out = []
    for n, c in enumerate(cues, 1):
        start = times[c[0]][0]
        end = times[c[-1]][1]
        if n < len(cues):  # nối liền cue sau nếu khoảng nghỉ ngắn để chữ không nháy
            nxt = times[cues[n][0]][0]
            if nxt - end < 0.35:
                end = nxt
        txt = " ".join(words[i] for i in c).rstrip(",.;:")
        out.append(f"{n}\n{fmt(start)} --> {fmt(end)}\n{txt}\n")
    open(a.out_srt, "w", encoding="utf-8").write("\n".join(out))
    print(f"{len(words)} từ kịch bản, khớp {matched} từ với whisper "
          f"({matched / len(words):.0%}), {len(cues)} dòng phụ đề -> {a.out_srt}")


if __name__ == "__main__":
    main()
