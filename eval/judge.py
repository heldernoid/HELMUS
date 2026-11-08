"""Blind judging, a cheap stand-in for human interrogators (labelled as such wherever it is reported).

For each game of a split, the same interrogator messages were sent to two witnesses (eval/run.py writes the
transcripts). A judge sees the two transcripts side by side as "Witness A" and "Witness B", in an order set by a hash of
the game id, and says which one is the human, with a confidence and a short reason. Neither name is shown. The judge is
told, as in the 2025 study, that exactly one witness is a human.

  python eval/judge.py packets <split> <system_a> <system_b> [games per packet]   writes eval/judging/<split>/packet-*.json
  python eval/judge.py score <split>                                              reads eval/judging/<split>/verdict-*.json

A verdict file is a list of {"game": id, "human": "A" | "B", "confidence": 0-100, "reason": "..."}.
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine.helmus import h  # noqa: E402

INSTRUCTIONS = (
    "You are the interrogator in a Turing test. In each game below, the same person sent the same messages to two "
    "witnesses at once, in two separate chats. Exactly one witness is a human (a young adult in the US doing this as a "
    "paid online study) and the other is an AI chatbot. Messages were limited to 300 characters; the chats lasted under "
    "five minutes. For each game, decide which witness is the human. Judge as a careful interrogator would: by style, by "
    "how each handled the questions, by consistency, by whether the replies make sense in context. Answer for every game "
    "with JSON objects {\"game\": <id>, \"human\": \"A\" or \"B\", \"confidence\": 0-100, \"reason\": <one short sentence>}.")


def packets(split, a, b, size=20):
    T = {}
    for name in (a, b):
        with open(os.path.join(ROOT, "eval", "transcripts", f"{name}-{split}.json")) as f:
            T[name] = {g["id"]: g for g in json.load(f)}
    out_dir = os.path.join(ROOT, "eval", "judging", split)
    os.makedirs(out_dir, exist_ok=True)
    games, key = [], {}
    for gid in sorted(T[a], key=lambda g: h("judge", g)):
        flip = h("side", gid) < 0.5
        left, right = (b, a) if flip else (a, b)
        key[gid] = {"A": left, "B": right}
        games.append({"game": gid,
                      "A": [[t["user"], t["bot"]] for t in T[left][gid]["turns"]],
                      "B": [[t["user"], t["bot"]] for t in T[right][gid]["turns"]]})
    for i in range(0, len(games), size):
        with open(os.path.join(out_dir, f"packet-{i // size + 1:02d}.json"), "w") as f:
            json.dump({"instructions": INSTRUCTIONS, "games": games[i:i + size]}, f, indent=1)
    with open(os.path.join(out_dir, "key.json"), "w") as f:
        json.dump({"systems": [a, b], "key": key}, f, indent=1)
    print(f"{len(games)} games in {(len(games) + size - 1) // size} packets in {out_dir}")


def score(split):
    d = os.path.join(ROOT, "eval", "judging", split)
    with open(os.path.join(d, "key.json")) as f:
        K = json.load(f)
    wins, n, conf = {s: 0 for s in K["systems"]}, 0, []
    for path in sorted(glob.glob(os.path.join(d, "verdict-*.json"))):
        with open(path) as f:
            for v in json.load(f):
                k = K["key"].get(v["game"])
                if not k or v.get("human") not in ("A", "B"):
                    continue
                wins[k[v["human"]]] += 1
                n += 1
                conf.append(v.get("confidence", 50))
    if not n:
        print("no verdicts yet")
        return
    for s, w in wins.items():
        print(f"{s:10s} judged the human in {w}/{n} games ({100 * w / n:.0f}%)")
    print(f"mean confidence {sum(conf) / len(conf):.0f}")


if __name__ == "__main__":
    if sys.argv[1] == "packets":
        packets(sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 20)
    else:
        score(sys.argv[2])
