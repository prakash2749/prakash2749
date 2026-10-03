#!/usr/bin/env python3
"""Heat guard: prove an editing pass left heat/sex sections untouched.

Splits each chapter into sections on '---' scene breaks. A section counts as
heat if it contains any explicit or charged term. Every heat section in the
snapshot must appear byte-identical in the edited file.

Usage: python craft/tools/heat_guard.py <snapshot_dir> <edited_dir> [file ...]
Exit code 1 if any heat section changed.
"""
import os, re, sys

HEAT = re.compile(
    r"\b(cock|cocks|dick|cunt|pussy|clit|tits|nipples?|orgasm\w*|cum|"
    r"come inside|came inside|fuck(?:s|ed|ing)? (?:me|her|him)\b|"
    r"underwear|straddl\w*|moan\w*|arous\w*|soaked|erect\w*|"
    r"kiss\w*|good girl|good boy|between (?:my|her) legs|inside (?:me|her)|"
    r"undress\w*|naked|wet for|grind\w* (?:down|against))\b",
    re.I,
)


# Edits inside heat sections that LO approved on 2026-09-26 ("fix everything").
# The guard applies these to the snapshot before comparing, so these exact
# changes pass and any other change inside a heat section still fails.
ALLOWED = {
    "ch-20.md": [('"Tonight I\'m going to ruin you standing up."\n\n"Good girl," I say.',
                  '"Tonight I\'m going to ruin you standing up."\n\nShe pushes back against my hand anyway.\n\n"Good girl," I say.')],
    "ch-16.md": [("with the door locked and the cat on my feet, doing", "with the door locked and no cat, doing"),
                 ('until you forgot the cat was there."', 'until you forgot the cat ever left."')],
    "ch-18.md": [("and it's the second time I've ever heard him do it.", "twice in one night.")],
    # 2026-09-27 continuity fix: Selene can't be smoothed, so Lucian never took her alarm out.
    "ch-31.md": [("You take the alarm out and I let you, and afterward you heal.",
                  "You bite and I let you, and afterward you heal.")],
}


def sections(text):
    return re.split(r"(?m)^---\s*$", text)


def heat_sections(text):
    return [s.strip() for s in sections(text) if HEAT.search(s)]


def main():
    snap, edit = sys.argv[1], sys.argv[2]
    files = sys.argv[3:] or sorted(f for f in os.listdir(snap) if f.endswith(".md"))
    bad = 0
    for f in files:
        a = open(os.path.join(snap, f), encoding="utf-8").read()
        for old, new in ALLOWED.get(f, []):
            a = a.replace(old, new)
        p = os.path.join(edit, f)
        if not os.path.exists(p):
            print(f"MISSING {f}")
            bad += 1
            continue
        b = open(p, encoding="utf-8").read()
        edited = {s.strip() for s in sections(b)}
        for i, s in enumerate(heat_sections(a)):
            if s not in edited:
                bad += 1
                first = s.splitlines()[0][:70] if s else ""
                print(f"CHANGED {f} heat section starting: {first!r}")
    print("heat guard: clean" if not bad else f"heat guard: {bad} problem(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
