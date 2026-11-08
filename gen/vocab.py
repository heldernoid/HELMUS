"""The vocabulary: the English words Helmus knows to be real, written by hand (gen/vocabulary/*.py), with their forms
made by fixed rules. It is not part of the network's weights; the reader uses it to tell a real word it has no unit
for ("worry") from a misspelling ("wrory"), so only misspellings are corrected, to the nearest real word.

Declare words by kind, so the rules add the right endings:
  verbs("walk talk")              walk walks walked walking (+ regular spelling rules: stop -> stopped, try -> tried)
  irregular_verbs({"go": "goes went gone going"})     forms listed in full
  nouns("cat city")               cat cats, city cities
  irregular_nouns({"child": "children"})
  adjectives("big happy")         big bigger biggest, happy happier happiest happily
  words("the of lol")             as they are (function words, slang, names, places, brands, interjections)
"""
FORMS = set()
BASES = {"verb": set(), "noun": set(), "adj": set(), "word": set()}
VOWELS = "aeiou"


def _cvc(w):
    """consonant-vowel-consonant at the end of a short word: the final consonant doubles (stop -> stopped)"""
    return (len(w) >= 3 and w[-1] not in VOWELS + "wxy" and w[-2] in VOWELS and w[-3] not in VOWELS
            and sum(c in VOWELS for c in w) == 1)


def verb_forms(v):
    if v.endswith("ie"):
        ing, ed = v[:-2] + "ying", v + "d"
    elif v.endswith(("ee", "ye", "oe")):
        ing, ed = v + "ing", v + "d"
    elif v.endswith("e"):
        ing, ed = v[:-1] + "ing", v + "d"
    elif v.endswith("y") and len(v) > 1 and v[-2] not in VOWELS:
        ing, ed = v + "ing", v[:-1] + "ied"
    elif _cvc(v):
        ing, ed = v + v[-1] + "ing", v + v[-1] + "ed"
    else:
        ing, ed = v + "ing", v + "ed"
    if v.endswith(("s", "x", "z", "ch", "sh", "o")):
        s = v + "es"
    elif v.endswith("y") and len(v) > 1 and v[-2] not in VOWELS:
        s = v[:-1] + "ies"
    else:
        s = v + "s"
    return {v, s, ed, ing}


def noun_forms(n):
    if n.endswith(("s", "x", "z", "ch", "sh")):
        p = n + "es"
    elif n.endswith("y") and len(n) > 1 and n[-2] not in VOWELS:
        p = n[:-1] + "ies"
    else:
        p = n + "s"
    if n.endswith("o"):
        return {n, n + "s", n + "es"}             # potatoes, photos: both spellings are real for some words
    return {n, p}


def adj_forms(a):
    out = {a}
    if a.endswith("y") and len(a) > 1 and a[-2] not in VOWELS:
        out |= {a[:-1] + "ier", a[:-1] + "iest", a[:-1] + "ily"}
    elif a.endswith("e"):
        out |= {a + "r", a + "st", a[:-1] + "y" if a.endswith("le") else a + "ly"}
    elif _cvc(a):
        out |= {a + a[-1] + "er", a + a[-1] + "est", a + "ly"}
    else:
        out |= {a + "er", a + "est", a + "ly"}
    return out


def _split(s):
    return [w.strip().lower() for w in s.split() if w.strip()]


def verbs(s):
    for v in _split(s):
        BASES["verb"].add(v)
        FORMS.update(verb_forms(v))


def irregular_verbs(table):
    for v, forms in table.items():
        BASES["verb"].add(v)
        FORMS.add(v)
        FORMS.update(_split(forms))


def nouns(s):
    for n in _split(s):
        BASES["noun"].add(n)
        FORMS.update(noun_forms(n))


def irregular_nouns(table):
    for n, forms in table.items():
        BASES["noun"].add(n)
        FORMS.add(n)
        FORMS.update(_split(forms))


def adjectives(s):
    for a in _split(s):
        BASES["adj"].add(a)
        FORMS.update(adj_forms(a))


def words(s):
    for w in _split(s):
        BASES["word"].add(w)
        FORMS.add(w)
