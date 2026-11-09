"""Play the held-out interrogations (eval/interrogations.json) through Helmus and through the ELIZA baseline, and
measure what can be measured without a judge:

  fallback   replies where nothing fit and a fallback answered (Helmus did not understand)
  grammar    replies from the grammar's entries (gr.*, in the fallback head): no intent fit, but the parse said what
             kind of message it was (a who-question, a request to describe, a negated statement), and Josh answered
             that kind; counted apart from both understanding and the plain fallbacks
  repeat     a reply said word for word earlier in the same game (the biggest giveaway, per Hutchens)
  length     words per reply (the winning 2025 persona: mostly under 5)
  assistant  replies that sound like an assistant (a fixed list of tells)

The set is split once, by a hash of each game's id: 60 games are the dev split (they may be read to find failures)
and the other 100 the test split (never read while writing Helmus; only their numbers are looked at).

Writes eval/transcripts/<system>-<split>.json for the judges and prints a table per split.
Usage: python eval/run.py
"""
import json
import os
import random
import re
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "baselines", "eliza"))
from engine.helmus import Net  # noqa: E402

TELLS = re.compile(r"\b(as an ai|i'm an ai|language model|i am here to help|how can i assist|great question|"
                   r"certainly|i apologi[sz]e|feel free|i hope this helps)\b", re.I)


def helmus_games(games, out_root=None):
    net = Net.load(out_root or os.environ.get("HELMUS_OUT", ROOT))
    now = datetime(2026, 11, 8, 20, 0, tzinfo=timezone.utc)
    out = []
    for g_i, g in enumerate(games):
        st, turns = {"seed": 1000 + g_i}, []
        for i, m in enumerate(g["messages"]):
            r, st, tr = net.turn(st, m, now + timedelta(minutes=i))
            gram = any(e.startswith("gr.") for e in tr["chosen"].values())
            turns.append({"user": m, "bot": r, "grammar": gram, "chosen": tr["chosen"],
                          "fallback": not gram and "fallback" in {net.book[e]["head"] for e in tr["chosen"].values()}})
        out.append({"id": g["id"], "style": g["style"], "turns": turns})
    return out


def eliza_games(games):
    import eliza
    out = []
    for g_i, g in enumerate(games):
        random.seed(1000 + g_i)
        e = eliza.Eliza()
        e.load(os.path.join(ROOT, "baselines", "eliza", "doctor.txt"))
        turns = []
        for m in g["messages"]:
            r = e.respond(m) or e.final()
            turns.append({"user": m, "bot": r, "fallback": False})
        out.append({"id": g["id"], "style": g["style"], "turns": turns})
    return out


def stats(games):
    n = rep = fb = gr = tell = words = short = 0
    for g in games:
        said = set()
        for t in g["turns"]:
            n += 1
            b = t["bot"].strip().lower()
            rep += b in said
            said.add(b)
            fb += t["fallback"]
            gr += t.get("grammar", False)
            tell += bool(TELLS.search(b))
            w = len(b.split())
            words += w
            short += w <= 5
    return {"replies": n, "fallback %": round(100 * fb / n, 1), "grammar %": round(100 * gr / n, 1),
            "repeat %": round(100 * rep / n, 1),
            "assistant %": round(100 * tell / n, 1), "words/reply": round(words / n, 1), "≤5 words %": round(100 * short / n, 1)}


def split(games):
    """the dev split: the 60 games whose id hashes lowest; the rest is the test split"""
    from engine.helmus import h
    order = sorted(games, key=lambda g: h("split", g["id"]))
    dev = {g["id"] for g in order[:60]}
    return [g for g in games if g["id"] in dev], [g for g in games if g["id"] not in dev]


def main():
    with open(os.path.join(ROOT, "eval", "interrogations.json")) as f:
        games = json.load(f)
    os.makedirs(os.path.join(ROOT, "eval", "transcripts"), exist_ok=True)
    results = {"games": len(games)}
    for part, gs in zip(("dev", "test"), split(games)):
        res = {"helmus": helmus_games(gs), "eliza": eliza_games(gs)}
        for name, out in res.items():
            with open(os.path.join(ROOT, "eval", "transcripts", f"{name}-{part}.json"), "w") as f:
                json.dump(out, f, indent=1)
        cols = list(stats(res["helmus"]).keys())
        print(f"{part} ({len(gs)} games)")
        print(f"  {'system':8s} " + " ".join(f"{c:>12s}" for c in cols))
        results[part] = {"games": len(gs)}
        for name, out in res.items():
            s = stats(out)
            results[part][name] = s
            print(f"  {name:8s} " + " ".join(f"{s[c]:>12}" for c in cols))
    for path in (os.path.join(ROOT, "eval", "results.json"), os.path.join(ROOT, "web", "model", "results.json")):
        try:
            with open(path) as f:
                results["judging"] = json.load(f).get("judging", {})   # judging verdicts stay until judged again
        except (FileNotFoundError, ValueError):
            pass
        with open(path, "w") as f:
            json.dump(results, f, indent=1)


if __name__ == "__main__":
    main()
