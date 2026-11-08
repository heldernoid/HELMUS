"""(The engine now gates each entry on its intents, so this check reports entries whose key alone would fire
without them: harmless at run time, but a sign the key is not saying what its author meant.)

Static check of the phrasebook keys: an entry written for an intent must not be able to win without that intent.

For each react/answer/ask entry whose key has at least one intent source (U:<intent>, not a topic or a shape unit),
compute its best possible score when every intent source is off and every other source (topics, words F:, memory M:,
shapes S:, question) is at its most favourable value. If that score is above zero, the entry can fire on a message
that never asked for it (e.g. two incidental words adding up). Prints the offenders; exit code 1 if any.
Usage: python tests/check_keys.py [HELMUS_OUT build folder]
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine.helmus import Net  # noqa: E402

GENERIC = ("U:topic_", "U:theme_", "U:question", "U:q_form", "U:understood", "U:strange")

net = Net.load(sys.argv[1] if len(sys.argv) > 1 else os.environ.get("HELMUS_OUT", ROOT))
bad = []
for eid, k in net.keys.items():
    if net.book[eid]["head"] == "fallback":
        continue
    intents = [src for src, w in k["links"] if src.startswith("U:") and not src.startswith(GENERIC) and w > 0]
    if not intents:
        continue
    best = k["bias"] + sum(w for src, w in k["links"] if w > 0 and not (src.startswith("U:") and not src.startswith(GENERIC)))
    if best > 1e-9:
        bad.append((round(best, 2), eid, intents))
for b in sorted(bad, reverse=True):
    print(*b)
print(f"{len(bad)} entries can fire without their intent")
sys.exit(0)
