"""Every intent's test sentences: those written as `yes` must fire it (above 0.5), those written as `no` must not."""
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine.helmus import Net  # noqa: E402

OUT = os.environ.get("HELMUS_OUT", ROOT)     # a private build folder, when several people build at once
NET = Net.load(OUT)
with open(os.path.join(OUT, "tests", "intents.json")) as f:
    CASES = json.load(f)


@pytest.mark.parametrize("unit,text,fires", CASES, ids=[f"{u}|{t}" for u, t, _ in CASES])
def test_intent(unit, text, fires):
    _, _, tr = NET.turn({"seed": 1}, text)
    v = tr["units"].get(unit, 0.0)
    assert (v > 0.5) == fires, f"{unit} = {v} for {text!r}; words {tr['words']}"
