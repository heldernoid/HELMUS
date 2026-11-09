"""The grammar against a treebank written blind (tests/treebank.json: chat messages and the analysis of their main
clause, written by a writer who never saw gen/grammar/). Each field is scored on its own; the test holds the grammar
to a floor per field, so a change that breaks what worked fails.

  python tests/test_grammar.py            prints the scores per field and per area (dev and test)
  python tests/test_grammar.py -v         also the misses of the dev split

Split by a hash of each message, once: 60% dev (its misses may be read to improve the grammar) and 40% test (never
read: only its scores are looked at), as the interrogations are split.
"""
import json
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine.helmus import Net, h  # noqa: E402

FIELDS = ("clause", "neg", "subj", "verb", "obj", "obj_head", "wh", "past", "fut")
FLOOR = {"clause": 0.85, "neg": 0.9, "subj": 0.8, "verb": 0.75, "obj": 0.6, "obj_head": 0.65, "wh": 0.9, "past": 0.9,
         "fut": 0.9}


def analysis(net, text):
    words, _ = net.read(text)
    an = net.analyse(words)
    c = an["clauses"][0] if an["clauses"] else None
    lead = [f for f in an.get("frags", []) if f not in ("IjP", "Dm", "Cc", "TagQ", "X")]
    if lead and lead[0] not in ("S", "Sq", "Sw", "Simp"):
        c = None                                        # "not much hbu": the message starts with a fragment
    if not c:
        return {"clause": "frag", "neg": False, "subj": None, "verb": None, "obj": None, "obj_head": None, "wh": None,
                "past": False, "fut": False}
    kind = next(k for k in ("Sw", "Sq", "Simp", "S") if k in c["cats"])
    return {"clause": kind, "neg": c["neg"], "subj": c["subj"], "verb": c["verb"], "obj": c["obj"],
            "obj_head": c["obj_head"], "wh": c["wh"], "past": c["past"], "fut": c["fut"]}


def score(net, bank):
    right, total, misses = Counter(), Counter(), []
    by_area = defaultdict(Counter)
    for e in bank:
        got = analysis(net, e["text"])
        bad = []
        for f in FIELDS:
            want = e.get(f)
            if f in ("subj", "verb", "obj", "obj_head", "wh") and isinstance(want, str):
                want = want.lower().strip()
            ok = got[f] == want
            right[f] += ok
            total[f] += 1
            if not ok:
                bad.append(f"{f}: {got[f]!r} (want {want!r})")
        by_area[e.get("area", "?")]["all"] += 1
        by_area[e.get("area", "?")]["ok"] += not bad
        if bad:
            misses.append((e["text"], bad))
    return {f: right[f] / total[f] for f in FIELDS}, by_area, misses


def load():
    with open(os.path.join(ROOT, "tests", "treebank.json")) as f:
        bank = json.load(f)
    dev = [e for e in bank if h("treebank", e["text"]) < 0.6]
    test = [e for e in bank if h("treebank", e["text"]) >= 0.6]
    return Net.load(os.environ.get("HELMUS_OUT", ROOT)), dev, test


def test_grammar_treebank():
    net, dev, test = load()
    for part in (dev, test):
        acc, _, _ = score(net, part)
        low = {f: round(a, 3) for f, a in acc.items() if a < FLOOR[f]}
        assert not low, f"fields under their floor: {low}"


if __name__ == "__main__":
    net, dev, test = load()
    res = {name: score(net, part) for name, part in (("dev", dev), ("test", test))}
    print(f"{len(dev)} dev and {len(test)} test messages")
    print(f"  {'field':9s} {'dev':>7s} {'test':>7s}")
    for f in FIELDS:
        print(f"  {f:9s} {100 * res['dev'][0][f]:6.1f}% {100 * res['test'][0][f]:6.1f}%   (floor {100 * FLOOR[f]:.0f}%)")
    print("whole analysis right, by area (dev, test):")
    for a in sorted(set(res["dev"][1]) | set(res["test"][1])):
        d, t = res["dev"][1][a], res["test"][1][a]
        print(f"  {a:14s} {d['ok']:3d}/{d['all']:3d}   {t['ok']:3d}/{t['all']:3d}")
    tot = {n: (sum(c["ok"] for c in r[1].values()), sum(c["all"] for c in r[1].values())) for n, r in res.items()}
    print(f"  {'all':14s} {tot['dev'][0]:3d}/{tot['dev'][1]:3d}   {tot['test'][0]:3d}/{tot['test'][1]:3d}")
    if "-v" in sys.argv:
        for text, bad in res["dev"][2]:
            print(f"- {text}\n    " + "; ".join(bad))
