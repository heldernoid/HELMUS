"""Coverage: for every intent's `yes` sentences, does Helmus answer with something meant for it, or fall back?
A sentence is covered when the reply has a react or answer entry (not a fallback). Prints the coverage by intent
prefix and lists uncovered sentences for one prefix.

Usage: python tests/coverage.py [prefix]        (prefix: core, st_, fo_, bt_, ks_; HELMUS_OUT for a private build)
"""
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine.helmus import Net  # noqa: E402

OUT = os.environ.get("HELMUS_OUT", ROOT)
net = Net.load(OUT)
with open(os.path.join(OUT, "tests", "intents.json")) as f:
    cases = [(u[2:], t) for u, t, yes in json.load(f) if yes and u.startswith("U:")]


def prefix(name):
    return name.split("_")[0] + "_" if name.split("_")[0] in ("st", "fo", "bt", "ks") else "core"


# intents that mean something only right after a question of Helmus's (a bare "mozambique" answers "where r u from")
CONTEXT = {"short_answer", "yes_no_answer", "short_name", "short_age"}
tot, ok, missed = defaultdict(int), defaultdict(int), defaultdict(list)
for name, text in cases:
    if name in CONTEXT:
        continue
    _, _, tr = net.turn({"seed": 1}, text)
    heads = {net.book[e]["head"] for e in tr["chosen"].values()}
    p = prefix(name)
    tot[p] += 1
    if "fallback" not in heads and ({"answer", "react"} & heads):
        ok[p] += 1
    else:
        missed[p].append((name, text))
for p in sorted(tot):
    print(f"{p:6s} {ok[p]:5d}/{tot[p]:<5d} {100 * ok[p] / tot[p]:5.1f}% covered")
want = sys.argv[1] if len(sys.argv) > 1 else None
if want:
    for name, text in missed.get(want, []):
        print(f"  {name}: {text}")
