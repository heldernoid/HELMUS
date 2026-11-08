"""Topics from the vocabulary's themes. The hand-written vocabulary (gen/vocabulary/) is grouped in themed blocks, each
under a comment line ("# fruit, vegetables, nuts, herbs and spices"). This module maps those themes, by hand, to the
topics a reply can be about, and gives every word of a mapped block (with its forms) the class c:t_<topic>; the topic
units U:theme_<topic> then fire on any of them (broader than the narrow topic_ units of
core, which older entries were written against). So "what kind of soup do you make" is about food without a pattern
that names soup.

The mapping below is the only decision here: (vocabulary file, a phrase of the block's comment) -> topic.
"""
import ast
import os

from gen import vocab
from gen.dsl import cls, unit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAP = {
    "food": [("nouns", "the kitchen"), ("nouns", "meals and cooking"), ("nouns", "bread, baking"), ("nouns", "main foods"),
             ("nouns", "fruit, vegetables"), ("nouns", "drinks"), ("verbs", "cooking and the kitchen"),
             ("verbs", "eating, drinking"), ("describing", "taste and smell"), ("describing", "food and drink")],
    # (the chat block of stores, restaurants and brands mixes food with clothes and shops: left out)
    "home": [("nouns", "the house and its rooms"), ("nouns", "furniture"), ("nouns", "things around the house"),
             ("verbs", "home, chores")],
    "clothes": [("nouns", "clothes and accessories")],
    "health": [("nouns", "the body"), ("nouns", "health and medicine"), ("verbs", "health, the doctor"),
               ("describing", "body and health")],
    "family": [("nouns", "family and relationships"), ("verbs", "people and relationships"),
               ("describing", "people and relationships")],
    "work": [("nouns", "jobs and professions"), ("nouns", "work and the office"), ("verbs", "work, jobs")],
    "school": [("nouns", "school and studying"), ("verbs", "school, studying")],
    "money": [("nouns", "money, banking"), ("verbs", "money and shopping"), ("describing", "money, price")],
    "travel": [("nouns", "transport and travel"), ("verbs", "moving around, travel"), ("chat", "cars and vehicles")],
    # (place names stay out of the themes: some intents capture an unknown word as a place, and a themed word is known)
    "nature": [("nouns", "nature, land and water"), ("nouns", "plants and trees"), ("verbs", "nature, weather, animals")],
    "weather": [("nouns", "weather and the sky"), ("describing", "weather and temperature")],
    "science": [("nouns", "space and science"), ("verbs", "science, numbers")],
    "pets": [("nouns", "animals")],
    "sports": [("nouns", "sports and exercise"), ("verbs", "sports, fitness"), ("chat", "sports leagues")],
    "games": [("nouns", "games, toys and hobbies"), ("chat", "games")],
    "tech": [("nouns", "phones, computers"), ("verbs", "phones, computers"), ("chat", "apps and platforms"),
             ("chat", "tech companies")],
    "media": [("nouns", "media, entertainment"), ("verbs", "art, music, making things")],
    "feelings": [("nouns", "feelings and the mind"), ("verbs", "feelings and attitudes"), ("describing", "feelings and moods"),
                 ("describing", "-ed adjectives: feelings")],
    "politics": [("nouns", "society, law, crime and politics"), ("verbs", "law, government")],
    "holidays": [("chat", "holidays and days")],
    "religion": [("chat", "religions and culture")],
    "town": [("nouns", "places in a town")],
}

# words that sit in a themed block but, in chat, usually mean something else ("can you", "watch out", "my plans")
NOT = {
    "food": "can cans canned canning nurse coat scarf",
    "clothes": "watch watches watched watching suit suits",
    "work": "plans plan planned planning own owns owned",
    "money": "fine fines change changes changed changing check checks",
    "family": "human humans bro bros guy guys dude dudes",
    "health": "hair eyes eye test tests",
    "nature": "world rain",
    "school": "word words letter letters trip trips plans study",
    "home": "study",
    "pets": "pet pets",
}

# words too common to mark a topic on their own (they sit in a themed block but say nothing about the subject)
STOP = set("make get go have take give put keep let set run turn come see look use do say tell work play show find "
           "need want like love feel think know call try leave start stop help move live open close end bit part thing "
           "way side top back home place time day night week year house room water food stuff lot kind type".split())


def blocks(name):
    """(comment, words) for each call in a vocabulary file: the words of the call, under the comment just above it"""
    path = os.path.join(ROOT, "gen", "vocabulary", name + ".py")
    src = open(path).read()
    lines = src.splitlines()
    out = []
    for node in ast.parse(src).body:
        if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)):
            continue
        comment = ""
        i = node.lineno - 2
        while i >= 0 and lines[i].startswith("#"):
            text = lines[i].lstrip("#").strip()
            if set(text) - set("-= ") and not text.startswith("("):     # not a rule line, not a section number
                comment = text
                break
            i -= 1
        words = []
        for arg in node.value.args:
            v = ast.literal_eval(arg)
            if isinstance(v, str):
                words += v.split()
            elif isinstance(v, dict):
                for k, f in v.items():
                    words += [k] + f.split()
        out.append((comment.lower(), node.value.func.id, words))
    return out


def build():
    files = {f: blocks(f) for f in ("nouns", "verbs", "describing", "chat")}
    for t, refs in MAP.items():
        words = set()
        for f, phrase in refs:
            hit = [b for b in files[f] if phrase in b[0]]
            if not hit:
                raise ValueError(f"no block '{phrase}' in gen/vocabulary/{f}.py")
            for _, kind, ws in hit:
                for w in ws:
                    if w in STOP or len(w) < 3:
                        continue
                    forms = {"nouns": vocab.noun_forms, "verbs": vocab.verb_forms, "adjectives": vocab.adj_forms}.get(kind)
                    words |= forms(w) if forms else {w}
        words -= set(NOT.get(t, "").split())
        cls("t_" + t, sorted(words), f"a word of the vocabulary's '{t}' themes, so a message about it is about {t}")
        unit("theme_" + t, {"F:c:t_" + t: 1.0}, f"the message is about {t} (any word of its vocabulary themes)")
