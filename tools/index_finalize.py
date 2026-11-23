"""Bước 3 của lập chỉ mục: kiểm tra bản nháp index/<mã>_draft.csv rồi xuất index/<mã>.csv.

Cách dùng:
    python tools/index_finalize.py 5H02D24

Bản nháp có cột: file, in, out, nhom, mo_ta, goc_may, mon, chat_luong
(nhom có thể ghi nhiều nhóm, cách nhau bằng "|": nhóm đầu là nhóm chính).

Script sẽ:
- Sửa tên file cho khớp đúng tên trong kho (so theo tên không phân biệt hoa thường, bỏ đuôi).
- Cắt out về thời lượng thật của file; báo dòng có in >= out.
- Thêm cột dur, sắp theo file + in.
- Báo nhóm không có trong rules/sp/<mã>.md (để Yan duyệt nhóm mới).
- Báo file trong kho chưa có dòng nào.
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INDEX = REPO / "index"
FIELDS = ["file", "in", "out", "dur", "nhom", "mo_ta", "goc_may", "mon", "chat_luong"]
SPECIAL = {"KHAC", "TRUNG"}  # KHAC: không thuộc nhóm nào; TRUNG: file trùng nội dung file khác


def rule_groups(code):
    text = (REPO / "rules" / "sp" / f"{code}.md").read_text(encoding="utf-8")
    groups = set(re.findall(r"\b(?:HOOK|PAIN|HERO|F|STEP|RESULT|CTA|LIFESTYLE|DEMO|TANG|SO_SANH)[A-Z0-9_]*\b", text))
    return groups


def main(code):
    files = list(csv.DictReader((INDEX / f"{code}_files.csv").open(encoding="utf-8-sig")))
    dur = {r["file"]: float(r["duration"] or 0) for r in files}
    by_stem = {Path(f).stem.lower(): f for f in dur}

    rows, problems = [], []
    for i, r in enumerate(csv.DictReader((INDEX / f"{code}_draft.csv").open(encoding="utf-8-sig")), 2):
        real = dur.get(r["file"]) and r["file"] or by_stem.get(Path(r["file"]).stem.lower())
        if not real:
            problems.append(f"dòng {i}: không thấy file {r['file']} trong kho")
            continue
        a, b = float(r["in"]), min(float(r["out"]), dur[real])
        if a >= b:
            problems.append(f"dòng {i}: {real} in {a} >= out {b}")
            continue
        r.update({"file": real, "in": f"{a:.1f}", "out": f"{b:.1f}", "dur": f"{b - a:.1f}"})
        rows.append(r)

    rows.sort(key=lambda r: (r["file"], float(r["in"])))
    out = INDEX / f"{code}.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    known = rule_groups(code) | SPECIAL
    main_groups = Counter(r["nhom"].split("|")[0] for r in rows)
    all_groups = Counter(g for r in rows for g in r["nhom"].split("|"))
    new = sorted(g for g in all_groups if g not in known)
    missing_rule = sorted(g for g in rule_groups(code) if g not in all_groups and not g.startswith("HOOK"))
    covered = {r["file"] for r in rows}
    uncovered = sorted(f for f in dur if f not in covered)

    print(f"{code}: {len(rows)} đoạn, {len(covered)}/{len(dur)} file -> {out.name}")
    print("Nhóm chính:", ", ".join(f"{g} {n}" for g, n in main_groups.most_common()))
    print("Nhóm mới (chưa có trong rules):", ", ".join(new) or "không")
    print("Nhóm trong rules chưa có source:", ", ".join(missing_rule) or "không")
    print("File chưa có đoạn nào:", ", ".join(uncovered) or "không")
    for p in problems:
        print("LỖI", p)


if __name__ == "__main__":
    main(sys.argv[1])
