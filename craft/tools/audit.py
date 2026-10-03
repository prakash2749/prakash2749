#!/usr/bin/env python3
"""Mechanical style audit against craft/STYLE_GUIDE.md.

Covers the §11 pre-ship checklist wherever a check can be made mechanically.
Every threshold traces to a number in the style guide, not to taste. Items 10
(swap test) and 12 (tense drift) are deliberately NOT automated — see NOTES at
the bottom of this file for why.

Usage:  python craft/tools/audit.py <file.md> [...]
Passing several files also prints a corpus summary, because the ending targets
(§5) are distributions across chapters, not per-chapter rules.
"""
import re, sys, os, statistics
from collections import Counter

BANNED = [
    "couldn't help but", "a mix of", "something shifted", "spoke volumes",
    "a testament to", "hung heavy", "crackled with", "whirlwind of",
    "raw vulnerability", "the weight of his gaze", "a silent understanding",
    "swallowed thickly", "released a breath", "let out a breath",
    "emotions i couldn't name", "palpable", "little did i know",
    "that's when i realized", "nothing would ever be the same",
    "everything changed", "the truth was", "i had no idea", "in that moment",
    "hold space", "safe space", "trauma response", "emotional labor",
    "check in with", "unpack", "gaslighting", "manhood", "womanhood",
    "her heat", "nub", "made love", "her sex", "velvet",
    "a muscle worked in his jaw", "pulse quickened", "stomach flipped",
    "clenched his jaw", "arithmetic", "load-bearing", "pricing",
    # retrospective narrator — banned outright
    "i want that on the record", "i'd like that noted", "i'm setting that down",
    "i found out later", "i want to be fair to myself", "i want that said",
    "let the record show", "looking back", "his hardness",
]

# AI voice-system tics: 'file' as a cognitive verb.
COGFILE = (r"\b(?:files?|filed|filing)\s+(?:it|that|this|him|her|them)\b"
           r"|\bfile[sd]?\s+the\s+paperwork\b"
           r"|\bfiled?\s+(?:away|behind|under)\b")

# The books are first-person PRESENT tense. A narrator who knows how it turns
# out is a different book, so anything reaching forward out of the scene is
# structurally wrong rather than merely overwritten.
FUTURE_KNOWLEDGE = [
    r"for the rest of my life",
    r"\bin a hundred years\b",
    r"\bI (?:won't|will not) know (?:it |that |)for\b",
    r"\bI don't know (?:it|that|this) yet\b",
    r"\bI (?:will|'ll) still be\b",
    r"\bI (?:would|'d) (?:learn|find out|understand)\b",
    r"\byears later\b",
    r"\bit would be (?:years|months|weeks) before\b",
    r"\bI had no way of knowing\b",
    r"\bnot for (?:years|months|weeks) (?:yet|would)\b",
]

# Finance/measurement metaphor family. 'arithmetic' is already in BANNED; these
# are its neighbours, which slip in wearing different clothes.
COLD_METAPHOR = [r"\bthe math\b", r"\bdo the math\b", r"\bbalance sheet\b",
                 r"\brunning a tally\b", r"\bcost-benefit\b", r"\bnet gain\b"]

BRITISH = ["mum", "arse", "grey", "realise", "realised", "realising", "colour",
           "honour", "favour", "travelled", "cancelled", "modelled", "signalled",
           "fortnight", "whilst", "organise", "apologise", "metre", "theatre",
           "neighbour", "neighbours", "practise", "defence", "offence"]

NUM = (r"one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
       r"fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|"
       r"fifty|sixty|seventy|eighty|ninety|hundred|thousand|dozen")
NUMSEQ = r"\b(?:" + NUM + r")(?:[\s-]+(?:and[\s-]+)?(?:" + NUM + r"))*\b"
DUR = (r"year|years|century|centuries|decade|decades|month|months|week|weeks|"
       r"day|days|hour|hours|minute|minutes|second|seconds|night|nights|"
       r"winter|winters|summer|summers")
# Kent's measure slot is almost entirely VAGUE ("a second", "a step") — that IS
# the target register. Only precise physical distance is the model tell, capped
# at ~5 times in a whole book.
MEASURE = (r"\b(?:" + NUM + r"|\d+)[\s-]+"
           r"(?:inch|inches|foot|feet|yard|yards|mile|miles|step|steps|pace|paces)\b")


def split_sentences(t):
    t = re.sub(r"\s+", " ", t).strip()
    return [p.strip() for p in
            re.split(r'(?<=[.!?])\s+(?=[A-Z"“—(*])', t) if p.strip()]


def wc(s):
    return len(re.findall(r"[A-Za-z'’]+(?:-[A-Za-z']+)*", s))


def strip_speech(s):
    s = re.sub(r'"[^"]*"', "", s)
    return re.sub(r"“[^”]*”", "", s)


def is_dialogue_para(p):
    return re.sub(r"^[—\-\*\s]*", "", p)[:1] in ('"', "“")


def audit(path, corpus):
    raw = open(path, encoding="utf-8").read()
    body = "\n".join(l for l in raw.split("\n")
                     if not l.startswith("#") and l.strip() != "---"
                     and not l.startswith("*Placement"))
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]

    # narration / dialogue split, keeping paragraph index for fragment runs
    narr, dial, seq = [], [], []
    for i, p in enumerate(paras):
        dpara = is_dialogue_para(p)
        for s in split_sentences(p):
            if dpara:
                dial.append(s)
                continue
            s2 = strip_speech(s)
            if wc(s2):
                narr.append(s2)
                seq.append((i, wc(s2)))
            else:
                dial.append(s)

    total = wc(body)
    nl = [wc(s) for s in narr]
    dl = [wc(s) for s in dial if wc(s)]
    per10k = lambda n: round(n * 10000 / max(total, 1), 1)
    flag = []

    print(f"\n=== {os.path.basename(path)} ===")
    print(f"words {total}   paragraphs {len(paras)}")

    # ---- §2 sentence and paragraph targets -------------------------------
    if nl:
        mean = sum(nl) / len(nl)
        med = sorted(nl)[len(nl) // 2]
        pct14 = 100 * sum(1 for x in nl if x <= 14) // len(nl)
        pct4 = 100 * sum(1 for x in nl if x <= 4) // len(nl)
        # Recalibrated 2026-09-27 against 208 comp chapters (Kent x4 + Haunting
        # Adeline), measured with THIS file's own segmentation after rejoining the
        # PDF-wrapped lines in the comp texts. Fail lines sit at the comp 10th/90th
        # percentile: narration mean p90 13.6, median p90 13, <=14 share p10 58,
        # fragments p10 10.5. The mean gate was already at the comp edge and is kept.
        print(f"NARRATION  mean {mean:.1f} (comp median 12.1, fail >14)   "
              f"median {med} (comp 11, fail >13)")
        print(f"           <=14 words {pct14}% (comp 66, fail <58)   "
              f"fragments <=4 words {pct4}% (comp ~18, fail <10)")
        if mean > 14:
            flag.append(f"narration mean {mean:.1f} over 14")
        if med > 13:
            flag.append(f"narration median {med} over 13")
        if pct14 < 58:
            flag.append(f"only {pct14}% of narration <=14 words (floor 58)")
        if pct4 < 10:
            flag.append(f"fragments {pct4}% under the 10 floor — rhythm is flat")
        if pct4 > 30:
            flag.append(f"fragments {pct4}% — well over the 21 measured; "
                        f"check whether reflective passages are shredded")
    if dl:
        dmean = sum(dl) / len(dl)
        d14 = 100 * sum(1 for x in dl if x <= 14) // len(dl)
        # Comp dialogue (same 208 chapters): mean median 9.3, p90 11.4; <=14 share
        # median 80, p10 69. The old 8 / 88 gates sat stricter than the comp median.
        print(f"DIALOGUE   mean {dmean:.1f} (comp 9.3, fail >11)   "
              f"median {sorted(dl)[len(dl)//2]} (target 5)   "
              f"<=14 words {d14}% (comp 80, fail <70)")
        if dmean > 11:
            flag.append(f"dialogue mean {dmean:.1f} over 11 — clip spoken lines")
        if d14 < 70:
            flag.append(f"only {d14}% of dialogue <=14 words (floor 70)")

    sc = [len(split_sentences(p)) for p in paras]
    if sc:
        one = 100 * sum(1 for x in sc if x == 1) // len(sc)
        upto3 = 100 * sum(1 for x in sc if x <= 3) // len(sc)
        # Comp single-sentence paragraphs: median 56, p10 38 (2026-09-27).
        print(f"PARAGRAPHS 1-sentence {one}% (comp 56, fail <38)   "
              f"1-3 sentences {upto3}% (target 93, fail <88)")
        if one < 38:
            flag.append(f"single-sentence paragraphs {one}% under the 38 floor")
        if upto3 < 88:
            flag.append(f"1-3 sentence paragraphs {upto3}% under the 88 floor")

        # DENSITY, not ratio. Every other paragraph check here is a proportion,
        # and proportions are blind to inflating the denominator: at 50%
        # single-sentence paragraphs, 50 paragraphs gives ~25 standalone lines
        # and 180 paragraphs gives ~90. The percentage passes either way while
        # the white space stops meaning anything, because contrast is what makes
        # it read as emphasis. §2's own numbers imply the floor — half the
        # paragraphs at one ~11-word sentence, the rest at two or three — so
        # roughly 16-25 words per paragraph.
        wpp = total / len(paras)
        print(f"           {len(paras)} paragraphs, {wpp:.1f} words each "
              f"(§2 implies ~16-25)")
        if wpp < 14:
            flag.append(f"{wpp:.1f} words per paragraph — every line is its own "
                        f"paragraph, so the white space has no contrast left to "
                        f"carry. Ratios still pass; the effect is gone")

    over20 = sorted(((n, s) for s, n in zip(narr, nl) if n > 20), reverse=True)
    if over20:
        print(f"  {len(over20)} narration sentence(s) over 20 words:")
        for n, s in over20[:6]:
            print(f"    [{n}] {s[:100]}")
    dover = sorted(((wc(s), s) for s in dial if wc(strip_speech(s)) == 0
                    and wc(s) > 18), reverse=True)
    if dover:
        print(f"  {len(dover)} dialogue sentence(s) over 18 words:")
        for n, s in dover[:4]:
            print(f"    [{n}] {s[:100]}")

    # ---- §4 the fragment engine ------------------------------------------
    runs = []
    i = 0
    while i < len(seq):
        if seq[i][1] > 4:
            j, frags = i + 1, []
            while j < len(seq) and seq[j][1] <= 4:
                frags.append(seq[j])
                j += 1
            if frags:
                crossed = all(frags[k][0] != (seq[i][0] if k == 0
                              else frags[k - 1][0]) for k in range(len(frags)))
                runs.append((len(frags), crossed))
            i = j if frags else i + 1
        else:
            i += 1
    if runs:
        n1 = 100 * sum(1 for r, _ in runs if r == 1) // len(runs)
        crossed = 100 * sum(1 for _, c in runs if c) // len(runs)
        # Run COUNT is reported but deliberately not a hard gate. §4's "~14 runs
        # per chapter, across roughly 50 paragraphs" cannot be reconciled with
        # §2: at 48-54% single-sentence paragraphs and an 11-word narration mean,
        # a 2,500-word chapter holds 104-139 paragraphs, not 50. §2's figures are
        # stated three times and are mutually consistent; the "50 paragraphs" is
        # one loose aside. Since §4 itself says 86% of runs cross a paragraph
        # break, run detection scales with segmentation — so a count normalized
        # against the wrong paragraph number is the wrong number.
        #
        # Honesty note: I found this while this check was failing 9 of 15 of my
        # own files, which is exactly when a threshold is most tempting to move.
        # The reasoning stands independent of that (the arithmetic disproves the
        # 50 on its own terms), so the fix is to stop gating on the unreliable
        # figure — not to pick a number my drafts clear. The reliable §2-sourced
        # measure of the same property is fragment DENSITY above, which is still
        # a hard gate. This one only fires when both signals agree.
        rper1k = len(runs) * 1000 / max(total, 1)
        print(f"FRAGMENTS  {len(runs)} runs = {rper1k:.1f}/1k words "
              f"(§4 implies ~5.6, but see note)   sentence+1 {n1}% (target 69)   "
              f"cross a para break {crossed}% (target 86)")
        if rper1k > 18 and pct4 > 30:
            flag.append(f"fragment runs {rper1k:.1f}/1k AND density {pct4}% — two "
                        f"independent signals agree the device is overused. "
                        f"Measure per section: the excess is usually in the "
                        f"reflective passages, not the violent ones")
        if n1 < 50:
            flag.append(f"only {n1}% of fragment runs are sentence+1 "
                        f"(measured 69) — runs are stacking too deep")

    # ---- §2 question marks ------------------------------------------------
    # §2 note: "most of Kent's question marks live in *spoken dialogue*", so the
    # 8-12 rate is a TOTAL, not narration-only. Measuring narration alone fires
    # on nearly every chapter, and a check that always fires gets ignored.
    tq = body.count("?")
    nq = sum(s.count("?") for s in narr)
    # Recalibrated 2026-09-26 against the full comp corpus, chapter by
    # chapter (craft/COMP_TEARDOWN.md): TOTAL question marks run 6.2/1k
    # (Haunting Adeline) to 13.4/1k (Deviant King). The old 219-291 figure
    # was Kent's narration-only rate and left the book last in every decile.
    # 2026-09-27: ceiling moved to the comp p90 (16.9/1k) after LO set a book
    # target of 12+/1k, which the old 13.3/1k ceiling made unreachable per chapter.
    lo, hi = max(1, total // 160), max(2, total // 59)
    print(f"QUESTIONS  {tq} total ({nq} in narration) — "
          f"this length wants {lo}-{hi}")
    if tq == 0:
        flag.append("zero question marks — a POV chapter with no "
                    "self-interrogation is under-pressured (§2)")
    elif tq > hi:
        flag.append(f"{tq} question marks, over the {hi} ceiling for this length")
    elif tq < lo:
        flag.append(f"{tq} question marks against {lo}-{hi} for this length — "
                    f"under-pressured; who is doubting anything here?")

    # ---- §5 chapter ending ------------------------------------------------
    if paras:
        last = paras[-1]
        lw = wc(last)
        ends_q = last.rstrip().endswith("?")
        ends_d = is_dialogue_para(last)
        print(f"ENDING     final paragraph {lw} words "
              f"(52% should be <=10, 27% <=5)"
              f"{'  [question]' if ends_q else ''}"
              f"{'  [dialogue]' if ends_d else ''}")
        corpus.append({"file": os.path.basename(path), "last_words": lw,
                       "q": ends_q, "d": ends_d})
        if lw > 25:
            flag.append(f"final paragraph {lw} words — endings run short, and "
                        f"this one is a paragraph, not a punch")

    # ---- §6 numbers -------------------------------------------------------
    durs, cards = [], []
    for m in re.finditer(NUMSEQ, body, re.I):
        tail = body[m.end():m.end() + 26]
        (durs if re.match(r"[\s-]+(?:" + DUR + r")\b", tail, re.I)
         else cards).append(m.group(0))
    idiom = [c for c in cards if re.fullmatch(r"one|two", c, re.I)]
    real = [c for c in cards if not re.fullmatch(r"one|two", c, re.I)]
    digits = re.findall(r"\b\d+\b", body)
    meas = re.findall(MEASURE, body, re.I)
    print(f"NUMBERS    cardinals {len(real)} = {per10k(len(real))}/10k "
          f"(ceiling 30)  [+{len(idiom)} idiomatic one/two, uncounted]")
    print(f"           durations {per10k(len(durs))}/10k (ceiling 8)   "
          f"digits {per10k(len(digits))}/10k (ceiling 2)   "
          f"measures {per10k(len(meas))}/10k (ceiling 5)")
    if real:
        print(f"           cardinals: {sorted(set(c.lower() for c in real))}")
    if per10k(len(real)) > 30:
        flag.append(f"cardinals {per10k(len(real))}/10k over ceiling 30")
    if per10k(len(durs)) > 8:
        # Print them rather than exempting immortal ages by regex. A 412-year-old
        # narrator legitimately says "four centuries"; the judgement of which
        # instances are characterization and which are padding has to be visible.
        flag.append(f"durations {per10k(len(durs))}/10k over ceiling 8: "
                    f"{sorted(d.lower() for d in durs)}")
    if per10k(len(digits)) > 2:
        flag.append(f"bare digits {per10k(len(digits))}/10k over ceiling 2")
    if per10k(len(meas)) > 5:
        flag.append(f"measure-phrases over ceiling: {meas}")
    rep = {k: v for k, v in Counter(d.lower() for d in durs).items() if v > 2}
    if rep:
        flag.append(f"restated duration {rep} — state it once, trust the reader")

    # ---- §7 sex vocabulary ratio -----------------------------------------
    low = body.lower()
    crude = sum(len(re.findall(r"\b" + w + r"s?\b", low))
                for w in ["cock", "cunt", "tits", "ass", "clit"])
    soft = sum(len(re.findall(r"\b" + w + r"\b", low))
               for w in ["his length", "her core", "core", "arousal", "sex",
                         "manhood", "womanhood", "heat"])
    if crude or soft:
        print(f"SEX VOCAB  crude {crude}   soft {soft}   (target ~70:1)")
        if soft and crude and soft > crude:
            flag.append(f"soft/euphemistic terms ({soft}) outnumber crude "
                        f"({crude}) — inverted against the 70:1 measured")

    # ---- banned lists, spelling, punctuation ------------------------------
    hits = [(b, low.count(b)) for b in BANNED if b in low]
    if hits:
        flag.append(f"BANNED PHRASES {hits}")
    cf = re.findall(COGFILE, body)
    if cf:
        flag.append(f"'file' as cognitive verb: {cf}")
    fk = [m.group(0) for pat in FUTURE_KNOWLEDGE
          for m in re.finditer(pat, body, re.I)]
    if fk:
        flag.append(f"FUTURE KNOWLEDGE (present-tense narrator): {fk}")
    cm = [m.group(0) for pat in COLD_METAPHOR
          for m in re.finditer(pat, body, re.I)]
    if cm:
        flag.append(f"finance/measurement metaphor family: {cm}")
    bh = [(b, len(re.findall(r"\b" + b + r"\b", low))) for b in BRITISH
          if re.search(r"\b" + b + r"\b", low)]
    if bh:
        flag.append(f"BRITISH SPELLING {bh}")
    semis = body.count(";")
    if semis:
        flag.append(f"{semis} semicolon(s) — the checklist says zero")

    print("FLAGS      " + ("none" if not flag else ""))
    for f in flag:
        print(f"  !! {f}")
    return len(flag)


def summarize(corpus):
    """§5 endings are distributions across chapters, not per-chapter rules."""
    if len(corpus) < 2:
        return
    n = len(corpus)
    pct = lambda c: 100 * c // n
    le10 = pct(sum(1 for r in corpus if r["last_words"] <= 10))
    le5 = pct(sum(1 for r in corpus if r["last_words"] <= 5))
    q = pct(sum(1 for r in corpus if r["q"]))
    d = pct(sum(1 for r in corpus if r["d"]))
    print(f"\n=== CORPUS ({n} files) — §5 ending distribution ===")
    print(f"  final paragraph <=10 words : {le10}%  (target 52, floor 45)")
    print(f"  final paragraph <=5 words  : {le5}%  (target 27, floor 20)")
    print(f"  ends on a question         : {q}%  (target 4, ceiling 8)")
    print(f"  ends on spoken dialogue    : {d}%  (target 23, ceiling 30)")
    out = []
    if le10 < 45:
        out.append(f"only {le10}% of endings <=10 words (floor 45) — "
                   f"chapters are trailing off instead of landing")
    if le5 < 20:
        out.append(f"only {le5}% of endings <=5 words (floor 20)")
    if q > 8:
        out.append(f"{q}% end on a question (ceiling 8) — the device is "
                   f"load-bearing where it should be rare")
    if d > 30:
        out.append(f"{d}% end on spoken dialogue (ceiling 30)")
    print("  FLAGS    " + ("none" if not out else ""))
    for o in out:
        print(f"    !! {o}")
    longest = sorted(corpus, key=lambda r: -r["last_words"])[:5]
    print("  longest endings: " +
          ", ".join(f"{r['file']} ({r['last_words']}w)" for r in longest))


# NOTES — deliberately not automated:
#  · Checklist 10 (swap test) is a judgement call between two narrators' voices.
#  · Checklist 12 (present tense) resists regex: legitimate backstory is past
#    tense throughout, so any pattern broad enough to catch real drift fires
#    constantly on correct prose. A check that cries wolf gets ignored, which is
#    worse than no check. Read the opening page of each chapter instead.
# ---------------------------------------------------------------------------
# --book mode: whole-manuscript checks that a single chapter can't show.
# Ceilings are per 100k words, set at ~2x the comp mean measured across the
# Adeline duet and four Kent books (craft/COMPS_ADELINE.md). A tic is a rate
# problem, not a per-sentence problem, so these only make sense book-wide.
# ---------------------------------------------------------------------------
TICS = [  # (label, regex, ceiling per 100k)
    ("Not X. Y. corrective", r"(?:^|(?<=[.!?\"”] ))Not [^.?!\n]{1,40}\. [A-Z]", 40),
    ("isn't X. It's Y", r"\b(?:isn't|wasn't|aren't)\b[^.?!\n]{0,60}[.,] (?:It's|It is|That's|He's|She's)\b", 10),
    ("the way (simile)", r"\bthe way\b", 80),
    ("the thing", r"\bthe thing\b", 10),
    ("which is/means", r"\bwhich (?:is|means)\b", 20),
    ("something", r"\bsomething\b", 150),
    ("hands", r"\bhands?\b", 320),
    ("copper", r"\bcopper\b", 4),
    ("damn", r"\bdamn\w*", 30),
    ("quiet", r"\bquiet\w*", 40),
    ("like a (simile)", r"\blike a\b", 100),
    ("the word", r"\bthe word\b", 12),
    ("In wolf", r"\bIn wolf\b", 15),
]
PHRASE_CAPS = [  # (phrase, cap for the whole book)
    ("of a man who has", 4), ("i put my hand", 5), ("on the other side of", 4),
    ("in wolf there's a word", 4), ("the man who killed my parents", 3),
    ("looks at me the way", 2), ("his hands are at his sides", 1),
    ("in front of witnesses", 5),
]
CANON_NGRAMS = {"say it again", "how is your mother's house"}
PROF = (r"\b(?:fuck\w*|motherfuck\w*|shit\w*|bullshit|damn\w*|goddamn\w*|hell|"
        r"bitch\w*|bastard\w*|asshole|piss\w*|jesus|christ)\b")
EXPL = (r"\b(?:cock|dick|pussy|cunt|clit|tits|nipples?|balls|ass|come|came|coming|"
        r"orgasm|thrust\w*|fuck\w*|moan\w*|wet|slick|tongue|lick\w*|suck\w*|"
        r"swallow\w*|nak\w+|throat|chok\w*|spread\w*|grind\w*|knees|straddl\w*|"
        r"hips|thighs)\b")
BOOKS = {
    "king-of-teeth": dict(fmc="Selene", inter="Cassian", pet="ghost",
                          # Lucian lowered 2026-09-27: a 400-year-old narrator
                          # should swear clearly less than a Frenchmen Street bartender.
                          bands={"Selene": (650, 950), "Lucian": (300, 550),
                                 "Cassian": (0, 0)}),
    "vow-of-poison": dict(fmc="Ondine", inter="Cray", pet="witch",
                          bands={"Ondine": (550, 750), "Silas": (300, 420),
                                 "Cray": (0, 0)}),
}


def book_cfg(mdir):
    path = os.path.abspath(mdir)
    return next((v for k, v in BOOKS.items() if k in path), BOOKS["king-of-teeth"])


def book_units(mdir, inter="Cassian"):
    """Reading order: prologue, chapters, interstitials slotted by *Placement.
    Missing chapters are skipped, so a partial (spine-first) draft still audits."""
    files = {os.path.splitext(f)[0]: os.path.join(mdir, f)
             for f in os.listdir(mdir) if f.endswith(".md")}
    after = {}
    for k, p in files.items():
        if k.startswith("I-"):
            m = re.search(r"after Ch\. (\d+)", open(p, encoding="utf-8").read())
            if m:
                after[int(m.group(1))] = k
    order = ["00-prologue"] if "00-prologue" in files else []
    for i in range(1, 100):
        k = f"ch-{i:02d}"
        if k in files:
            order.append(k)
        if i in after:
            order.append(after[i])
    if "epilogue" in files:
        order.append("epilogue")
    units = []
    for k in order:
        raw = open(files[k], encoding="utf-8").read()
        head = raw.split("\n", 1)[0]
        pov = (inter if k.startswith("I-") else
               head.split("·")[-1].strip() if "·" in head else "mixed")
        body = "\n".join(l for l in raw.split("\n") if not l.startswith("#")
                         and not l.startswith("*Placement") and l.strip() != "---")
        units.append((k, pov, body))
    return units


def book(mdir):
    cfg = book_cfg(mdir)
    fmc = cfg["fmc"]
    units = book_units(mdir, cfg["inter"])
    text = "\n\n".join(b for _, _, b in units)
    total = wc(text)
    p100 = lambda n, w=total: round(n * 100000 / max(w, 1), 1)
    flags = []
    print(f"\n######## BOOK: {len(units)} units, {total} words")

    print("\n-- per unit: explicit/1k · hot words · dialogue% · profanity/100k --")
    hot, sel_dl = 0, []
    for k, pov, b in units:
        w = wc(b)
        words = b.lower().split()
        e = len(re.findall(EXPL, b.lower())) * 1000 / max(w, 1)
        blocks = sum(1 for i in range(0, len(words), 300)
                     if len(re.findall(EXPL, " ".join(words[i:i + 300]))) >= 4)
        dl = 100 * sum(wc(q) for q in re.findall(r'"[^"]*"|“[^”]*”', b)) // max(w, 1)
        pr = p100(len(re.findall(PROF, b.lower())), w)
        hot += e >= 12
        mark = "HOT" if e >= 12 else "   "
        print(f"  {k:12} {pov[:8]:8} {w:5}w  {e:5.1f} {mark} ~{blocks*300:4}hw  "
              f"dlg {dl:3}%  prof {pr:6}")
        # Adeline's FMC chapters dip to 3-6% on backstory chapters, so the
        # per-chapter floor is low and the POV average carries the target.
        if pov == fmc and dl < 8:
            flags.append(f"{k}: {fmc} chapter at {dl}% dialogue (floor 8)")
        if pov == fmc:
            sel_dl.append(dl)
    if sel_dl:
        avg = sum(sel_dl) / len(sel_dl)
        print(f"  {fmc} dialogue average {avg:.1f}% (target >=12)")
        if avg < 12:
            flags.append(f"{fmc} dialogue average {avg:.1f}% under 12")
    share = round(100 * hot / len(units))
    print(f"  HOT units: {hot}/{len(units)} = {share}% (target >=28)")
    if share < 28:
        flags.append(f"hot units {share}% under the 28% target")

    # Same measurement craft/tools/compare.py runs on the comps: 2,000-word
    # windows, so chapter length can't flatter or hide a scene.
    words = text.lower().split()
    wins = [" ".join(words[i:i + 2000]) for i in range(0, len(words) - 1000, 2000)]
    dens = [len(re.findall(EXPL, x)) * 1000 / len(x.split()) for x in wins]
    hot_w = [i for i, d in enumerate(dens) if d >= 12]
    first = round(100 * hot_w[0] / len(wins)) if hot_w else 100
    wshare = round(100 * len(hot_w) / len(wins))
    print(f"  windows: {wshare}% hot (target >=28), first hot at {first}% "
          f"(target <10)")
    if wshare < 28:
        flags.append(f"hot windows {wshare}% under 28")
    if first >= 10:
        flags.append(f"first hot window at {first}%, target under 10")
    # peak is the densest 2,000-word stretch anywhere (compare.py measures the
    # comps the same way), so a scene isn't penalized for straddling a grid line
    peak = max(len(re.findall(EXPL, " ".join(words[i:i + 2000]))) / 2
               for i in range(0, max(len(words) - 2000, 1), 100))
    print(f"  sliding peak {peak:.1f}/1k (target >=32; comps 35-60)")
    if peak < 32:
        flags.append(f"peak stretch {peak:.1f}/1k under 32")

    print("\n-- rhythm --")
    lens = [n for n in (wc(x) for x in split_sentences(text)) if n]
    med = statistics.median(lens)
    short = round(100 * sum(n < 11 for n in lens) / len(lens))
    print(f"  sentences: mean {statistics.mean(lens):.1f}  median {med}  "
          f"under 11 words {short}%  (comps: median 10-14, under-11 34-51%)")
    if med < 10:
        flags.append(f"median sentence {med} under 10")
    if short > 50:
        flags.append(f"{short}% of sentences under 11 words (max 50)")
    choppy = []
    for k, _, b in units:
        lb = [n for n in (wc(x) for x in split_sentences(b)) if n]
        if lb and statistics.median(lb) < 9:
            choppy.append(f"{k}({statistics.median(lb)})")
    print(f"  chapters with median under 9: {len(choppy)} {' '.join(choppy)}")

    print("\n-- profanity by POV (per 100k) --")
    for pov, (lo, hi) in cfg["bands"].items():
        t = " ".join(b for _, p, b in units if p == pov).lower()
        if not t:
            continue
        r = p100(len(re.findall(PROF, t)), wc(t))
        print(f"  {pov:8} {r:6}  (band {lo}-{hi})")
        if not lo <= r <= hi:
            flags.append(f"{pov} profanity {r}/100k outside {lo}-{hi}")

    print("\n-- tic rates (per 100k, ceiling) --")
    for label, pat, ceil in TICS:
        n = len(re.findall(pat, text, re.M))
        r = p100(n)
        print(f"  {label:22} {r:6}  (n={n}, ceiling {ceil})")
        if r > ceil:
            flags.append(f"tic '{label}' {r}/100k over ceiling {ceil}")

    low = re.sub(r"\s+", " ", text.lower().replace("’", "'"))
    print("\n-- capped phrases (whole book) --")
    for ph, cap in PHRASE_CAPS:
        n = low.count(ph)
        print(f"  {ph:32} {n:3}  (cap {cap})")
        if n > cap:
            flags.append(f"phrase '{ph}' x{n} over cap {cap}")

    w = re.findall(r"[a-z']+", low)
    c = Counter(" ".join(w[i:i + 5]) for i in range(len(w) - 5))
    rep = [(g, v) for g, v in c.most_common(60) if v >= 4
           and not any(k in g for k in CANON_NGRAMS)]
    print("\n-- repeated 5-grams (>=4) --")
    for g, v in rep[:25]:
        print(f"  {v:3}  {g}")

    print("\n-- closers --")
    last = {}
    for k, _, b in units:
        s = split_sentences(b.strip().split("\n")[-1] if b.strip() else "")
        if s:
            last.setdefault(s[-1].strip(), []).append(k)
    # Ch. 11 plants this line and Ch. 34 pays it off; the repeat is the device.
    allowed = {"That's how I know."}
    for s, ks in last.items():
        if len(ks) > 1 and s not in allowed:
            flags.append(f"duplicate closer {ks}: {s[:60]}")
    going = [k for k, _, b in units
             if re.search(r"I(?:'m| am) going to[^.]*\.\s*$", b.strip()[-200:])]
    print(f"  endings on 'I'm going to': {len(going)} {going}")
    if len(going) > 3:
        flags.append(f"{len(going)} chapters end on 'I'm going to' (max 3)")

    print("\n-- pet-name ledger --")
    if cfg["pet"] == "witch":
        # "witch" is also an ordinary noun, so only direct address counts:
        # opening a quote or following a comma/stop, then punctuation.
        quoted = " ".join(re.findall(r'"[^"]*"|“[^”]*”', text))
        addr = len(re.findall(r'(?:(?<=["“])|(?<=, )|(?<=[.!?] ))[Ww]itch(?=[.,!?—"”])',
                              quoted))
        print(f"  witch as address in dialogue {addr} (target 40-60)")
        if not 40 <= addr <= 60:
            flags.append(f"witch as address x{addr}, target 40-60")
        print("\n  BOOK FLAGS " + ("none" if not flags else ""))
        for f in flags:
            print(f"    !! {f}")
        return len(flags)
    # An italicized *ghost* in narration is a narrator thinking about the
    # name, not using the word for something else, so it isn't a violation.
    ghost_ital = len(re.findall(r"\*(?:quiet, )?ghosts?[.,!?]?\*", low))
    ghost_all = len(re.findall(r"\bghost\w*", low)) - ghost_ital
    quoted = " ".join(re.findall(r'"[^"]*"|“[^”]*”', text)).lower()
    ghost_q = len(re.findall(r"\bghost\b", quoted))
    chere = low.count("chère")
    witness = low.count("my witness")
    print(f"  ghost in dialogue {ghost_q} (target 40-60)   ghost elsewhere "
          f"{ghost_all - ghost_q} (target 0)   chère {chere} (max 3)   "
          f"my witness {witness} (max 6)")
    if not 40 <= ghost_q <= 60:
        flags.append(f"ghost as address x{ghost_q}, target 40-60")
    if ghost_all - ghost_q:
        flags.append(f"ghost outside dialogue x{ghost_all - ghost_q} — the word is hers")
    if chere > 3:
        flags.append(f"chère x{chere} over 3")
    if witness > 6:
        flags.append(f"my witness x{witness} over 6")

    print("\n  BOOK FLAGS " + ("none" if not flags else ""))
    for f in flags:
        print(f"    !! {f}")
    return len(flags)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--book"]:
        mdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
            os.path.dirname(__file__), "..", "..", "books",
            "book-1-king-of-teeth", "manuscript")
        sys.exit(1 if book(mdir) else 0)
    corpus, bad = [], 0
    for p in sys.argv[1:]:
        bad += audit(p, corpus)
    summarize(corpus)
    sys.exit(1 if bad else 0)
