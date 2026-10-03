"""
Measure King of Teeth against the comp corpus with one script, so every number
in craft/COMPS_ADELINE.md is comparable.

    python craft/tools/compare.py

Reads the full-text comps in comps/ (gitignored) and the manuscript in the
order build_book.py sets it (teaser excluded). Prints stats only.
"""
import os
import re
import statistics as st
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.join(ROOT, "books", "book-1-king-of-teeth"))
sys.stdout.reconfigure(encoding="utf-8")
from build_book import CHAPTER_ORDER, MANUSCRIPT_DIR  # noqa: E402

COMPS = {
    "Haunting Adeline": "_haunting_adeline_fulltext.txt",
    "Hunting Adeline": "_hunting_adeline_fulltext.txt",
    "Deviant King": "_deviant_king_fulltext.txt",
    "God of Malice": "_god_of_malice_fulltext.txt",
    "Hunt the Villain": "_hunt_villain_fulltext.txt",
    "Kiss the Villain": "_kiss_villain_fulltext.txt",
}
EXPL = (r"\b(cock|dick|pussy|cunt|clit|tits|nipples?|balls|ass|asshole|come|came|"
        r"coming|cum|orgasm|thrust\w*|fuck\w*|moan\w*|wet|slick|precum|tongue|lick\w*|"
        r"suck\w*|swallow\w*|nak\w+|throat|chok\w*|spread\w*|grind\w*|knees|"
        r"straddl\w*|hips|thighs)\b")
PROF = (r"\b(fuck\w*|motherfuck\w*|shit\w*|bullshit|damn\w*|goddamn\w*|hell|"
        r"bitch\w*|bastard\w*|asshole|piss\w*|jesus|christ)\b")


def clean(t):
    t = (t.replace("�", '"').replace("“", '"').replace("”", '"')
          .replace("’", "'").replace("‘", "'"))
    t = re.sub(r"OceanofPDF\.com", "", t)
    t = re.sub(r"--- part[^\n]*---", "", t)
    return re.sub(r"\*+", "", t)


def ours():
    parts = []
    for fn, _, typ in CHAPTER_ORDER:
        if typ in ("teaser", "bonus"):
            continue
        t = open(os.path.join(MANUSCRIPT_DIR, fn), encoding="utf-8").read()
        parts.append("\n".join(l for l in t.split("\n")
                               if not l.startswith("#") and not l.startswith("*Placement")))
    return clean("\n".join(parts))


def measure(t):
    words = t.split()
    n = len(words)
    low = t.lower()
    per = lambda pat: round(len(re.findall(pat, low)) * 100000 / n)
    wins = [" ".join(words[i:i + 2000]).lower() for i in range(0, n - 1000, 2000)]
    dens = [len(re.findall(EXPL, w)) * 1000 / len(w.split()) for w in wins]
    hot = [i for i, d in enumerate(dens) if d >= 12]
    sents = [s for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", t)) if s.strip()]
    lens = [len(s.split()) for s in sents]
    quoted = sum(len(q.split()) for q in re.findall(r'"[^"]{1,600}"', t))
    # scene intensity: the three densest non-overlapping 2,000-word stretches,
    # and how much of their text is dialogue (Kent's sex scenes talk)
    slide = sorted(((len(re.findall(EXPL, " ".join(words[i:i + 2000]).lower())) / 2, i)
                    for i in range(0, max(n - 2000, 1), 100)), reverse=True)
    top, used = [], []
    for d, i in slide:
        if all(abs(i - j) >= 2000 for j in used):
            top.append(d)
            used.append(i)
        if len(top) == 3:
            break
    hot_txt = " ".join(" ".join(words[i:i + 2000]) for i in used)
    hot_q = sum(len(q.split()) for q in re.findall(r'"[^"]{1,600}"', hot_txt))
    return {
        "words": n,
        "expl/1k": round(len(re.findall(EXPL, low)) * 1000 / n, 1),
        "hot%": round(100 * len(hot) / len(wins)),
        "first hot%": round(100 * hot[0] / len(wins)) if hot else 100,
        # peak: the densest 2,000-word stretch anywhere, sliding in 100-word steps
        "peak": round(max(len(re.findall(EXPL, " ".join(words[i:i + 2000]).lower())) / 2
                          for i in range(0, max(n - 2000, 1), 100)), 1),
        "top3": round(sum(top) / len(top), 1),
        "hot dlg%": round(100 * hot_q / max(len(hot_txt.split()), 1)),
        "prof": per(PROF),
        "fuck": per(r"\bfuck\w*"),
        "dlg%": round(100 * quoted / n),
        "median": st.median(lens),
        "<11%": round(100 * sum(x < 11 for x in lens) / len(lens)),
        "like a": per(r"\blike a\b"),
        "quiet": per(r"\bquiet\w*"),
        "hands": per(r"\bhands\b"),
    }


if __name__ == "__main__":
    rows = {}
    for name, fn in COMPS.items():
        path = os.path.join(ROOT, "comps", fn)
        if os.path.exists(path):
            rows[name] = measure(clean(open(path, encoding="utf-8", errors="replace").read()))
    rows["KING OF TEETH"] = measure(ours())
    b2 = os.path.join(ROOT, "books", "book-2-vow-of-poison", "manuscript")
    if os.path.isdir(b2):
        sys.path.insert(0, os.path.dirname(__file__))
        from audit import book_units  # noqa: E402
        rows["VOW OF POISON*"] = measure(clean("\n".join(b for _, _, b in book_units(b2, "Cray"))))
    cols = list(next(iter(rows.values())).keys())
    print(f"{'':18}" + "".join(f"{c:>11}" for c in cols))
    for name, r in rows.items():
        print(f"{name[:18]:18}" + "".join(f"{r[c]:>11}" for c in cols))
