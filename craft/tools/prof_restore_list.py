#!/usr/bin/env python3
"""Restore a hand-picked list of profanity-bearing sentences the human pass cut.

Each entry is (book_dir, file, exact sentence from the snapshot). For the
paragraph that held it in the snapshot, the sentence is put back after its
preceding sentence in the current paragraph. The current paragraph is found
by matching that preceding sentence. It prints anything it can't place.

Usage: python craft/tools/prof_restore_list.py <list.tsv> [--apply]
"""
import re, sys, difflib

SENT = re.compile(r'[^.!?]+[.!?]+[*"”)]*\s*')


def load(p):
    return open(p, encoding="utf-8", newline="").read()


def main():
    listfile, apply = sys.argv[1], "--apply" in sys.argv
    rows = [l.rstrip("\n").split("\t") for l in open(listfile, encoding="utf-8") if l.strip()]
    cache = {}
    ok = miss = 0
    for book, f, target in rows:
        snap = load(f"{book}/manuscript_pre-human-pass_2026-09-26/{f}")
        key = f"{book}/manuscript/{f}"
        cur = cache.setdefault(key, load(key))
        para = next((p for p in snap.split("\n") if target in p), None)
        if para is None:
            print("NOT IN SNAPSHOT", f, target); miss += 1; continue
        if target in cur:
            print("ALREADY PRESENT", f, target); continue
        sents = [s for s in SENT.findall(para)]
        idx = next(i for i, s in enumerate(sents) if target in s)
        placed = False
        # anchor on the nearest preceding sentence still present in the current text
        for j in range(idx - 1, -1, -1):
            anchor = sents[j].strip()
            if len(anchor) > 12 and cur.count(anchor) == 1:
                cur = cur.replace(anchor, anchor + " " + target, 1)
                placed = True
                break
        if not placed:
            for j in range(idx + 1, len(sents)):
                anchor = sents[j].strip()
                if len(anchor) > 12 and cur.count(anchor) == 1:
                    cur = cur.replace(anchor, target + " " + anchor, 1)
                    placed = True
                    break
        if placed:
            cache[key] = cur; ok += 1
            print("OK", f, target)
        else:
            print("NO ANCHOR", f, target); miss += 1
    if apply:
        for k, v in cache.items():
            open(k, "w", encoding="utf-8", newline="").write(v)
    print(f"placed {ok}, missed {miss}")


if __name__ == "__main__":
    main()
