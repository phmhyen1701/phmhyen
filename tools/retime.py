"""Quy đổi mốc thời gian sau khi làm sạch lại voice (bỏ thêm câu đọc lặp, đổi tốc độ...).

Cách dùng:
    py -3.12 tools/retime.py old_voice_map.json new_voice_map.json file.csv:cot1,cot2 [file2.csv:cot ...]

- voice_map.json do tools/clean_voice.py ghi ra (bản cũ là list, bản mới là {"speed", "map"}).
- Mốc cũ -> thời gian trên voice gốc -> mốc mới. Phần hook ghép đầu (trước đoạn voice đầu tiên)
  chỉ chia theo tốc độ. Mốc rơi vào đoạn đã bỏ thì dồn về đầu đoạn giữ kế tiếp.
- Ghi đè file csv (giữ BOM để Excel đọc đúng tiếng Việt). Sau khi chạy nên soát lại ranh giới cảnh
  với whisper của voice mới.
"""
import csv
import io
import json
import sys


def load(path):
    d = json.load(open(path, encoding="utf-8"))
    if isinstance(d, list):
        return 1.0, d
    return float(d["speed"]), d["map"]


def to_raw(t, vmap, speed):
    """mốc trên voice sạch -> ('hook', giây) hoặc ('raw', giây gốc)."""
    t *= speed
    if t < vmap[0][2]:
        return "hook", t
    for a, b, n in vmap:
        if n <= t <= n + (b - a) + 1e-6:
            return "raw", a + (t - n)
    a, b, n = vmap[-1]
    return "raw", b


def from_raw(kind, x, vmap, speed):
    if kind == "hook":
        return x / speed
    for a, b, n in vmap:
        if x < a:
            return n / speed
        if x <= b:
            return (n + x - a) / speed
    a, b, n = vmap[-1]
    return (n + b - a) / speed


def main():
    old_sp, old = load(sys.argv[1])
    new_sp, new = load(sys.argv[2])
    for spec in sys.argv[3:]:
        path, cols = spec.rsplit(":", 1)
        cols = cols.split(",")
        rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
        for r in rows:
            for c in cols:
                if r.get(c, "").strip():
                    r[c] = f"{from_raw(*to_raw(float(r[c]), old, old_sp), new, new_sp):.2f}"
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator="\r\n")
        w.writeheader()
        w.writerows(rows)
        open(path, "w", encoding="utf-8-sig", newline="").write(buf.getvalue())
        print(f"{path}: quy đổi {len(rows)} dòng, cột {', '.join(cols)}")


if __name__ == "__main__":
    main()
