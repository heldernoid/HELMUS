"""The authoring language for Helmus. Content modules (gen/lexicon.py, gen/intents/*, gen/memory.py,
gen/phrasebook/*, gen/persona/*) call these functions; gen/generate.py turns what they declare into the edit list
(weights/helmus.edits, every line with its reason), the phrasebook table and the persona table.

Nothing here fits anything: each function writes the weights its arguments spell out.

Patterns (for `intent`), words separated by spaces, all lowercase, after informal spellings are expanded:
  word        that word                         a|b        either word
  @class      any word of a class (cls)         [x] [a|b]  optional
  *           up to 3 other words here          !x         not after x (x within the 2 words before the next word)
  ^ / $       at the start / end of the message {slot}     any word, copied into a register (see `register`); {slot:unknown} only a word not in the lexicon
  #num        any number (in figures or a number word)
  a|b_c       one of several word sequences: "vacation|a_trip" is "vacation" or "a trip"
  {slot:kind} kinds: (none) any word, unknown (not in the lexicon), content (not a function word such as the, a,
              my), #num (a number), @class (a word of that class), t:<tag> (a word the grammar tags so: t:Np)
"""
import re

DECL = {"edits": [], "book": [], "persona": None, "tests": [], "units": {"D": set(), "U": set(), "M": set()}}
_seen = set()


def _e(line, why):
    if not why or not why.strip():
        raise ValueError(f"every weight needs a reason: {line}")
    DECL["edits"].append(f"{line}  # {why.strip()}")


def _unit(layer, name, why):
    if name in DECL["units"][layer]:
        return
    DECL["units"][layer].add(name)
    _e(f"UNIT {layer} {name}", why)


# ---- lexicon ------------------------------------------------------------------------------------------------------
def cls(name, words, why):
    """a word class: every word in `words` gets the feature c:<name>"""
    for w in words.split() if isinstance(words, str) else words:
        key = (w, name)
        if key in _seen:
            continue
        _seen.add(key)
        _e(f"EMB {w} c:{name} 1", f"{w} is {why}")


def known(words, why):
    """ordinary words Helmus should read as themselves: known words are never taken for a typo of another word"""
    for w in words.split():
        if w not in _vocab:
            _vocab.add(w)
            _e(f"VOCAB {w}", why)


def alias(raw, words, why):
    """an informal spelling read as words: alias('u', 'you'), alias('ngl', 'not gonna lie')"""
    _e(f"ALIAS {raw} {'+'.join(words.split())}", why)


def aliases(table, why):
    for raw, words in table.items():
        alias(raw, words, why)


# ---- detectors and intents ------------------------------------------------------------------------------------------
GAP = 3


def _elements(pattern):
    out = []
    for tok in pattern.split():
        if tok == "*":
            out.append(("gap",))
        elif tok == "^":
            out.append(("start",))
        elif tok == "$":
            out.append(("end",))
        elif tok.startswith("{") and tok.endswith("}"):
            name, _, kind = tok[1:-1].partition(":")
            feat = {"unknown": "shape:unknown", "content": "shape:content", "": "shape:any", "#num": "shape:number|c:number"}.get(kind)
            if feat is None and kind.startswith("@"):
                feat = "c:" + kind[1:]
            if feat is None and kind.startswith("t:"):        # a word the grammar tags so (t:Np, a name)
                feat = kind
            if feat is None:
                raise ValueError(f"unknown slot kind {kind} in {pattern}")
            out.append(("slot", name, feat))
        elif tok.startswith("!"):
            out.append(("not", _feats(tok[1:])))
        elif tok.startswith("[") and tok.endswith("]"):
            out.append(("opt", _feats(tok[1:-1])))
        else:
            out.append(("req", _feats(tok)))
    return out


_vocab = set()


def _feats(tok):
    if tok == "#num":
        return "shape:number|c:number"
    for a in tok.split("|"):
        if not a.startswith(("@", "#")) and a not in _vocab:
            _vocab.add(a)
            _e(f"VOCAB {a}", "a word a detector reads: known, so never read as a typo of another word")
    return "|".join("shape:number|c:number" if a == "#num" else ("c:" + a[1:]) if a.startswith("@") else ("w:" + a)
                    for a in tok.split("|"))


def compile_pattern(name, pattern, why):
    """one detector: required words at the right offsets (an AND), optional words and gaps widen the window of the
    words after them, `!x` blocks, `{slot}` is the anchor whose position is copied"""
    els = _elements(pattern)
    core = [i for i, e in enumerate(els) if e[0] in ("req", "slot")]
    if not core:
        raise ValueError(f"pattern needs a word: {pattern}")
    anchor = next((i for i, e in enumerate(els) if e[0] == "slot"), core[0])
    taps, k = [], 0
    # forward from the anchor
    lo = hi = 0
    pend_not = []
    for e in els[anchor + 1:]:
        if e[0] == "gap":
            hi += GAP
        elif e[0] == "opt":
            hi += 1
        elif e[0] == "not":
            pend_not.append(e[1])
        elif e[0] == "end":
            taps.append((lo, hi, "pos:end", 1.0)); k += 1
        elif e[0] in ("req", "slot"):
            lo, hi = lo + 1, hi + 1
            for f in pend_not:
                taps.append((lo - 2, hi - 1, f, -1.0))
            pend_not = []
            taps.append((lo, hi, e[1] if e[0] == "req" else e[2], 1.0)); k += 1
    # backward from the anchor
    lo = hi = 0
    for e in reversed(els[:anchor]):
        if e[0] == "gap":
            lo -= GAP
        elif e[0] == "opt":
            lo -= 1
        elif e[0] == "start":
            taps.append((lo, hi, "pos:start", 1.0)); k += 1
        elif e[0] == "not":
            taps.append((lo - 2, hi - 1, e[1], -1.0))
        elif e[0] in ("req", "slot"):
            lo, hi = lo - 1, hi - 1
            taps.append((lo, hi, e[1] if e[0] == "req" else e[2], 1.0)); k += 1
    a = els[anchor]
    taps.append((0, 0, a[1] if a[0] == "req" else a[2], 1.0)); k += 1
    _unit("D", name, f"detector for '{pattern}' ({why})")
    for lo, hi, f, w in taps:
        _e(f"TAP {name} {lo} {hi} {f} {w:g}", f"'{pattern}': {'blocked by' if w < 0 else 'needs'} {f} at {lo}..{hi}")
    _e(f"BIAS D {name} {-(k - 1):g}", f"AND of the {k} required parts of '{pattern}'")
    return name, a[1] if a[0] == "slot" else None


def expand(pattern, limit=8):
    """a pattern with optional words, as the plain patterns it stands for: "are you [still] there" is "are you there"
    and "are you still there". An optional word means that word or nothing, never any word (a window would let
    "are you from there" through). At most `limit` variants (three optional words)."""
    toks = pattern.split()
    variants = [[]]
    for t in toks:
        opt = t.startswith("[") and t.endswith("]")
        body = t[1:-1] if opt else t
        alts = body.split("|")
        seq = lambda a: "_" in a and not a.startswith(("@", "{", "#", "!", "^", "$"))   # noqa: E731 (class names keep their _)
        if any(seq(a) for a in alts):                # a|b_c: one of several word sequences ("vacation|a_trip")
            choices = [a.split("_") if seq(a) else [a] for a in alts]
        else:
            choices = [[body]]
        if opt:
            choices = [[]] + choices
        variants = [v + c for v in variants for c in choices]
    if len(variants) > limit * 2:
        raise ValueError(f"too many optional words or sequences in '{pattern}'")
    return [" ".join(v) for v in variants if any(not x.startswith(("!", "^", "$", "*")) for x in v)]


INTENTS = {}


def intent(name, patterns, why, yes=(), no=(), weight=1.0, unless=()):
    """an utterance unit U:<name> that fires when any of its patterns does (an OR); `yes` and `no` are test
    sentences that must and must not fire it; `unless` lists other intents (or F: features) that block it, so
    'how are you a bot' is an accusation and not a 'how are you'"""
    if name in INTENTS:
        raise ValueError(f"intent {name} is declared twice")
    _unit("U", name, why)
    slots, dets = {}, []
    for i, p in enumerate(patterns):
        for j, v in enumerate(expand(p)):
            d, slot = compile_pattern(f"{name}.{i}" + (f".{j}" if j else ""), v, why)
            _e(f"LINK U {name} D:{d} {weight:g}", f"'{v}' is one way of saying: {why}")
            dets.append(d)
            if slot:
                slots.setdefault(slot, []).append(d)
    INTENTS[name] = {"patterns": list(patterns), "dets": dets, "slots": slots, "unless": list(unless), "why": why}
    for s in yes:
        DECL["tests"].append(("U:" + name, s, True))
    for s in no:
        DECL["tests"].append(("U:" + name, s, False))


def unit(name, links, why, bias=0.0):
    """a U unit built from other units or features: links {src: weight}"""
    _unit("U", name, why)
    for src, w in links.items():
        _e(f"LINK U {name} {src} {w:g}", why)
    if bias:
        _e(f"BIAS U {name} {bias:g}", why)


def meta_units():
    """units over all intents, declared after every content module: `understood` (any intent fired) and `strange`
    (mostly unknown words and nothing understood: gibberish or something odd)"""
    for name, it in INTENTS.items():
        block = -(len(it["dets"]) + 1)          # enough to silence the intent even if every one of its detectors fires
        for other in it["unless"]:
            if other.startswith("F:"):
                _e(f"LINK U {name} {other} {block}", f"{name} is blocked by {other}: {it['why']} is not meant then")
                continue
            for d in INTENTS[other]["dets"]:
                _e(f"LINK U {name} D:{d} {block}", f"{name} is blocked when the message is {INTENTS[other]['why']}")
    unit("understood", {f"U:{n}": 1.0 for n in INTENTS}, "some intent fired: Helmus understood the message")
    unit("strange", {"S:any": 1.0, "S:unknown_share": 1.0, "U:understood": -2.0}, "nothing understood and most words "
         "unknown: a keyboard smash or something odd", bias=-1.0)


def topic(name, classes, why):
    """a topic unit: any word of these classes in the message"""
    unit("topic_" + name, {"F:c:" + c: 1.0 for c in classes.split()}, why)


def register(name, intent_name, slot, why, phrase=False):
    """copy the word at `slot` of `intent_name`'s patterns into register `name` when the intent fires. A phrase
    register copies the phrase the grammar finds there instead ("doing laundry", not "doing"), seen from the other
    side ("my job" -> "your job"), and its main word as {name.head}"""
    for d in INTENTS[intent_name]["slots"].get(slot, []):
        _e(f"REG {name} {d} U:{intent_name}" + (" phrase" if phrase else ""), why)


def register_when(name, intent_name, slot, gate, why, phrase=False):
    """as register, but copied when `gate` is on (a memory: "Helmus just asked where the user is from"), so a bare
    answer ("mozambique") is read in the light of the question"""
    for d in INTENTS[intent_name]["slots"].get(slot, []):
        _e(f"REG {name} {d} {gate}" + (" phrase" if phrase else ""), why)


def check(name, reg, facts, why):
    """a claim about the persona, checked against its life: when `reg` is copied this turn, C:<name> is on if the
    copied phrase agrees with the persona facts `facts` (a word of it is in them), C:<name>_no if it does not
    ("you said you were from texas": no, ohio)"""
    _e(f"CHECK {name} {reg} {','.join(facts.split())}", why)


def check_stop(words, why):
    """words that say nothing in a claim ("a", "the", "around here"): left out when a claim is checked"""
    _e("CHECKSTOP " + " ".join(words.split()), why)


# ---- memory ---------------------------------------------------------------------------------------------------------
def mem(name, links, why, decay=1.0, bias=0.0):
    """a memory unit carried between turns: m = clip(decay * m_prev + sum(w * src) + bias); a src may be a U: or S:
    unit of this message, M: (last turn's memory) or E:<entry> (an entry Helmus said last turn)"""
    _unit("M", name, why)
    _e(f"DECAY {name} {decay:g}", f"{name}: {'kept' if decay == 1 else 'fades by ' + format(1 - decay, 'g')} from turn to turn")
    for src, w in links.items():
        _e(f"LINK M {name} {src} {w:g}", why)
    if bias:
        _e(f"BIAS M {name} {bias:g}", why)


# ---- phrasebook -------------------------------------------------------------------------------------------------------
def say(eid, head, when, texts, why, bias=None, group=None):
    """a phrasebook entry: `when` {src: weight} is its key; the bias defaults to -(sum of positive weights) + 0.5,
    so it fires (score 0.5) when all its positive sources are fully on. head: react | answer | ask | fallback"""
    if head not in ("react", "answer", "ask", "fallback"):
        raise ValueError(head)
    if any(e["id"] == eid for e in DECL["book"]):
        raise ValueError(f"duplicate entry {eid}")
    texts = [texts] if isinstance(texts, str) else list(texts)
    for t in texts:
        if t != t.strip() or (t.endswith(".") and not t.endswith("..")):
            raise ValueError(f"{eid}: no surrounding spaces, no final full stop: {t!r}")
    if bias is None:
        bias = -sum(w for w in when.values() if w > 0) + 0.5
    _e(f"BIAS K {eid} {bias:g}", f"{eid}: {why}")
    for src, w in when.items():
        _e(f"LINK K {eid} {src} {w:g}", f"{eid}: {why}")
    DECL["book"].append({"id": eid, "head": head, "texts": texts, "group": group})


def more_of(eid, why, score=0.95):
    """asked for another one ("anything else?") right after `eid`: the same entry again, its next unsaid line (the
    entry is a list of separate things, as "say something only a human would know" is)"""
    src = next(e for e in DECL["book"] if e["id"] == eid)
    say(eid + ".more", src["head"], {"U:ask_another": 1, "E:" + eid: 1, "E:" + eid + ".more": 1}, src["texts"],
        f"another one, after {eid}: {why}", bias=round(score - 2, 3), group=src.get("group"))


def rate(name, value, why):
    _e(f"RATE {name} {value:g}", why)


def persona(table):
    DECL["persona"] = table


def facts(table, why):
    """more facts about the persona, declared next to the phrasebook lines that use them; a fact already in the table
    must keep its value (one life, one story)"""
    if not why:
        raise ValueError("facts need a reason")
    F = DECL["persona"]["facts"]
    for k, v in table.items():
        if k in F and F[k] != v:
            raise ValueError(f"fact {k} is already '{F[k]}', not '{v}'")
        F[k] = v


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


# ---- grammar ----------------------------------------------------------------------------------------------------------
# A weighted context-free grammar over word tags (gen/grammar/). Costs are in thousandths, never above zero: the
# parser keeps the cheapest analysis (the highest total), so a cost says how much less likely a reading is.
GRAMMAR = {"tags": {}, "rules": [], "cats": {}, "lhs": set(), "rhs": set(), "literals": set(), "lemmas": {}}


def _milli(cost):
    c = int(round(cost * 1000))
    if c > 0:
        raise ValueError(f"a cost is never above zero: {cost}")
    return c


def tag(name, words, why, cost=0.0):
    """every word in `words` can be a `name` (a word tag: N, V, Det...), at `cost`. Special words: <unk> (a word
    with no tag), <num> (a number in figures), <sym> (an emoji or other sign), <any> (every word)"""
    ws = words.split() if isinstance(words, str) else list(words)
    c = _milli(cost)
    new = []
    for w in ws:
        k = (w, name)
        if k in GRAMMAR["tags"]:
            continue
        GRAMMAR["tags"][k] = c
        new.append(w)
    for i in range(0, len(new), 400):
        _e(f"TAG {name} {c} " + " ".join(new[i:i + 400]), why)


def lemma(base, forms, why):
    """the forms of a verb read as its base: G:verb_<base>"""
    fs = [f for f in sorted(set(forms)) if f != base and f not in GRAMMAR["lemmas"]]
    for f in fs:
        GRAMMAR["lemmas"][f] = base
    if fs:
        _e(f"LEMMA {base} " + " ".join(fs), why)


def _variants(tokens):
    """optional parts "(X)" as the variants with and without them"""
    out = [[]]
    for t in tokens:
        if t.startswith("(") and t.endswith(")"):
            out = [v + x for v in out for x in ([], [t[1:-1]])]
        else:
            out = [v + [t] for v in out]
    return [v for v in out if v]


def rule(spec, why, cost=0.0):
    """a grammar rule "A -> B C^ D:role": `^` marks the head (the child that gives the phrase its main word, the
    first child if none is marked), `:role` names a child's role (subj, obj, neg, past...), 'word' is that word
    itself, (X) is optional. Rules with more than two children are binarised into hidden parts (_A.n)."""
    lhs, _, rhs = spec.partition("->")
    lhs = lhs.strip()
    if not rhs.strip():
        raise ValueError(f"rule needs children: {spec}")
    for alt in rhs.split(" | "):
        for toks in _variants(alt.split()):
            kids = []
            for t in toks:
                head = t.endswith("^") or "^:" in t
                t = t.replace("^", "")
                sym, _, role = t.partition(":")
                if sym.startswith("'"):
                    GRAMMAR["literals"].add(sym)
                kids.append((sym, role or "-", head))
            h = next((i for i, k in enumerate(kids) if k[2]), 0)
            _binarise(lhs, kids, h, _milli(cost), why)


def _binarise(lhs, kids, h, cost, why):
    GRAMMAR["lhs"].add(lhs)
    if len(kids) <= 2:
        GRAMMAR["rhs"].update(k[0] for k in kids)
        n = len(GRAMMAR["rules"])
        GRAMMAR["rules"].append((lhs, kids, h, cost))
        _e(f"RULE {lhs} {' '.join(k[0] for k in kids)} {cost} {h} {' '.join(k[1] for k in kids)}", why)
        return n
    rest = f"_{lhs}.{len(GRAMMAR['rules'])}"
    first, others = kids[0], kids[1:]
    _binarise(rest, others, max(h - 1, 0), 0, why + " (a part of the rule)")
    return _binarise(lhs, [first, (rest, "-", False)], 0 if h == 0 else 1, cost, why)


def gcat(kind, cats, why):
    """what a category is for the network: phrase (a register may copy it; g:<cat> at its first word), clause (its
    roles give the G: features of the message), hidden (spliced out of the tree shown on the page)"""
    for c in cats.split():
        GRAMMAR["cats"][c] = kind
        _e(f"GCAT {c} {kind}", why)


def reflect(table, why):
    """how a copied phrase reads from the other side: "my" -> "your". `you` reads "i" as a subject and "me" after it"""
    for a, b in table.items():
        _e(f"REFLECT {a} {b}", why)
