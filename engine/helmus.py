"""Helmus, the engine: runs the hand-written network on one message at a time.

Every parameter comes from the edit list (weights/helmus.edits); every line Helmus can say comes from the
phrasebook (weights/phrasebook.json) and the persona table (weights/persona.json). Nothing is trained. The engine
starts with every weight at zero and applies the edits.

Layers (see docs/design.md):
  read   fixed: words, numbers and punctuation; the message's shape (S: features)
  G      grammar: word tags and a weighted context-free grammar (TAG, RULE); the best parse gives each word its tag
         (t:), each phrase its start (g:) and role (r:), and the message its clause features (G:)
  T      fixed: the persona's clock (T: features): its local time and week, read from the persona table
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
DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
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
        self.tags, self.lemmas, self.cats, self.reflects = {}, {}, {}, {}
        self.rules, self.unary, self.binary = [], {}, {}       # grammar: rules, by child (unary), by left child (binary)
        self.literals = set()
        self.phrase_regs = set()
        self.checks, self.check_stop = [], set()             # claims checked against the persona's facts
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
                if len(p) > 4 and p[4] == "phrase":
                    self.phrase_regs.add(p[1])
            elif op == "TAG":
                for w in p[3:]:
                    self.tags.setdefault(w, []).append((p[1], int(p[2])))
                key = f"TAG {p[1]}"
            elif op == "LEMMA":
                for f in p[2:]:
                    self.lemmas[f] = p[1]
                key = "LEMMA " + p[1]
            elif op == "RULE":
                k = (len(p) - 4) // 2                          # RULE lhs kids... cost head roles...
                kids, cost, head, roles = p[2:2 + k], int(p[2 + k]), int(p[3 + k]), p[4 + k:4 + 2 * k]
                rid = len(self.rules)
                self.rules.append((p[1], kids, cost, head, roles))
                if k == 1:
                    self.unary.setdefault(kids[0], []).append(rid)
                else:
                    self.binary.setdefault(kids[0], {}).setdefault(kids[1], []).append(rid)
                self.literals.update(c for c in kids if c.startswith("'"))
                key = f"RULE {rid}"
            elif op == "CHECK":
                self.checks.append((p[1], p[2], p[3].split(","))); key = "CHECK " + p[1]
            elif op == "CHECKSTOP":
                self.check_stop.update(p[1:]); key = "CHECKSTOP"
            elif op == "GCAT":
                self.cats[p[1]] = p[2]; key = "GCAT " + p[1]
            elif op == "REFLECT":
                self.reflects[p[1]] = p[2]; key = "REFLECT " + p[1]
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
    # ---- the grammar ----------------------------------------------------------------------------------------------
    BEAM = 200         # the best analyses kept per span: a guard for long messages; chat rarely reaches it

    def word_tags(self, w):
        if w in self.tags:
            out = list(self.tags[w])
        elif w.isdigit():
            out = list(self.tags.get("<num>", []))
        elif not re.fullmatch(r"[a-z0-9']+", w):
            out = list(self.tags.get("<sym>", []))
        else:
            out = list(self.tags.get("<unk>", []))
            for suffix in ("ing", "ed", "ly", "s"):            # a guess by the ending (fixed rule; the costs are weights)
                if w.endswith(suffix) and len(w) > len(suffix) + 2:
                    out += self.tags.get("<unk-" + suffix + ">", [])
                    break
            if w.endswith("'s") and w[:-2] in self.tags:       # brother's: a possessive of a known word
                out = list(self.tags.get("<poss>", [])) + out
        out += self.tags.get("<any>", [])
        if "'" + w + "'" in self.literals:
            out.append(("'" + w + "'", 0))
        return out

    def _close(self, cell, bp):
        """unary rules, until nothing improves (costs are never above zero, so this ends)"""
        changed = True
        while changed:
            changed = False
            for b in list(cell):
                for rid in self.unary.get(b, ()):
                    a, _, cost, _, _ = self.rules[rid]
                    v = cell[b] + cost
                    if a not in cell or v > cell[a]:
                        cell[a], bp[a] = v, (rid,)
                        changed = True

    def _prune(self, cell, bp):
        if len(cell) <= self.BEAM:
            return cell, bp
        keep = sorted(cell, key=lambda c: -cell[c])[:self.BEAM]   # a stable sort: ties keep their order
        keep = set(keep)
        return {c: v for c, v in cell.items() if c in keep}, {c: v for c, v in bp.items() if c in keep}

    def parse(self, words):
        """the best analysis of the message (CKY over word tags, scores added in thousandths): a tree of
        [category, start, end, children, role, head index] with hidden parts spliced out, or None"""
        n = len(words)
        if not n or not self.rules:
            return None
        V, B = {}, {}                                          # (i, j) -> {category: score}, {category: backpointer}
        for i, w in enumerate(words):
            cell, bp = {}, {}
            for t, c in self.word_tags(w):
                if t not in cell or c > cell[t]:
                    cell[t], bp[t] = c, None
            self._close(cell, bp)
            V[i, i + 1], B[i, i + 1] = self._prune(cell, bp)
        for span in range(2, n + 1):
            for i in range(0, n - span + 1):
                j = i + span
                cell, bp = {}, {}
                for k in range(i + 1, j):
                    L, R = V[i, k], V[k, j]
                    for b, vb in L.items():
                        right = self.binary.get(b)
                        if not right:
                            continue
                        for c, vc in R.items():
                            for rid in right.get(c, ()):
                                a = self.rules[rid][0]
                                v = vb + vc + self.rules[rid][2]
                                if a not in cell or v > cell[a]:
                                    cell[a], bp[a] = v, (rid, k)
                self._close(cell, bp)
                V[i, j], B[i, j] = self._prune(cell, bp)
        top = "Msg" if "Msg" in V[0, n] else None
        if top is None:
            return None

        def build(cat, i, j, role):
            b = B[i, j][cat]
            if b is None:                                      # a word: its tag
                return [cat, i, j, [], role, i]
            _, kids, _, head, roles = self.rules[b[0]]
            spans = [(i, j)] if len(kids) == 1 else [(i, b[1]), (b[1], j)]
            raw = [build(kc, x, y, r if r != "-" else None) for (x, y), kc, r in zip(spans, kids, roles)]
            ch = []
            for node in raw:
                ch += node[3] if node[0].startswith("_") else [node]   # a hidden part's children are ours
            return [cat, i, j, ch, role, raw[head][5]]

        return build("Msg", 0, n, None), V[0, n]["Msg"]

    PERSON = {"i": "1", "we": "1", "me": "1", "us": "1", "you": "2"}
    VERBISH = ("Hv", "Hz", "Hd", "Do", "Dz", "Dd", "Let")      # have, do and let as main verbs read as verbs too
    AUX = ("BeP", "BeD", "Md", "Been")
    WH = ("what", "who", "whom", "which", "whose", "where", "when", "why", "how")                          # an auxiliary alone ("i am", "i can"): its base

    def analyse(self, words):
        """the parse, and what the network reads from it: per word T (t:<tag>, g:<phrase> at a phrase's first word,
        r:<role> at the main word of a phrase with a role), for the message G (the features of its main clauses:
        G:S, G:Sq, G:Sw, G:Simp, G:neg, G:past, G:subj_2, G:verb_<base>...), and the phrases a register may copy"""
        n = len(words)
        out = {"tree": None, "score": 0, "T": [{} for _ in words], "G": {}, "phrases": [], "tag": [None] * n,
               "clauses": []}
        res = self.parse(words)
        if not res:
            return out
        tree, score = res
        out["tree"], out["score"] = tree, score
        T, tags, recs = out["T"], out["tag"], []

        def walk(node, rec, deep=False):
            """deep: inside a verb phrase that is itself an object or complement ("i want [to get a dog]"): its
            roles are not the main clause's"""
            cat, i, j, ch, role, hd = node
            kind = self.cats.get(cat)
            if not ch:
                tags[i] = cat
                T[i]["t:" + cat] = 1.0
            if kind in ("copy", "phrase", "clause", "subclause"):
                T[i]["g:" + cat] = 1.0
            if kind == "copy" and j - i <= 6:
                out["phrases"].append(node)
            if role:
                T[hd]["r:" + role] = 1.0
            if role and rec is not None and not deep:
                rec["roles"].append((role, node))             # a role belongs to the clause the phrase is part of
            if kind == "clause" and rec is not None and rec["main"] and role not in ("comp", "conj"):
                if not ((cat == "Sq" and "Sw" in rec["cats"]) or (cat == "S" and {"Sq", "Sw"} & set(rec["cats"]))):
                    rec["cats"].append(cat)                   # a clause inside a main clause of the same message;
                    #                                           where [are you from] is a wh-question, not yes/no
            elif kind in ("clause", "subclause"):
                main = kind == "clause" and role != "comp" and (rec is None or rec["main"])
                rec = {"cats": [cat], "roles": [], "head": hd, "main": main}
                recs.append(rec)
                deep = False
            for c in ch:
                walk(c, rec, deep or (cat.startswith("VP") and role in ("comp", "obj")))

        walk(tree, None)
        G = out["G"]
        main = [r for r in recs if r["main"]]
        for r in recs:
            if not r["main"]:
                for c in r["cats"]:
                    G["G:sub_" + c] = 1.0
        if not main:
            G["G:frag"] = 1.0
        for r in main:
            for c in r["cats"]:
                G["G:" + c] = 1.0
            subj = False
            info = {"cats": r["cats"], "subj": None, "obj": None, "obj_head": None, "verb": None, "wh": None,
                    "obj_span": None, "obj_main": None}
            for role, node in r["roles"]:
                w = words[node[5]]
                if role in ("wh", "whsubj"):                  # the phrase's question word (in what way -> what)
                    q = next((x for x in words[node[1]:node[2]] if x in self.WH), words[node[1]])
                    G["G:wh_" + q] = G["G:wh"] = 1.0
                    info["wh"] = info["wh"] or q
                if role in ("subj", "whsubj"):
                    subj = True
                    info["subj"] = info["subj"] or w
                    G["G:subj_" + w] = 1.0
                    G["G:subj_" + self.PERSON.get(w, "3")] = 1.0
                elif role == "obj":
                    G["G:obj"] = 1.0
                    if info["obj"] is None:
                        info["obj"] = " ".join(words[node[1]:node[2]])
                        info["obj_head"] = words[self.main_word(node)]
                        info["obj_span"], info["obj_main"] = (node[1], node[2]), self.main_word(node)
                    if w in self.PERSON:
                        G["G:obj_" + self.PERSON[w]] = 1.0
                elif role not in ("comp", "conj", "voc", "pred", "obj2"):
                    G["G:" + role] = 1.0
            if not subj and any(c in ("S", "Sq") for c in r["cats"]):
                G["G:subj_none"] = 1.0
            t = tags[r["head"]] or ""
            hw = words[r["head"]]
            if any(role == "pred" for role, _ in r["roles"]):
                info["verb"] = "be"                           # be and a describing word, a noun, a place, a clause
            elif t.startswith("V") or t in self.VERBISH or t in self.AUX:
                info["verb"] = self.lemmas.get(hw, hw)
            elif any(role == "q" and self.lemmas.get(words[nd[5]]) == "be" for role, nd in r["roles"]):
                info["verb"] = "be"
            if info["verb"]:
                G["G:verb_" + info["verb"]] = 1.0
            info.update({k: any(role == k for role, _ in r["roles"]) for k in ("neg", "past", "fut")})
            out["clauses"].append(info)
        out["frags"] = []                                        # the message's fragments, in order

        def fragments(nd):
            if nd[0] == "Msg":
                for c in nd[3]:
                    fragments(c)
            elif nd[0] == "Frag":
                out["frags"].append(nd[3][0][0] if nd[3] else "Frag")
        fragments(tree)
        frags, node = 0, tree
        while node[3] and node[0] == "Msg":
            frags += 1
            node = node[3][0]
        out["frag_np"] = None                                   # the message's first fragment, when it is a noun phrase
        first = node[3][0] if node[0] == "Frag" and node[3] else None
        if first and first[0] == "NP" and first[2] - first[1] <= 6:
            out["frag_np"] = (first[1], first[2])
            if frags == 1:
                out["G"]["G:np"] = 1.0                          # the whole message is one noun phrase
        if frags == 1 and main:
            G["G:whole"] = 1.0                                # one clause covers the message
        return out

    def reflect(self, words, an, i, j):
        """words i..j as the other side would say them: my -> your, i am -> you are; "you" as a subject -> "i",
        otherwise "me" """
        out = []
        for k in range(i, j):
            w = words[k]
            if w == "you" and "r:subj" not in an["T"][k]:
                out.append(self.reflects.get("you:obj", self.reflects.get(w, w)))
            else:
                out.append(self.reflects.get(w, w))
        return " ".join(out)

    @staticmethod
    def main_word(node):
        """the word a phrase is about: a noun phrase's head; for a verb phrase, its object's (doing laundry ->
        laundry), else its verb"""
        if not node[0].startswith("VP"):
            return node[5]
        todo = list(node[3])
        while todo:
            c = todo.pop(0)
            if c[4] == "obj":
                return c[5]
            if not c[0].startswith(("S", "Rel", "WhCl")):
                todo += c[3]
        return node[5]

    def phrase_at(self, an, p):
        """the phrase a register copies at word p: the longest phrase starting there, else the shortest noun phrase
        around it (at most 6 words), else the word"""
        start = [nd for nd in an["phrases"] if nd[1] == p]
        if start:
            return max(start, key=lambda nd: nd[2] - nd[1])
        around = [nd for nd in an["phrases"] if nd[0] == "NP" and nd[1] <= p < nd[2]]
        if around:
            return min(around, key=lambda nd: nd[2] - nd[1])
        return None

    def features(self, words, an=None):
        X = []
        n = len(words)
        for i, w in enumerate(words):
            f = dict(self.emb.get(w, {}))
            if an:
                f.update(an["T"][i])
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
        clock = self.clock(now)
        words, S = self.read(text)
        calc = S.pop("_calc", None)
        norm = " ".join(words)
        if norm and any(" ".join(self.read(m)[0]) == norm for m in state.get("history", [])):
            S["S:repeat"] = 1.0                              # the user sent this same message before
        an = self.analyse(words)
        X = self.features(words, an)
        A = dict(S)
        A.update(clock["T"])
        A.update(an["G"])
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
        fresh = set()                                        # registers copied from this message
        for reg, slots in self.regs.items():                # the strongest of the register's slot detectors
            best = max(slots, key=lambda sg: A.get("D:" + sg[0], 0.0))
            slot, gate = best
            if A.get(gate, 0.0) > 0.5 and A.get("D:" + slot, 0.0) > 0.5 and where.get(slot, -1) >= 0:
                at = where[slot]
                fresh.add(reg)
                nd = self.phrase_at(an, at) if reg in self.phrase_regs else None
                if nd:
                    regs[reg] = self.reflect(words, an, nd[1], nd[2])
                    hd = self.main_word(nd)
                    regs[reg + ".head"] = self.reflect(words, an, hd, hd + 1)
                else:
                    regs[reg] = words[at]
                    regs.pop(reg + ".head", None)
        for name, reg, facts in self.checks:                 # a claim about the persona: true or not
            if reg in fresh:
                A["C:" + name + ("" if self.agrees(regs[reg], facts) else "_no")] = 1.0
        used = state.get("used", {})
        # K: score every entry; each head takes its best above zero
        # an entry fits when its key alone scores above zero; among those that fit, a used entry ranks lower
        # (repeat penalty) but is not ruled out: a person may say the same kind of thing twice
        raw, scores = {}, {}
        for eid, k in self.keys.items():
            raw[eid] = k["bias"] + sum(w * A.get(src, 0.0) for src, w in k["links"])
            scores[eid] = raw[eid] - self.rates.get("repeat_penalty", 0.6) * used.get(eid, 0)
        turn_no = state.get("turn", 0) + 1
        ctx = {"calc": calc, "regs": regs, "clock": clock, "words": words, "history": state.get("history", []), "an": an}
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
                 "tree": an["tree"], "tags": an["tag"],
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
        clock = ctx["clock"]
        local = clock["local"]

        def fill(m):
            key = m.group(1)
            if key.startswith("p:"):
                for day in clock["days"]:                    # a fact of this day of the week, else the fact
                    if key[2:] in P.get("by_day", {}).get(day, {}):
                        return P["by_day"][day][key[2:]]
                return str(P["facts"].get(key[2:], ""))
            if key == "calc":
                return ctx["calc"] or ""
            if key in ctx["regs"]:
                return ctx["regs"][key]
            if key.startswith("g."):                          # from the parse: the main clause's object, a noun phrase
                return self._gslot(key, ctx)
            if key == "time":
                hr = local.hour % 12 or 12
                return f"{hr}:{local.minute:02d}"
            if key in ("first_msg", "last_msg"):
                hist = ctx["history"]
                if not hist:
                    return ""
                m = (hist[0] if key == "first_msg" else hist[-1]).strip().lower().rstrip("?!.")
                return m if len(m) <= 40 else m[:37].rsplit(" ", 1)[0] + "..."
            if key == "weekday":
                return local.strftime("%A").lower()
            if key == "daypart":
                hr = local.hour
                return "morning" if 5 <= hr < 12 else "afternoon" if 12 <= hr < 17 else "evening" if 17 <= hr < 22 else "night"
            return ""
        return re.sub(r"\{([a-z0-9_:.]+)\}", fill, text).strip()

    def utc_offset(self, now):
        """the persona's offset from UTC at `now`: standard time, plus an hour in summer by the US rule (from 2am on
        the second Sunday of March to 2am on the first Sunday of November)"""
        off = self.persona.get("utc_offset", 0)
        if self.persona.get("dst") == "us":
            def sunday(month, n):                            # the date of the nth Sunday of the month
                first = datetime(now.year, month, 1, tzinfo=timezone.utc)
                return (6 - first.weekday()) % 7 + 1 + 7 * (n - 1)
            start = datetime(now.year, 3, sunday(3, 2), tzinfo=timezone.utc) + timedelta(hours=2 - off)
            end = datetime(now.year, 11, sunday(11, 1), tzinfo=timezone.utc) + timedelta(hours=1 - off)
            if start <= now < end:
                off += 1
        return off

    def clock(self, now):
        """the persona's local time and the T: features of its week (persona "week": what each day holds). The day
        turns over at `day_starts` (5am): at 1am Thursday it is still Wednesday night. Facts of the day of the week
        come from "by_day", a morning version (before 1pm) first"""
        P = self.persona
        local = now.astimezone(timezone(timedelta(hours=self.utc_offset(now))))
        cut = P.get("day_starts", 0)
        d = (local - timedelta(hours=cut)).weekday()
        week = P.get("week", {})
        today, tomorrow, yesterday = (set(week.get(DAYS[(d + k) % 7], [])) for k in (0, 1, -1))
        hr = local.hour
        T = {}
        for name, on in (("work_tonight", "work" in today), ("work_tomorrow", "work" in tomorrow),
                         ("worked_last_night", "work" in yesterday), ("class_today", "class" in today),
                         ("class_ahead", "class" in today and cut <= hr < P.get("class_at", 13)),
                         ("class_done", "class" in today and not cut <= hr < P.get("class_at", 13)),
                         ("class_tomorrow", "class" in tomorrow), ("busy_tomorrow", bool(tomorrow)),
                         ("day_off", not today)):
            if on:
                T["T:" + name] = 1.0
        days = ([DAYS[d] + "_am"] if cut <= hr < 13 else []) + [DAYS[d]]
        return {"local": local, "T": T, "days": days}

    def agrees(self, phrase, facts):
        """a claimed phrase agrees with the persona when one of its words (left out: the CHECKSTOP words; a final s
        does not count) is a word of the named facts; a phrase of stop words only says nothing against them"""
        norm = lambda w: w[:-1] if len(w) > 3 and w.endswith("s") else w   # noqa: E731
        said = {norm(w) for w in re.findall(r"[a-z0-9]+", phrase.lower()) if w not in self.check_stop}
        known = {norm(w) for f in facts for w in re.findall(r"[a-z0-9]+", str(self.persona["facts"].get(f, "")).lower())}
        return not said or bool(said & known)

    def _gslot(self, key, ctx):
        """{g.obj}: the main clause's object, said from the other side (at most 6 words, else its main word);
        {g.obj.head}: its main word; {g.np}: the message's noun phrase when it is only one ("pineapple pizza?")"""
        an, words = ctx["an"], ctx["words"]
        c = an["clauses"][0] if an["clauses"] else None
        if key in ("g.obj", "g.obj.head") and c and c["obj_span"]:
            i, j = c["obj_span"]
            if key == "g.obj" and j - i <= 6:
                return self.reflect(words, an, i, j)
            return self.reflect(words, an, c["obj_main"], c["obj_main"] + 1)
        if key == "g.np" and an.get("frag_np"):
            return self.reflect(words, an, *an["frag_np"])
        return ""

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
