"""The grammar's verb phrases. Shared by every persona.

A verb phrase is built for each form of the verb, so a clause can ask for the right one:
  VPb  base (like pizza; after do, to, a modal; the present after i/you/we/they)     VPz  third person (likes pizza)
  VPd  past (liked pizza)      VPn  participle (liked by everyone, have liked)      VPg  -ing (liking pizza)
  VPto to and a base phrase (to like pizza)
Each form takes the same complements: an object, two objects, a preposition phrase, a describing phrase, a to-phrase,
an -ing phrase, a clause, a particle (give up, pick it up). Chat English does not say which verbs take which, so all
are allowed and the costs prefer the common ones; the parser's other choices settle the rest.

The same phrases with a gap (VPb/NP...) are the inside of a wh-question: in "what do you like _" the object is the
question word, missing after "like".

Then the verb group of a clause (VPfin): a verb phrase with its auxiliaries, negation, tense and modals, each part
marked with its role (neg, past, fut, modal, perf, prog, pass, do), which the network reads as G: features.
"""
from gen.dsl import rule

FORMS = {"b": "V", "z": "Vz", "d": "Vd", "n": "Vn", "g": "Vg"}

for f, T in FORMS.items():
    P = f"VP{f}"
    G = f"VP{f}/NP"
    what = {"b": "base", "z": "third person", "d": "past", "n": "participle", "g": "-ing"}[f]
    # ---- complements
    rule(f"{P} -> {T}^", f"a {what} verb alone (i sleep, he left)", -0.25 if f == "b" else 0)
    rule(f"{P} -> {T}^ NP:obj", f"a {what} verb and its object (like pizza)")
    rule(f"{P} -> {T}^ NP:obj2 NP:obj", f"a {what} verb and two objects (give me a minute, send me the link)", -0.35)
    rule(f"{P} -> {T}^ PP", f"a {what} verb and a preposition phrase (live in ohio, talk about games)", -0.05)
    rule(f"{P} -> {T}^ NP:obj PP", f"a {what} verb, an object and a preposition phrase (put it on the desk)", -0.05)
    rule(f"{P} -> {T}^ AdjP:attr", f"a {what} verb and a describing phrase (feel tired, look good, get bored)", -0.2)
    rule(f"{P} -> {T}^ NP:obj AdjP:attr", f"a {what} verb, an object and a describing phrase (makes me happy)", -0.45)
    rule(f"{P} -> {T}^ VPto:comp", f"a {what} verb and a to-phrase (want to go, try to sleep)", -0.05)
    rule(f"{P} -> {T}^ NP:obj VPto:comp", f"a {what} verb, an object and a to-phrase (want you to come)", -0.25)
    rule(f"{P} -> {T}^ VPg:obj", f"a {what} verb and an -ing phrase as its object (love playing, hate doing laundry)", -0.1)
    rule(f"{P} -> {T}^ NP:obj VPb:comp", f"a {what} verb, an object and a base phrase (let me know, make me laugh)", -0.3)
    rule(f"{P} -> {T}^ NP:obj VPg:comp", f"a {what} verb, an object and an -ing phrase (saw him playing)", -0.6)
    rule(f"{P} -> {T}^ NP:obj VPn:comp", f"a {what} verb, an object and a participle (got my car fixed)", -0.7)
    rule(f"{P} -> {T}^ Sbar:comp", f"a {what} verb and a clause (think that..., know if..., hope so)", -0.1)
    rule(f"{P} -> {T}^ S:comp", f"a {what} verb and a clause without 'that' (i think you are right)", -0.25)
    rule(f"{P} -> {T}^ WhCl:comp", f"a {what} verb and a wh-clause (know what you mean, wonder why)", -0.1)
    rule(f"{P} -> {T}^ NP:obj Sbar:comp", f"a {what} verb, an object and a clause (told me that...)", -0.35)
    rule(f"{P} -> {T}^ NP:obj WhCl:comp", f"a {what} verb, an object and a wh-clause (tell me what you like)", -0.25)
    rule(f"{P} -> {T}^ NP:obj S:comp", f"a {what} verb, an object and a clause (told me i was wrong)", -0.6)
    rule(f"{P} -> {T}^ Part", f"a {what} verb and a particle (give up, hang out, wake up)", -0.1)
    rule(f"{P} -> {T}^ Part NP:obj", f"a {what} verb, a particle and an object (pick up the phone)", -0.04)
    rule(f"{P} -> {T}^ NP:obj Part", f"a {what} verb, an object and a particle (pick it up)", -0.25)
    rule(f"{P} -> {T}^ Part PP", f"a {what} verb, a particle and a preposition phrase (hang out with friends)", -0.15)
    rule(f"{P} -> {T}^ Part VPg:obj", f"a {what} verb, a particle and an -ing phrase (keep on going)", -0.3)
    rule(f"{P} -> {T}^ AdvP", f"a {what} verb and an adverb it needs (go home, come back, get here)", -0.05)
    rule(f"{P} -> {T}^ NP:obj AdvP", f"a {what} verb, an object and an adverb (bring it back)", -0.2)
    rule(f"{P} -> {T}^ 'like' NP:comp | {T}^ 'like' S:comp | {T}^ 'like' VPg:comp | {T}^ 'as' 'if' S:comp",
         f"a {what} verb and 'like' (looks like rain, feel like going out, feels like i am dying)", -0.2)
    rule(f"{P} -> {T}^ 'it' VPto:comp | {T}^ 'it' Sbar:comp", f"a {what} verb, 'it' and what it stands for "
         "(hate it when..., love it that...)", -0.3)
    # ---- adjuncts: where, when, how, why
    rule(f"{P} -> {P}^ AdvP", "an adverb after the verb phrase (play a lot, sleep late)", -0.08)
    rule(f"{P} -> AdvP {P}^", "an adverb before the verb phrase (just got here, really like it)", -0.08)
    rule(f"{P} -> AdvNeg:neg {P}^", "never before the verb phrase (never played it)")
    rule(f"{P} -> {P}^ PP", "a preposition phrase after the verb phrase (play with my friends)", -0.15)
    rule(f"{P} -> {P}^ NPt", "a time phrase after the verb phrase (play every day, went last week)", -0.1)
    rule(f"{P} -> {P}^ NP", "a noun phrase after the verb phrase, as an adjunct (rare)", -0.9)
    rule(f"{P} -> {P}^ Sbar", "a clause after the verb phrase (stayed home because it rained)", -0.2)
    rule(f"{P} -> {P}^ VPto", "a purpose after the verb phrase (went there to eat)", -0.5)
    rule(f"{P} -> {P}^ VPg", "an -ing phrase after the verb phrase (spent the day gaming)", -0.8)
    rule(f"{P} -> {P}^ Cc {P}:conj", "verb phrases joined (eat and sleep)", -0.15)
    rule(f"{P} -> Dm {P}^", "a filler before the verb phrase (like, literally)", -0.5)
    rule(f"{P} -> {P}^ 'and' 'stuff' | {P}^ 'or' 'something' | {P}^ 'and' 'everything' | {P}^ 'or' 'whatever' | "
         f"{P}^ 'and' 'all' 'that' | {P}^ 'and' 'things' | {P}^ 'lol'", "a vague tail (game and stuff)", -0.05)
    # ---- the same with a gap: the question word is missing from inside the phrase (what do you like _)
    rule(f"{G} -> {T}^", f"a {what} verb whose object is the question word (what do you like)", -0.05)
    rule(f"{G} -> {T}^ NP:obj2", f"a {what} verb whose second object is the question word (what do you call it)", -0.4)
    rule(f"{G} -> {T}^ PP/NP", f"a {what} verb with the question word after its preposition (who are you talking to)", -0.1)
    rule(f"{G} -> {T}^ NP:obj PP/NP", f"a {what} verb, an object, and the question word after a preposition", -0.25)
    rule(f"{G} -> {T}^ VPto/NP:comp", f"a {what} verb and a to-phrase with the gap (what do you want to do)", -0.1)
    rule(f"{G} -> {T}^ NP:obj VPto/NP:comp", f"a {what} verb, an object, a to-phrase with the gap (what do you want "
         "me to say)", -0.35)
    rule(f"{G} -> {T}^ VPg/NP:comp", f"a {what} verb and an -ing phrase with the gap (what do you like doing)", -0.2)
    rule(f"{G} -> {T}^ S/NP:comp", f"a {what} verb and a clause with the gap (what do you think i like)", -0.4)
    rule(f"{G} -> {T}^ Part", f"a {what} verb and a particle, the object being the question word", -0.2)
    rule(f"{G} -> {T}^ 'like'", f"a {what} verb and 'like' with the gap (what does it look like)", -0.1)
    rule(f"{G} -> {G}^ AdvP | {G}^ PP | {G}^ Sbar", "adjuncts after a phrase with a gap (what do you do for fun)", -0.1)
    rule(f"{G} -> {G}^ NPt", "a time phrase after a phrase with a gap (what are you doing tonight)", -0.1)
    rule(f"{G} -> AdvP {G}^ | AdvNeg:neg {G}^", "an adverb before a phrase with a gap (what do you usually eat)", -0.08)

rule("VPto -> To VPb^", "to and a base phrase (to go)")
rule("VPto -> To Be Pred^ | To Hv:perf VPn^ | To Be Neg:neg Pred^", "to be..., to have done")
rule("VPto -> Neg:neg VPto^ | AdvNeg:neg VPto^", "not to go, never to return")
rule("VPto -> VPto^ Cc VPto:conj | VPto^ Cc VPb:conj", "to eat and to sleep, to go and get it", -0.15)
rule("VPto -> To", "'to' alone, the rest understood (i want to)", -0.6)
rule("VPto/NP -> To VPb/NP^ | To Be Pred/NP^", "a to-phrase with the gap")
rule("PP/NP -> P^ | To^", "a preposition whose noun phrase is the question word (where are you from, who to)")
rule("VPbare -> VPb^", "the phrase after a modal (can play)")
rule("VPbare -> Be Pred^ | Be Neg:neg Pred^", "be and a predicate after a modal (will be fine)")
rule("VPbare -> Hv:perf VPn^ | Hv:perf Been Pred^", "have done, have been after a modal (could have won)")
rule("VPbare/NP -> VPb/NP^ | Be Pred/NP^ | Hv:perf VPn/NP^", "the phrase after a modal, with the gap")
rule("VPbare/NP -> Be^", "be, its predicate the gap (what would it be)", -0.05)

# ---- what follows be: the predicate ---------------------------------------------------------------------------------
rule("Pred -> NP^:pred | AdjP^:pred | PP^:pred", "what follows be: a noun phrase, a describing phrase, a place")
rule("Pred -> AdvP^:pred", "what follows be: an adverb (here, home, outside, back)", -0.15)
rule("Pred -> VPg^:prog", "be and an -ing phrase: something going on (i am playing)")
rule("Pred -> VPn^:pass", "be and a participle: something done to it (it was cancelled)", -0.3)
rule("Pred -> VPto^", "be and a to-phrase (the plan is to sleep)", -0.5)
rule("Pred -> 'going':fut VPto^ | 'gonna':fut VPb^", "be going to: the future (i am going to sleep)")
rule("Pred -> 'about' VPto^ | 'supposed' VPto^ | 'able' VPto^ | 'used' PP^:pred", "about to, supposed to, able to, used to it")
rule("Pred -> Sbar^:pred", "be and a clause (the problem is that i am broke)", -0.3)
rule("Pred -> 'like' NP^ | 'like' AdjP^ | 'like' S^ | 'like' Pred^", "chat's 'like' (he is like 6 foot, i was like no)", -0.4)
rule("Pred -> Pred^ AdvP | Pred^ PP | Pred^ Sbar | Pred^ NPt", "adjuncts after the predicate (tired today, busy at work)", -0.15)
rule("Pred -> AdvP Pred^", "an adverb before the predicate (always tired, just chilling)", -0.05)
rule("Pred -> AdvNeg:neg Pred^", "never before the predicate (never late)")
rule("Pred -> Pred^ Cc Pred:conj", "predicates joined (tired and bored)", -0.15)
rule("Pred -> Being Pred^", "being (you are being weird)", -0.1)
rule("Pred/NP -> VPg/NP^:prog | VPn/NP^:pass | PP/NP^ | 'like'", "a predicate with the gap (what are you doing, what is it like)")
rule("Pred/NP -> 'going':fut VPto/NP^", "going to, with the gap (what are you going to do)")
rule("Pred/NP -> Pred/NP^ AdvP | Pred/NP^ PP | Pred/NP^ NPt", "adjuncts after a predicate with the gap", -0.1)
rule("Pred/NP -> AdvP Pred/NP^", "an adverb before a predicate with the gap", -0.05)

# ---- the verb group of a clause: auxiliaries, negation, tense ------------------------------------------------------
rule("VPfin -> VPb^ | VPz^", "a present verb phrase (i like it, she likes it)")
rule("VPfin -> VPd^:past", "a past verb phrase (i liked it)")
rule("VPfin -> BeP Pred^ | BeD:past Pred^", "be and its predicate (i am tired, it was fun)")
rule("VPfin -> BeP Neg:neg Pred^ | BeD:past Neg:neg Pred^", "not after be (i am not tired)")
rule("VPfin -> Md:modal VPbare^", "a modal and a phrase (i can play, i would like that)", -0.01)
rule("VPfin -> Md:modal Neg:neg VPbare^", "a modal, not and a phrase (i can not go)", -0.01)
rule("VPfin -> 'will':fut VPbare^ | 'will':fut Neg:neg VPbare^ | 'shall':fut VPbare^", "will: the future")
rule("VPfin -> Do:do Neg:neg VPb^ | Dz:do Neg:neg VPb^ | Dd:past Neg:neg VPb^", "do not, did not (i do not know)")
rule("VPfin -> Do:do VPb^ | Dz:do VPb^ | Dd:past VPb^", "do for emphasis (i do like it, i did try)", -0.5)
rule("VPfin -> Hv:perf VPn^ | Hz:perf VPn^ | Hd:past VPn^", "have and a participle (i have seen it)")
rule("VPfin -> Hv:perf Neg:neg VPn^ | Hz:perf Neg:neg VPn^ | Hd:past Neg:neg VPn^", "have not done")
rule("VPfin -> Hv:perf Been Pred^ | Hz:perf Been Pred^ | Hd:past Been Pred^", "have been (i have been busy)")
rule("VPfin -> Hv:perf Neg:neg Been Pred^ | Hz:perf Neg:neg Been Pred^", "have not been")
rule("VPfin -> AdvP VPfin^", "an adverb before the verb group (i really do, i just got here)", -0.05)
rule("VPfin -> AdvNeg:neg VPfin^", "never (i never said that)")
rule("VPfin -> VPfin^ Cc VPfin:conj", "verb groups joined (i was tired and went to bed)", -0.2)
rule("VPfin -> Dm VPfin^", "a filler (i like literally can not)", -0.5)
rule("VPfin -> VPfin^ AdvP", "an adverb after the verb group (i am fine too)", -0.1)
# the verb understood from before ("yes i do", "i can", "i am not")
rule("VPfin -> BeP^ | BeD^:past | Md^:modal | Do^:do | Dz^:do | Dd^:past | Hv^:perf | Hz^:perf | 'will'^:fut",
     "an auxiliary alone, the rest understood (i am, i do, i can)", -0.6)
rule("VPfin -> BeP^ Neg:neg | BeD^:past Neg:neg | Md^:modal Neg:neg | Do^:do Neg:neg | Dz^:do Neg:neg | "
     "Dd^:past Neg:neg | Hv^:perf Neg:neg | Hz^:perf Neg:neg | 'will'^:fut Neg:neg",
     "an auxiliary and not, the rest understood (i am not, i do not)", -0.55)
# the verb group with a gap (for wh-questions and relative clauses)
rule("VPfin/NP -> VPb/NP^ | VPz/NP^", "a present verb phrase with the gap")
rule("VPfin/NP -> VPd/NP^:past", "a past verb phrase with the gap")
rule("VPfin/NP -> BeP Pred/NP^ | BeD:past Pred/NP^ | BeP Neg:neg Pred/NP^", "be and a predicate with the gap")
rule("VPfin/NP -> BeP^ | BeD^:past", "be with its predicate as the gap (what your name is)", -0.2)
rule("VPfin/NP -> Md:modal VPbare/NP^ | Md:modal Neg:neg VPbare/NP^ | 'will':fut VPbare/NP^", "a modal, with the gap")
rule("VPfin/NP -> Do:do Neg:neg VPb/NP^ | Dz:do Neg:neg VPb/NP^ | Dd:past Neg:neg VPb/NP^", "do not, with the gap")
rule("VPfin/NP -> Hv:perf VPn/NP^ | Hz:perf VPn/NP^ | Hd:past VPn/NP^", "have done, with the gap")
rule("VPfin/NP -> AdvP VPfin/NP^ | AdvNeg:neg VPfin/NP^", "an adverb before a verb group with the gap", -0.05)
