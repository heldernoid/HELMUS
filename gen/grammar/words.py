"""Word tags for the grammar: what each word can be (a noun, a past-tense verb, a determiner...). Shared by every
persona: this is English, not Josh.

Most tags come from the hand-written vocabulary (gen/vocabulary/), read block by block: the rules that make its forms
also say what each form is (walk -> walks is third person, walked past or participle, walking -ing; cat -> cats
plural; big -> bigger comparative, biggest superlative, bigly an adverb). The closed classes (pronouns, determiners,
auxiliaries, prepositions, conjunctions, question words) are listed here by hand, as are the costs of the rarer readings
of very common words ("like" is a verb, a preposition and a filler).

Tags:
  N Ns Np PossN           noun, plural noun, proper name, possessive (brother's)
  Pr1 Pr2 PrS PrIt PrO PrRefl PrPoss PrInd     i, you, he/she/we/they, it, me/him/us/them, myself, mine, someone
  Det Dem Poss Q Num Ord  a/the, this/that, my/your, some/every/many, numbers, first/last
  Adj AdjC AdjS           big, bigger, biggest
  Adv AdvDeg AdvT AdvF AdvNeg                  adverbs: plain, degree (very), time (today), frequency (often), never
  V Vz Vd Vn Vg           verb: base, third person, past, participle, -ing
  BeP BeD Be Been Being   am/is/are, was/were, be, been, being
  Hv Hz Hd Do Dz Dd Md    have, has, had, do, does, did, the modals (can, will, would...)
  Neg To P Part           not, to, prepositions, particles (up, out, off...)
  Cc Sub Comp             and/or/but, because/if/when..., that
  WhN WhD WhA             what/who, which/whose, where/when/why/how
  Ex Ij Dm Let Pls Ampm Than X                 there (is), interjections, fillers (like, well), let, please, am/pm, than,
                                               anything (the last resort: a word read as nothing in particular)
"""
import ast
import os

from gen import vocab
from gen.dsl import lemma, tag

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def calls(name):
    """(comment, function, argument) for each call in a vocabulary file, the argument as written (a string or a
    table), under the comment just above it"""
    path = os.path.join(ROOT, "gen", "vocabulary", name + ".py")
    src = open(path).read()
    lines = src.splitlines()
    out = []
    for node in ast.parse(src).body:
        if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)):
            continue
        comment, i = "", node.lineno - 2
        while i >= 0 and lines[i].startswith("#"):
            text = lines[i].lstrip("#").strip()
            if set(text) - set("-= ") and not text.startswith("("):
                comment = text
                break
            i -= 1
        out.append((comment.lower(), node.value.func.id, ast.literal_eval(node.value.args[0])))
    return out


# ---- the closed classes, by hand ----------------------------------------------------------------------------------
CLOSED = {
    "Pr1": "i",
    "Pr2": "you",
    "PrS": "he she we they",
    "PrIt": "it",
    "PrO": "me him her us them em",
    "PrRefl": "myself yourself himself herself itself ourselves yourselves themselves oneself themself ourself",
    "PrPoss": "mine yours his hers ours theirs",
    "PrInd": "someone somebody something anyone anybody anything everyone everybody everything nobody nothing none "
             "noone one whatever whoever",
    "Det": "a an the",
    "Dem": "this that these those",
    "Poss": "my your his her our their its thy",
    "Q": "some any no every each all both either neither many much few several enough lots plenty more most less "
         "least another other half such",
    "Ord": "first second third fourth fifth sixth seventh eighth ninth tenth last next final",
    "BeP": "am is are",
    "BeD": "was were",
    "Be": "be",
    "Been": "been",
    "Being": "being",
    "Hv": "have",
    "Hz": "has",
    "Hd": "had",
    "Do": "do",
    "Dz": "does",
    "Dd": "did",
    "Md": "can could will would shall should may might must ought",
    "Neg": "not",
    "To": "to",
    "P": "about above across after against along alongside amid among around as at before behind below beneath "
         "beside besides between beyond by despite during except for from in inside into like near of off on onto "
         "out outside over past per since through throughout till until to toward towards under underneath unlike "
         "up upon via with within without plus minus versus vs",
    "Part": "up down out off in on over away back around through along ahead apart aside together about",
    "Cc": "and or but nor plus",
    "Sub": "because cause if when whenever while although though unless until till since whether once as before "
           "after so whereas wherever",
    "Comp": "that",
    "WhN": "what who whom which",
    "WhD": "which whose what",
    "WhA": "where when why how",
    "Ex": "there",
    "Dm": "like well so anyway anyways actually basically literally honestly seriously though tho btw also then wait",
    "Adj": "awake asleep alive alone afraid aware ready alright",
    "Let": "let",
    "Pls": "please",
    "Ampm": "am pm",
    "Than": "than",
    "AdvDeg": "very so really pretty too quite rather super extremely totally lowkey highkey hella way kinda sorta "
              "incredibly insanely absolutely completely fully truly real mad",
    "AdvT": "now today tonight tomorrow yesterday later soon then already yet still again ago lately recently earlier "
            "sooner tmrw tmr tonite currently anymore",
    "AdvF": "always often sometimes usually rarely ever constantly normally generally occasionally seldom hardly "
            "barely mostly",
    "AdvNeg": "never",
    "Ntime": "day days night nights week weeks weekend weekends month months year years morning mornings afternoon "
             "afternoons evening evenings time times summer winter spring fall hour hours minute minutes moment while "
             "semester season decade",
}
# readings of closed-class words that are rarer, at a cost (a word may have several)
COSTS = {
    ("Sub", "so"): -0.3, ("Sub", "as"): -0.3, ("Sub", "once"): -0.4, ("Sub", "before"): -0.2, ("Sub", "after"): -0.2,
    ("Sub", "since"): -0.2, ("Sub", "till"): -0.2, ("Sub", "cause"): -0.2, ("Dm", "like"): -0.6, ("Dm", "so"): -0.3,
    ("Dm", "well"): -0.2, ("Dm", "then"): -0.4, ("Dm", "also"): -0.5, ("Dm", "though"): -0.1, ("P", "like"): -0.1,
    ("Part", "about"): -0.5, ("Part", "through"): -0.4, ("Part", "along"): -0.3, ("Part", "in"): -0.25,
    ("Part", "on"): -0.25, ("P", "as"): -0.2, ("Cc", "plus"): -0.3, ("Q", "half"): -0.3, ("Q", "such"): -0.3,
    ("Ord", "next"): -0.1, ("Ord", "last"): -0.1, ("AdvDeg", "real"): -0.4, ("AdvDeg", "mad"): -0.5,
    ("AdvDeg", "way"): -0.4, ("AdvDeg", "pretty"): -0.1, ("PrO", "her"): -0.05, ("Poss", "his"): 0,
    ("WhN", "which"): -0.1, ("PrInd", "one"): -0.3, ("Md", "ought"): -0.3, ("Ampm", "am"): -0.4, ("WhD", "what"): -0.05, ("Dm", "wait"): -0.2,
    ("AdvT", "then"): -0.1, ("AdvT", "still"): -0.05, ("PrPoss", "his"): -0.3, ("Q", "more"): -0.05,
}
# readings the vocabulary gives that are wrong or rare for these words in chat (removed, or kept at a cost)
OPEN_COSTS = {"Np": -0.35}                              # a common word that is also a name ("will", "may") is a name rarely
DROP = {("can", "N"), ("will", "N"), ("may", "Np"), ("us", "Np"), ("it", "Np"), ("am", "Np"), ("so", "Adj"),
        ("not", "Ij"), ("can", "V"), ("will", "V"), ("must", "V"), ("might", "N"), ("never", "AdvT"),
        ("always", "AdvT"), ("often", "AdvT"), ("sometimes", "AdvT"), ("ever", "AdvT"), ("usually", "AdvT")}
EXTRA = {
    # words of the closed classes that are also open-class words, with the costs of those readings
    "Adj": ("well -0.3 right 0 okay 0 fine 0 sure 0 good 0 same -0.1 done -0.2 own -0.2 other -0.2 only -0.3 "
            "real 0 cool 0 alright 0 down -0.4 up -0.6 out -0.6 back -0.6 over -0.5"),
    "Adv": ("just 0 only 0 even 0 also 0 too -0.1 here 0 there -0.1 home -0.2 back -0.1 away 0 out -0.3 up -0.4 "
            "down -0.4 off -0.4 around -0.2 almost 0 maybe 0 probably 0 definitely 0 though -0.2 else 0 right -0.2 "
            "well -0.2 together 0 alone 0 instead 0 anyway -0.1 more -0.2 less -0.2 enough -0.2 all -0.4 much -0.1 "
            "kind -0.9 sort -0.9 like -0.8 now 0 then -0.1 first -0.2 last -0.4 once -0.2 twice 0 forever 0 soon 0 "
            "better 0 best -0.2 most -0.3 least -0.3 longer 0 harder 0 faster 0 earlier 0 later 0"),
    "N": "kind -0.1 sort -0.2 lot 0 bit 0 thing 0 way 0 time 0 home 0 right -0.6 well -0.7 back -0.5 today -0.2 "
         "tonight -0.2 tomorrow -0.2 yesterday -0.2 weekend 0 like -0.9 work 0 one -0.3 couple 0 pair 0 dozen 0",
    "V": "like 0 well -0.9 back -0.8 mind 0 mean 0 bet -0.1 guess 0 hope 0 need 0 dare -0.3 used -0.2",
    "Ij": "yes 0 no 0 okay 0 ok 0 sure 0 right -0.2 well -0.2 like -0.9 please -0.1 thanks 0 thank -0.6 sorry 0 "
          "bye 0 hi 0 hello 0 hey 0 lol 0 haha 0 hehe 0 same -0.2 true -0.2 nice -0.3 cool -0.3 damn 0 dang 0 god -0.4 "
          "bruh 0 bro -0.2 dude -0.2 man -0.4 yo 0 wow 0 omg 0 lmao 0 welp 0 alright -0.1 fair -0.3 facts -0.3 "
          "word -0.6 bet -0.4 nope 0 yep 0 yeah 0 nah 0 mhm 0 hmm 0 um 0 uh 0 oh 0 ah 0 ugh 0 yay 0 oops 0 xd 0",
    "Num": "one 0",
    "Vd": "used -0.2",
}


def third(v):
    """the third person by the rule of gen/vocab.py's verb_forms"""
    if v.endswith(("s", "x", "z", "ch", "sh", "o")):
        return v + "es"
    if v.endswith("y") and len(v) > 1 and v[-2] not in vocab.VOWELS:
        return v[:-1] + "ies"
    return v + "s"


def build():
    """tag every word: the closed classes, then the vocabulary by its blocks"""
    seen, pending = {}, {}
    pasts_of_others = set()

    def add(t, ws, why, cost=0.0):
        """collected, then written one line per tag, cost and reason (a vocabulary block is one reason)"""
        ws = [w for w in (ws.split() if isinstance(ws, str) else ws) if (w, t) not in DROP]
        pending.setdefault((t, cost, why), []).extend(ws)
        for w in ws:
            seen.setdefault(w, set()).add(t)

    for t, ws in CLOSED.items():
        plain = [w for w in ws.split() if (t, w) not in COSTS]
        add(t, plain, f"a closed-class word: {t}")
        for w in ws.split():
            if (t, w) in COSTS:
                add(t, [w], f"a rarer reading of a closed-class word as {t}", COSTS[t, w])
    for t, spec in EXTRA.items():
        p = spec.split()
        for w, c in zip(p[::2], p[1::2]):
            add(t, [w], f"a common word that can also be {t}", float(c))

    # ---- verbs: the forms by their rules, the irregular ones from their tables (third person, past, participle, -ing)
    skip = {"be", "have", "do"}
    for comment, fn, arg in calls("verbs"):
        if fn == "verbs":
            for v in arg.split():
                if v in skip:
                    continue
                f = vocab.verb_forms(v)
                z = [third(v)]
                ing = [x for x in f if x.endswith("ing") and x not in (v, z[0])]
                ed = [x for x in f if x not in ing and x not in z and x != v]
                add("V", [v], f"a verb ({comment})")
                add("Vz", z, f"third person of a verb ({comment}): by the spelling rule")
                add("Vd", ed, f"past of a verb ({comment}): by the spelling rule")
                add("Vn", ed, f"participle of a verb ({comment}): by the spelling rule")
                add("Vg", ing, f"-ing form of a verb ({comment}): by the spelling rule")
                lemma(v, f, "forms of a verb, by the spelling rules")
        elif fn == "irregular_verbs":
            for v, forms in arg.items():
                if v in skip:
                    continue
                fs = forms.split()
                ing = [x for x in fs if x.endswith("ing")]
                rest = [x for x in fs if x not in ing]
                z, mid = rest[:1], rest[1:]
                add("V", [v], "an irregular verb (its forms are listed in its table)")
                add("Vz", z, "third person of an irregular verb (from its table)")
                add("Vg", ing, "-ing form of an irregular verb (from its table)")
                pasts_of_others.update(x for x in mid if x != v)
                if len(mid) == 2 and mid[0] != mid[1]:      # went gone: past, then participle
                    add("Vd", [mid[0]], "past of an irregular verb (from its table)")
                    add("Vn", [mid[0]], "the past of an irregular verb, as a participle: rarer", -0.3)
                    add("Vn", [mid[1]], "participle of an irregular verb (from its table)")
                    add("Vd", [mid[1]], "the participle of an irregular verb, as a past: rarer", -0.3)
                else:                                       # said: past and participle alike
                    add("Vd", mid, "past of an irregular verb (from its table)")
                    add("Vn", mid, "participle of an irregular verb (from its table)")
                lemma(v, fs, "forms of an irregular verb, from its table")
    for v in ("have", "do"):                                # as main verbs ("i have a cat", "i do homework")
        f = {"have": ("have", "has", "had", "having"), "do": ("do", "does", "did", "doing")}[v]
        add("V", [f[0]], f"'{v}' as a main verb")
        add("Vz", [f[1]], f"'{v}' as a main verb")
        add("Vd", [f[2]], f"'{v}' as a main verb")
        add("Vn", [{"have": "had", "do": "done"}[v]], f"'{v}' as a main verb")
        add("Vg", [f[3]], f"'{v}' as a main verb")
        lemma(v, list(f) + ["done"] if v == "do" else list(f), f"forms of '{v}'")
    lemma("be", ["am", "is", "are", "was", "were", "been", "being"], "forms of 'be'")

    # ---- nouns
    for comment, fn, arg in calls("nouns"):
        if fn == "nouns":
            for n in arg.split():
                pl = [x for x in vocab.noun_forms(n) if x != n]
                t = "Np" if "months" in comment else "N"
                add(t, [n], f"a noun ({comment})")
                add("Ns", pl, f"plural of a noun ({comment}): by the spelling rule")
        elif fn == "irregular_nouns":
            for n, pl in arg.items():
                add("N", [n], "a noun with an irregular plural")
                add("Ns", pl.split(), "an irregular plural (from its table)")
        elif fn == "words":
            for w in arg.split():
                plural = w.endswith("s") and not w.endswith(("ss", "us", "is"))
                add("Np" if "months" in comment else ("Ns" if plural else "N"), [w],
                    f"a noun as it is written ({comment})")

    # ---- describing words, by zone: adjectives, adverbs, function words (by hand above), numbers, interjections
    zone = "adj"
    for comment, fn, arg in calls("describing"):
        if comment.startswith("time and frequency"):
            zone = "adv"
        elif comment.startswith("personal pronouns"):
            zone = "function"
        elif comment.startswith("cardinal numbers"):
            zone = "num"
        elif comment.startswith("ordinals"):
            zone = "ord"
        elif comment.startswith(("days of the week", "months")):
            zone = "day"
        elif comment.startswith("seasons"):
            zone = "season"
        elif comment == "" and fn == "words" and zone == "season":
            zone = "ij"
        ws = arg.split()
        if zone == "adj" and fn == "adjectives":
            for a in ws:
                for f in vocab.adj_forms(a):
                    if f == a:
                        add("Adj", [f], f"an adjective ({comment})")
                    elif f.endswith("est"):
                        add("AdjS", [f], f"superlative of an adjective ({comment}): by the spelling rule")
                    elif f.endswith("er"):
                        add("AdjC", [f], f"comparative of an adjective ({comment}): by the spelling rule")
                    elif f.endswith("ly"):
                        add("Adv", [f], f"adverb of an adjective ({comment}): by the spelling rule")
        elif zone == "adj":
            group = set(ws)
            for w in ws:
                if w in ("better", "worse", "more", "less", "further", "farther", "elder"):
                    add("AdjC", [w], "a comparative")
                elif w in ("best", "worst", "most", "least", "furthest", "farthest", "eldest"):
                    add("AdjS", [w], "a superlative")
                elif w.endswith("est") and (w[:-3] in group or w[:-2] in group or w[:-3] + "y" in group):
                    add("AdjS", [w], "a superlative")
                elif w.endswith("er") and (w[:-2] in group or w[:-1] in group or w[:-3] + "y" in group):
                    add("AdjC", [w], "a comparative")
                elif w.endswith("ly") and "end in -ly" not in comment:
                    add("Adv", [w], f"an adverb ({comment})")
                    if w[:-2] not in group and w[:-3] + "y" not in group:
                        add("Adj", [w], f"'{w}' can be an adjective", -0.5)
                else:
                    add("Adj", [w], f"an adjective ({comment})")
        elif zone == "adv":
            t = {"degree and amount": "AdvDeg"}.get(comment, "Adv")
            if comment.startswith("time and frequency"):
                t = "AdvT"
                ws = [w for w in ws if w not in CLOSED["AdvF"].split() and w != "never"]
            add(t, ws, f"an adverb ({comment})")
        elif zone == "num":
            add("Num", ws, "a number word")
        elif zone == "ord":
            add("Ord", [w for w in ws if w not in ("halves", "quarter", "quarters", "couple", "pair", "pairs")],
                "an ordinal or a fraction")
            add("N", ["quarter", "couple", "pair"], "a fraction or an amount, as a noun")
            add("Ns", ["halves", "quarters", "pairs"], "a fraction or an amount, as a noun")
        elif zone == "day":
            add("Np", [w for w in ws if not w.startswith("week")], f"a day or month name ({comment})")
            add("N", [w for w in ws if w.startswith("week") and not w.endswith("s")], "a word for days")
            add("Ns", [w for w in ws if w.startswith("week") and w.endswith("s")], "a word for days")
        elif zone == "season":
            add("N", [w for w in ws if w not in ("pm", "autumnal", "wintry", "wintery", "summery")], "a season or time of day")
            add("Adj", ["autumnal", "wintry", "wintery", "summery"], "an adjective of a season")
        elif zone == "ij":
            add("Ij", ws, "an interjection")

    # ---- chat words: slang, interjections, names, places, brands
    for comment, fn, arg in calls("chat"):
        ws = arg.split()
        if any(k in comment for k in ("laughing", "interjections", "emoticon", "chat abbreviations")):
            add("Ij", ws, f"chat ({comment})")
        elif "current slang" in comment:
            add("Ij", ws, f"slang ({comment})", -0.2)
            add("Adj", ws, f"slang, as a describing word ({comment})", -0.3)
            add("N", ws, f"slang, as a noun ({comment})", -0.5)
        elif "nationalities and peoples" in comment:
            for n in ws:
                add("N", [n], "a nationality, as a noun")
                add("Ns", [x for x in vocab.noun_forms(n) if x != n], "plural of a nationality")
                add("Adj", [n], "a nationality, as a describing word", -0.1)
        elif "nationalities and languages" in comment or "religions" in comment:
            add("Adj", ws, f"a describing word ({comment})")
            add("Np", ws, f"a name ({comment})", -0.1)
        else:
            add("Np", ws, f"a name ({comment})", -0.05)

    # ---- what any other word can be: a guess by its ending, then the last resort
    add("Np", ["<unk>"], "a word with no tag: most likely a name", -0.25)
    add("N", ["<unk>"], "a word with no tag: maybe a thing", -0.35)
    add("Adj", ["<unk>"], "a word with no tag: rarely a describing word", -0.9)
    add("V", ["<unk>"], "a word with no tag: rarely a verb", -1.0)
    add("Ij", ["<unk>"], "a word with no tag: rarely an interjection", -1.0)
    add("Vg", ["<unk-ing>"], "an unknown word ending in -ing: an -ing form", -0.3)
    add("Vd", ["<unk-ed>"], "an unknown word ending in -ed: a past", -0.4)
    add("Vn", ["<unk-ed>"], "an unknown word ending in -ed: a participle", -0.5)
    add("Adv", ["<unk-ly>"], "an unknown word ending in -ly: an adverb", -0.4)
    add("Ns", ["<unk-s>"], "an unknown word ending in -s: a plural", -0.4)
    add("Num", ["<num>"], "a number in figures")
    add("Ij", ["<sym>"], "an emoji or other sign: like an interjection", -0.2)
    add("PossN", ["<poss>"], "a known word with 's: a possessive")
    add("X", ["<any>"], "any word, read as nothing in particular: the last resort", -3.0)
    irregular_past = pasts_of_others
    for (t, cost, why), ws in list(pending.items()):
        if t == "V" and cost == 0:
            rare = [w for w in ws if w in irregular_past]
            if rare:
                pending[t, cost, why] = [w for w in ws if w not in irregular_past]
                pending.setdefault(("V", -0.4, "a base verb that is also the past of a common verb (saw, found): "
                                    "the past is likelier"), []).extend(rare)
    time_nouns = set(CLOSED["Ntime"].split())                # day, week: nouns through Nom -> Ntime only
    for (t, cost, why), ws in pending.items():
        if t in ("N", "Ns"):
            ws = [w for w in ws if w not in time_nouns]
        tag(t, ws, why, cost)
    return seen


def pending_words(pending, t, why_part):
    return [w for (tt, _, why), ws in pending.items() if tt == t and why_part in why for w in ws]
