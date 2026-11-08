"""Helmus, the engine: runs the hand-written network on one message at a time.

Every parameter comes from the edit list (weights/helmus.edits); every line Helmus can say comes from the
phrasebook (weights/phrasebook.json) and the persona table (weights/persona.json). Nothing is trained. The engine
starts with every weight at zero and applies the edits.

Layers (see docs/design.md):
  read   fixed: words, numbers and punctuation; the message's shape (S: features)
  E      lexicon: word -> named features (EMB), informal spellings -> words (ALIAS)
  D      phrase detectors: a convolution over word positions with windowed taps, clipped to [0, 1]
  U      utterance units: pooled detectors and features, clipped to [0, 1]
  M      memory: carried from turn to turn, m = clip(a * m_prev + links + bias)
  R      registers: words copied from the message (the name after "my name is")
  K      phrasebook keys: each entry's score = key . units + bias - repeat penalty; three heads pick their best
"""
import json
import math
import os
import re
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADS = ("react", "answer", "ask")
WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?|[?!.,]+|[^\sa-z0-9]", re.I)


def clip(v):
    return 0.0 if v < 0 else 1.0 if v > 1 else v


def h(*parts):
    """a stable hash in [0, 1) (FNV-1a, 32 bits, over the UTF-8 bytes): the seeded choice between variants, so a
    chat is reproducible, and the same in the browser (web/helmus.js)"""
    x = 0x811C9DC5
    for b in "|".join(str(p) for p in parts).encode():
        x = ((x ^ b) * 0x01000193) & 0xFFFFFFFF
    return x / 2 ** 32


class Net:
    def __init__(self, edits_text, phrasebook, persona, vocab_text=""):
        self.alias, self.emb = {}, {}
        self.units = {"D": {}, "U": {}, "M": {}}          # name -> {"bias": b, "taps"/"links": [...], "decay": a}
        self.regs = {}                                     # register -> [(slot detector, gate unit)]
        self.keys = {}                                     # entry -> {"bias": b, "links": [(src, w)]}
        self.rates = {}
        self.vocab = set()
        self.why = {}
        for n, raw in enumerate(edits_text.splitlines(), 1):
            line, _, reason = raw.partition("#")
            p = line.split()
            if not p:
                continue
            op = p[0]
            key = None
            if op == "ALIAS":
                self.alias[p[1]] = p[2].split("+"); key = "ALIAS " + p[1]
            elif op == "EMB":
                self.emb.setdefault(p[1], {})[p[2]] = float(p[3]); key = f"EMB {p[1]} {p[2]}"
            elif op == "UNIT":
                self.units[p[1]].setdefault(p[2], {"bias": 0.0, "taps": [], "links": [], "decay": 0.0}); key = f"UNIT {p[1]} {p[2]}"
            elif op == "TAP":
                self.units["D"][p[1]]["taps"].append((int(p[2]), int(p[3]), p[4].split("|"), float(p[5]))); key = f"TAP {p[1]}"
            elif op == "BIAS":
                if p[1] == "K":
                    self.keys.setdefault(p[2], {"bias": 0.0, "links": []})["bias"] = float(p[3])
                else:
                    self.units[p[1]][p[2]]["bias"] = float(p[3])
                key = f"BIAS {p[1]} {p[2]}"
            elif op == "LINK":
                if p[1] == "K":
                    self.keys.setdefault(p[2], {"bias": 0.0, "links": []})["links"].append((p[3], float(p[4])))
                else:
                    self.units[p[1]][p[2]]["links"].append((p[3], float(p[4])))
                key = f"LINK {p[1]} {p[2]} {p[3]}"
            elif op == "DECAY":
                self.units["M"][p[1]]["decay"] = float(p[2]); key = f"DECAY {p[1]}"
            elif op == "REG":
                self.regs.setdefault(p[1], []).append((p[2], p[3])); key = f"REG {p[1]} {p[2]}"
            elif op == "VOCAB":
                self.vocab.add(p[1]); key = "VOCAB " + p[1]
            elif op == "RATE":
                self.rates[p[1]] = float(p[2]); key = f"RATE {p[1]}"
            else:
                raise ValueError(f"line {n}: unknown op {op}")
            self.why.setdefault(key, reason.strip())
        self.book = {e["id"]: e for e in phrasebook}
        # an entry keyed to intents fits only when one of them fired: its intent sources (U: units other than topics
        # and message shapes) with a positive weight; a sum of incidental words never stands in for the question
        generic = ("U:topic_", "U:theme_", "U:question", "U:q_form", "U:understood", "U:strange")
        self.gates = {eid: [src for src, w in k["links"] if w > 0 and src.startswith("U:") and not src.startswith(generic)]
                      for eid, k in self.keys.items()}
        self.persona = persona
        for words in self.alias.values():
            self.vocab.update(words)
        self.known = self.vocab | set(self.emb)
        # real English words (the hand-written vocabulary): never corrected; with the known words, the targets of a fix
        self.real = {w for w in vocab_text.split("\n") if w and not w.startswith("#")}
        self.lexicon_all = sorted(w for w in self.known | self.real if len(w) >= 3 and w.isalpha())

    @classmethod
    def load(cls, root=ROOT):
        with open(os.path.join(root, "weights", "helmus.edits")) as f:
            edits = f.read()
        with open(os.path.join(root, "weights", "phrasebook.json")) as f:
            book = json.load(f)
        with open(os.path.join(root, "weights", "persona.json")) as f:
            persona = json.load(f)
        vpath = os.path.join(root, "weights", "vocab.txt")
        vocab = open(vpath).read() if os.path.exists(vpath) else ""
        return cls(edits, book, persona, vocab)

    # ---- read (fixed) -------------------------------------------------------------------------------------------
    def read(self, text):
        """the message as normalised words (informal spellings expanded) and its shape features"""
        raw = WORD.findall(text)
        S = {"S:any": 1.0}
        if "?" in text:
            S["S:question"] = 1.0
        letters = [c for c in text if c.isalpha()]
        if len(letters) >= 4 and all(c.isupper() for c in letters):
            S["S:shout"] = 1.0
        if re.search(r"(.)\1\1", text.lower()):
            S["S:stretched"] = 1.0
        if not raw:
            S["S:empty"] = 1.0
        words = []
        for tok in raw:
            t = tok.lower()
            if re.fullmatch(r"[?!.,]+", t):
                continue
            t = re.sub(r"([a-z])\1{2,}", r"\1\1", t)        # sooo -> soo (letters only: 9000 stays 9000)
            if re.fullmatch(r"(?:ha|ah){2,}h?|(?:he){2,}h?|l(?:ol)+|(?:lo)+l", t):
                t = "haha" if t[0] in "ah" else "hehe" if t[0] == "h" or t[0] == "e" else "lol"   # hahahaha, lolol
            if t not in self.known and t not in self.alias and t not in self.emb:
                single = re.sub(r"([a-z])\1+", r"\1", t)    # lmaoo -> lmao, hahaa -> haha stays a word it knows
                if single in self.known or single in self.alias:
                    t = single
            words += self.alias.get(t, [t])
        words = [self._near(w) for w in words]
        S["S:words"] = min(1.0, len(words) / 20)
        if words:
            S["S:unknown_share"] = sum(1 for w in words if w not in self.known and not w.isdigit()) / len(words)
        if len(words) <= 2:
            S["S:short"] = 1.0
        math_ = self._math(text)
        if math_:
            S.update(math_)
        return words, S

    def _near(self, w):
        """a misspelling reads as the nearest real word (fixed rule). A word in the vocabulary is real and stays as it
        is ("worry" is never read as "sorry"); a word in neither the vocabulary nor the network's words is taken for a
        typo and read as the word at the smallest edit distance (Damerau: a letter added, dropped, changed, or two
        neighbours swapped), within a budget that grows with the word:
          3-4 letters   two neighbouring letters swapped        hwo -> how, teh -> the
          5-7 letters   one edit                                wehre -> where, robbot -> robot
          8+ letters    two edits                               tommorow -> tomorrow
        The first letter must match (people rarely mistype it). On a tie, a word the network reads wins."""
        if w in self.known or w in self.alias or w in self.real or len(w) < 3 or not w.isalpha():
            return w
        n = len(w)
        budget = 2 if n >= 8 else 1
        best, best_key = w, (budget + 1, 1, 1)
        for cand in self.lexicon_all:
            if cand[0] != w[0] or abs(len(cand) - n) > budget:
                continue
            if n <= 4 and (len(cand) != n or sorted(cand) != sorted(w)):
                continue                                     # short words: only a swap of two neighbours
            d = _dl(w, cand, budget)
            # on a tie: a word of the same length (two letters swapped or one changed is a likelier slip than one
            # added or dropped: "wehre" is "where", not "were"), then a word the network reads
            key = (d, 0 if len(cand) == n else 1, 0 if cand in self.known else 1)
            if d <= budget and key < best_key:
                best, best_key = cand, key
                if key == (1, 0, 0):
                    break
        return best

    @staticmethod
    def _math(text):
        """the calculator layer (fixed): a + - x * / b in the message; the network decides whether to answer"""
        m = re.search(r"(-?\d+(?:\.\d+)?)\s*([+\-x*/]|times|plus|minus|divided by)\s*(-?\d+(?:\.\d+)?)", text.lower())
        if not m:
            return None
        a, op, b = float(m.group(1)), m.group(2), float(m.group(3))
        op = {"times": "*", "x": "*", "plus": "+", "minus": "-", "divided by": "/"}.get(op, op)
        if op == "/" and b == 0:
            return {"S:math": 1.0, "S:math_hard": 1.0}
        v = {"+": a + b, "-": a - b, "*": a * b, "/": a / b if b else 0}[op]
        easy = abs(a) <= 12 and abs(b) <= 12 and op in "+-*" and v == int(v)
        out = {"S:math": 1.0, ("S:math_easy" if easy else "S:math_hard"): 1.0, "_calc": str(int(v)) if v == int(v) else f"{v:.2f}"}
        return out

    # ---- the network ----------------------------------------------------------------------------------------------
    def features(self, words):
        X = []
        n = len(words)
        for i, w in enumerate(words):
            f = dict(self.emb.get(w, {}))
            f.setdefault("w:" + w, 1.0)
            if w not in self.known and not w.isdigit():
                f["shape:unknown"] = 1.0
            if w.isdigit():
                f["shape:number"] = 1.0
            if "c:func" not in f:
                f["shape:content"] = 1.0
            if i == 0:
                f["pos:start"] = 1.0
            if i == n - 1:
                f["pos:end"] = 1.0
            f["shape:any"] = 1.0
            X.append(f)
        return X

    def detect(self, X):
        """D: each detector at each position; returns pooled max and its position"""
        out, where = {}, {}
        n = len(X)
        for name, u in self.units["D"].items():
            best, at = 0.0, -1
            for t in range(n):
                s = u["bias"]
                for lo, hi, feats, w in u["taps"]:
                    m = 0.0
                    for o in range(lo, hi + 1):
                        if 0 <= t + o < n:
                            x = X[t + o]
                            for f in feats:
                                v = x.get(f, 0.0)
                                if v > m:
                                    m = v
                    s += w * m
                v = clip(s)
                if v > best + 1e-9:
                    best, at = v, t
            out["D:" + name], where[name] = best, at
        return out, where

    def turn(self, state, text, now=None):
        """one message in, one reply out; `state` carries memory between turns"""
        now = now or datetime.now(timezone.utc)
        words, S = self.read(text)
        calc = S.pop("_calc", None)
        norm = " ".join(words)
        if norm and any(" ".join(self.read(m)[0]) == norm for m in state.get("history", [])):
            S["S:repeat"] = 1.0                              # the user sent this same message before
        X = self.features(words)
        A = dict(S)
        for f in {k for x in X for k in x}:                  # F: a feature anywhere in the message
            A["F:" + f] = max(x.get(f, 0.0) for x in X)
        D, where = self.detect(X)
        A.update(D)
        for name, u in self.units["U"].items():
            A["U:" + name] = clip(u["bias"] + sum(w * A.get(src, 0.0) for src, w in u["links"]))
        prevM, prevE = state.get("M", {}), state.get("E", {})
        M = {}
        for name, u in self.units["M"].items():
            s = u["bias"] + u["decay"] * prevM.get(name, 0.0)
            for src, w in u["links"]:
                if src.startswith("M:"):
                    s += w * prevM.get(src[2:], 0.0)
                elif src.startswith("E:"):
                    s += w * prevE.get(src[2:], 0.0)
                else:
                    s += w * A.get(src, 0.0)
            M[name] = clip(s)
        for k, v in M.items():
            A["M:" + k] = v
        for k, v in prevE.items():                          # what Helmus said last turn, readable by keys too
            A["E:" + k] = v
        regs = dict(state.get("R", {}))
        for reg, slots in self.regs.items():                # the strongest of the register's slot detectors
            best = max(slots, key=lambda sg: A.get("D:" + sg[0], 0.0))
            slot, gate = best
            if A.get(gate, 0.0) > 0.5 and A.get("D:" + slot, 0.0) > 0.5 and where.get(slot, -1) >= 0:
                regs[reg] = words[where[slot]]
        used = state.get("used", {})
        # K: score every entry; each head takes its best above zero
        # an entry fits when its key alone scores above zero; among those that fit, a used entry ranks lower
        # (repeat penalty) but is not ruled out: a person may say the same kind of thing twice
        raw, scores = {}, {}
        for eid, k in self.keys.items():
            raw[eid] = k["bias"] + sum(w * A.get(src, 0.0) for src, w in k["links"])
            scores[eid] = raw[eid] - self.rates.get("repeat_penalty", 0.6) * used.get(eid, 0)
        turn_no = state.get("turn", 0) + 1
        ctx = {"calc": calc, "regs": regs, "now": now, "words": words, "history": state.get("history", [])}
        said = set(state.get("said", []))
        seed = state.get("seed", 0)

        def pick(cands, key):
            """the best candidate whose lines are not all said already; if every one is spent, the best"""
            ranked = sorted(cands, key=key, reverse=True)
            for e in ranked:
                if any(self._fill(t, ctx) not in said for t in self.book[e]["texts"]):
                    return e
            return ranked[0]

        chosen = {}
        for head in HEADS:
            fit = [e for e in scores if self.book[e]["head"] == head and raw[e] > 0
                   and (not self.gates[e] or any(A.get(g, 0.0) > 0.5 for g in self.gates[e]))]
            if fit:
                chosen[head] = pick(fit, lambda e: (scores[e], -h(seed, e)))
        if "answer" not in chosen and "react" not in chosen:   # nothing fits: the fallback entries
            chosen["answer"] = pick([e for e in scores if self.book[e]["head"] == "fallback"],
                                    lambda e: (scores[e], -h(seed, e, used.get(e, 0))))
        parts = [self.render(chosen[hd], state, turn_no, ctx) for hd in ("react", "answer", "ask") if hd in chosen]
        reply = self.style(" ".join(p for p in parts if p), state.get("seed", 0), turn_no)
        new_used = dict(used)
        for e in chosen.values():
            new_used[e] = new_used.get(e, 0) + 1
        E = {e: 1.0 for e in chosen.values()}
        for hd, e in chosen.items():
            E["@h:" + hd] = 1.0
            if self.book[e].get("group"):
                E["@" + self.book[e]["group"]] = 1.0
        hist = state.get("history", []) + [text]
        new_state = {"seed": state.get("seed", 0), "turn": turn_no, "M": M, "E": E, "R": regs, "used": new_used,
                     "history": hist, "said": state.get("said", []) + [p for p in parts if p]}
        r3 = lambda v: math.floor(v * 1000 + 0.5) / 1000      # noqa: E731 (rounds halves up, as Math.round in the page)
        trace = {"words": words, "units": {k: r3(v) for k, v in A.items() if v > 0.001 and not k.startswith("F:")},
                 "chosen": chosen, "top": sorted(((r3(v), e) for e, v in scores.items()), reverse=True)[:8]}
        return reply, new_state, trace

    # ---- the table: templates and style -------------------------------------------------------------------------------
    def render(self, eid, state, turn_no, ctx):
        """an entry's text: the variant the seed picks, or the next one along if that exact line was already said in
        this chat (never the same line twice while the entry has another)"""
        texts = self.book[eid]["texts"]
        n = state.get("used", {}).get(eid, 0)
        start = int(h(state.get("seed", 0), eid, n) * len(texts))
        said = set(state.get("said", []))
        for k in range(len(texts)):
            out = self._fill(texts[(start + k) % len(texts)], ctx)
            if out not in said:
                return out
        return self._fill(texts[start], ctx)

    def _fill(self, text, ctx):
        P = self.persona

        def fill(m):
            key = m.group(1)
            if key.startswith("p:"):
                return str(P["facts"].get(key[2:], ""))
            if key == "calc":
                return ctx["calc"] or ""
            if key in ctx["regs"]:
                return ctx["regs"][key]
            if key == "time":
                local = ctx["now"].astimezone(timezone(timedelta(hours=P["utc_offset"])))
                hr = local.hour % 12 or 12
                return f"{hr}:{local.minute:02d}"
            if key in ("first_msg", "last_msg"):
                hist = ctx["history"]
                if not hist:
                    return ""
                m = (hist[0] if key == "first_msg" else hist[-1]).strip().lower().rstrip("?!.")
                return m if len(m) <= 40 else m[:37].rsplit(" ", 1)[0] + "..."
            if key == "weekday":
                return ctx["now"].astimezone(timezone(timedelta(hours=P["utc_offset"]))).strftime("%A").lower()
            if key == "daypart":
                hr = ctx["now"].astimezone(timezone(timedelta(hours=P["utc_offset"]))).hour
                return "morning" if 5 <= hr < 12 else "afternoon" if 12 <= hr < 17 else "evening" if 17 <= hr < 22 else "night"
            return ""
        return re.sub(r"\{([a-z0-9_:]+)\}", fill, text).strip()

    def style(self, text, seed, turn_no):
        """the fixed pass of the voice: lowercase, no final full stop; a typo now and then at the rate the weights set"""
        if self.persona.get("lowercase", True):
            text = text.lower()
        text = re.sub(r"\.\s*$", "", text).strip()
        rate = self.rates.get("typo", 0.0)
        words = text.split(" ")
        if rate and len(words) >= 2 and h(seed, turn_no, "typo") < rate:
            i = int(h(seed, turn_no, "typo-at") * len(words))
            w = words[i]
            if len(w) >= 4 and w.isalpha():
                j = 1 + int(h(seed, turn_no, "typo-j") * (len(w) - 2))
                words[i] = w[:j] + w[j + 1] + w[j] + w[j + 2:]   # two letters swapped, the commonest slip
        return " ".join(words)


def _dl(a, b, cap):
    """Damerau-Levenshtein distance (optimal string alignment), stopping early once it passes `cap`"""
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev2, prev = None, list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            c = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + c)
            if prev2 is not None and i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                cur[j] = min(cur[j], prev2[j - 2] + 1)
        if min(cur) > cap:
            return cap + 1
        prev2, prev = prev, cur
    return prev[len(b)]


def _one_edit(a, b):
    if a == b:
        return False
    if len(a) == len(b):
        d = [i for i in range(len(a)) if a[i] != b[i]]
        return len(d) == 1 or (len(d) == 2 and d[1] == d[0] + 1 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]])
    if len(a) > len(b):
        a, b = b, a
    i = 0
    while i < len(a) and a[i] == b[i]:
        i += 1
    return a[i:] == b[i + 1:]


def delay(reply, prev, seed, turn_no):
    """seconds before the reply is shown: the 2025 study's typing delay (a minimum, typing, reading, a skewed pause)"""
    g = -math.log(max(1e-9, 1 - h(seed, turn_no, "think"))) * 0.6      # a right-skewed thinking pause
    return 1.0 + 0.3 * len(reply) + 0.03 * len(prev) + g


if __name__ == "__main__":
    import sys
    net = Net.load()
    st = {"seed": int(sys.argv[1]) if len(sys.argv) > 1 else 1}
    print("(talking to Helmus; empty line to stop)")
    while True:
        try:
            msg = input("> ")
        except EOFError:
            break
        if not msg.strip():
            break
        r, st, tr = net.turn(st, msg)
        print(r)
        if os.environ.get("TRACE"):
            print("   ", tr["chosen"], tr["top"][:4])
