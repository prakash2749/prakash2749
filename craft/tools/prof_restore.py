#!/usr/bin/env python3
"""Restore inline profanity cut by the human pass, but never standalone tics.

A cut counts as inline when the removed text is one or two words with no
sentence punctuation (e.g. "the whole goddamn room", "opening a fucking jar").
Standalone sentences like "Shit." or "Jesus Christ." stay cut. Lines inside
heat sections are unchanged by the pass, so nothing there is touched.

Usage: python craft/tools/prof_restore.py <book_dir> [...] [--apply]
"""
import re, os, sys, difflib

PROF = re.compile(r"\b(?:fuck\w*|motherfuck\w*|shit\w*|bullshit|damn\w*|goddamn\w*|hell|"
                  r"bitch\w*|bastard\w*|asshole|piss\w*|jesus|christ)\b", re.I)
PUNCT = re.compile(r"[.!?]")


def inline_cut(dele, ins):
    if not PROF.search(dele) or PROF.search(ins):
        return False
    if len(dele.split()) > 2 or PUNCT.search(dele):
        return False
    return len(ins.split()) <= 1


def main():
    apply = "--apply" in sys.argv
    books = [a for a in sys.argv[1:] if not a.startswith("--")]
    total = 0
    for b in books:
        snap, cur = f"{b}/manuscript_pre-human-pass_2026-09-26", f"{b}/manuscript"
        for f in sorted(os.listdir(cur)):
            if not f.endswith(".md") or "original" in f:
                continue
            A = open(f"{snap}/{f}", encoding="utf-8", newline="").read().split("\n")
            C = open(f"{cur}/{f}", encoding="utf-8", newline="").read().split("\n")
            changed = False
            for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, C, autojunk=False).get_opcodes():
                if op != "replace" or i2 - i1 != j2 - j1:
                    continue
                for k in range(i2 - i1):
                    old, new = A[i1 + k], C[j1 + k]
                    ow, nw = re.split(r"(\s+)", old), re.split(r"(\s+)", new)
                    wm = difflib.SequenceMatcher(None, ow, nw, autojunk=False)
                    out, gain, ok = [], 0, True
                    for o, a1, a2, b1, b2 in wm.get_opcodes():
                        dele, ins = "".join(ow[a1:a2]), "".join(nw[b1:b2])
                        if o == "equal":
                            out.append(ins)
                        elif inline_cut(dele, ins.strip()):
                            out.append(dele)
                            gain += len(PROF.findall(dele))
                        else:
                            out.append(ins)  # keep every other edit from the pass
                    if gain:
                        merged = "".join(out)
                        total += gain
                        print(f"{f} +{gain}: {merged.strip()[:120]}")
                        if apply:
                            C[j1 + k] = merged
                            changed = True
            if apply and changed:
                open(f"{cur}/{f}", "w", encoding="utf-8", newline="").write("\n".join(C))
    print("total", total)


if __name__ == "__main__":
    main()
