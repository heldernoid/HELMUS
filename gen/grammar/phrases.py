"""The grammar's phrases: noun phrases, adjective, adverb and preposition phrases. Shared by every persona.

Costs say how much less likely a reading is (in the parser's units, thousandths). The cheapest reading of a phrase
is a plain one: a determiner and a noun, an adjective, a preposition and its noun phrase. Attachments that chat makes
ambiguous ("a game with friends": the game has friends, or the playing does) cost a little more on the noun."""
from gen.dsl import rule

# ---- the noun and what is built around it (Nom: a noun with its describing words, no determiner) -------------------
rule("Nom -> N^ | Ns^", "a noun")
rule("Nom -> Np^", "a name inside a noun phrase (my xbox, the ohio state game)", -0.15)
rule("Nom -> Ntime^", "a time noun as a plain noun (the day was long, what time is it)", -0.4)
rule("Nom -> AdjP Nom^", "describing words before the noun (a new job, really good pizza)", -0.05)
rule("Nom -> N Nom^", "a noun before a noun: compounds (pizza place, phone case); the last noun is the head", -0.25)
rule("Nom -> Ns Nom^", "a plural before a noun: chat drops the apostrophe (my brothers dog)", -0.5)
rule("Nom -> Np Nom^", "a name before a noun (ohio state football, taco bell food)", -0.3)
rule("Nom -> PossN Nom^", "a possessive before a noun (my brother's dog)", -0.05)
rule("Nom -> Vg Nom^", "an -ing word before a noun (gaming chair, swimming pool)", -0.45)
rule("Nom -> Vn Nom^", "a participle before a noun (fried chicken, a used car)", -0.45)
rule("Nom -> Ord Nom^", "first, last, next before a noun", -0.05)
rule("Nom -> Num Nom^", "a number inside the phrase (my two cats, the 3 games)", -0.1)
rule("Nom -> Nom^ PP", "a preposition phrase after the noun (a friend from work)", -0.2)
rule("Nom -> Nom^ Rel", "a relative clause after the noun (the game i play)", -0.15)
rule("Nom -> Nom^ VPg", "an -ing phrase after the noun (people sitting there)", -0.55)
rule("Nom -> Nom^ VPn", "a participle phrase after the noun (a game called valorant)", -0.55)
rule("Nom -> Nom^ VPto", "a to-phrase after the noun (time to go, a game to play)", -0.4)
rule("Nom -> Nom^ Cc Nom:conj", "nouns joined (cats and dogs)", -0.2)
rule("Nom -> Nom^ 'and' 'stuff' | Nom^ 'and' 'things' | Nom^ 'or' 'something' | Nom^ 'and' 'everything' | "
     "Nom^ 'or' 'whatever' | Nom^ 'and' 'all' 'that'", "a vague tail (games and stuff, pizza or something)", -0.05)

# ---- noun phrases -------------------------------------------------------------------------------------------------
rule("NP -> Det Nom^ | Dem Nom^ | Poss Nom^ | Q Nom^", "a determiner and a noun")
rule("NP -> Det Num Nom^ | Poss Num Nom^ | Dem Num Nom^", "a determiner, a number and a noun (my two cats)")
rule("NP -> Det Ord Nom^ | Poss Ord Nom^ | Dem Ord Nom^", "the first..., my last..., this next...")
rule("NP -> Num Nom^", "a number and a noun (two dogs, 5 hours)")
rule("NP -> PossP Nom^", "a possessor and a noun (my brother's dog, sam's car)")
rule("PossP -> PossN^ | Det PossN^ | Poss PossN^ | Dem PossN^", "the possessor (my brother's)")
rule("NP -> Nom^", "a bare noun: plurals and mass nouns (dogs, pizza), or chat dropping the article", -0.4)
rule("NP -> QP Nom^", "an amount with a degree word (way too much coffee, so many people)")
rule("QP -> AdvDeg Q^ | AdvDeg QP^", "a degree word before an amount (too much, way too many)")
rule("NP -> Np^", "a name")
rule("NP -> Np Np^", "a two-word name (new york is two words, taylor swift)", -0.15)
rule("NP -> Pr1^ | Pr2^ | PrS^ | PrIt^ | PrO^ | PrRefl^ | PrPoss^", "a pronoun")
rule("NP -> PrInd^", "someone, something, nothing")
rule("NP -> PrInd^ AdjP", "something good, nothing special", -0.05)
rule("NP -> PrInd^ 'else' | WhN^ 'else'", "something else", -0.02)
rule("NP -> PrInd^ VPto", "something to do, nothing to eat", -0.1)
rule("NP -> PrInd^ Rel", "someone who gets it, something i said", -0.1)
rule("NP -> PrInd^ PP", "someone from work, nothing about it", -0.15)
rule("NP -> Dem^", "this, that (that is cool)", -0.15)
rule("NP -> Q^", "some, all, both (i want some)", -0.4)
rule("NP -> Q 'of' NP^ | Num 'of' NP^ | Ord 'of' NP^", "some of my friends, two of them, the first of them")
rule("NP -> Num^", "a number (i am 19, at 5)", -0.1)
rule("NP -> Num^ Ampm | Num^ 'oclock' | Num^ Num", "a time (5 pm, 10 oclock, 10 30)", -0.05)
rule("NP -> Num^ Nom", "an age, an amount (19 years, 5 bucks)", -0.1)
rule("NP -> 'today'^ | 'tonight'^ | 'tomorrow'^ | 'yesterday'^ | 'tmrw'^", "a time word as a noun phrase "
     "(today is my birthday)", -0.3)
rule("NP -> NPt^", "a time phrase as a noun phrase (last night was fun)", -0.3)
rule("NPt -> 'last' Ntime^ | 'next' Ntime^ | 'this' Ntime^ | 'that' Ntime^ | 'every' Ntime^ | 'each' Ntime^ | "
     "'all' Ntime^ | 'most' Ntime^ | 'some' Ntime^ | 'one' Ntime^ | 'the' 'other' Ntime^ | 'the' 'whole' Ntime^ | "
     "'all' 'the' Ntime^ | Num Ntime^ | 'a' Ntime^ | 'today'^ | 'tonight'^ | 'tomorrow'^ | 'yesterday'^ | 'tmrw'^ | "
     "'last' Np^ | 'this' Np^ | 'next' Np^ | 'every' Np^ | 'all' 'day' 'long' | 'all' 'night' 'long' | "
     "'these' 'days' | 'those' 'days' | 'the' 'next' Ntime^ | 'the' 'last' Ntime^ | 'once' 'a' Ntime^ | "
     "'twice' 'a' Ntime^ | Num 'times' 'a' Ntime^ | 'every' 'single' Ntime^ | 'all' 'the' 'time'",
     "a time phrase: when or how often (last night, every day, all week, two years)")
rule("NPt -> NPt^ 'ago' | NPt^ 'now' | AdvDeg NPt^ | 'like' NPt^", "two days ago, for like two years now", -0.05)
rule("NP -> Det AdjS^ | Poss AdjS^ | Det AdjC^", "the best, my favorite one, the better one", -0.1)
rule("NP -> Det Adj^", "the same, the other, a little", -0.4)
rule("NP -> NP^ PP", "a noun phrase with a preposition phrase after it", -0.35)
rule("NP -> NP^ Rel", "a noun phrase with a relative clause", -0.25)
rule("NP -> NP^ Cc NP:conj", "noun phrases joined (my mom and my sister)", -0.15)
rule("NP -> Pr2^ Q | PrS^ Q", "you all, we both, they all", -0.1)
rule("NP -> Pr2^ 'guys' | PrS^ 'guys' | Pr2^ 'two' | Pr2^ 'people'", "you guys, we two", -0.05)
rule("NP -> Q 'the' Nom^ | Q Poss Nom^ | Q Dem Nom^", "all the games, both my parents, all these people")
rule("NP -> 'a' 'lot' | 'a' 'bit' | 'a' 'little' | 'a' 'couple' | 'a' 'few' | 'lots'", "an amount", -0.05)
rule("NP -> 'a' 'lot' 'of' NP^ | 'lots' 'of' NP^ | 'a' 'bunch' 'of' NP^ | 'a' 'couple' 'of' NP^ | "
     "'a' 'few' Nom^ | 'tons' 'of' NP^ | 'a' 'ton' 'of' NP^ | 'plenty' 'of' NP^ | 'a' 'little' 'bit' 'of' NP^",
     "an amount of something (a lot of games): the head is the something")
rule("NP -> 'kind' 'of' NP^ | 'sort' 'of' NP^ | 'type' 'of' NP^", "a kind of something (kind of a jerk)", -0.2)
rule("NP -> 'that' 'kind' 'of' Nom^ | 'this' 'kind' 'of' Nom^ | 'what' 'kind' 'of' Nom^", "that kind of music", -0.05)
rule("NP -> Det Nom^ 'ago' | Num Nom^ 'ago' | 'a' 'while' 'ago' | 'a' 'long' 'time' 'ago'", "two days ago", -0.05)
rule("NP -> NP^ 'too' | NP^ 'though'", "a noun phrase with a tail (you too, me though)", -0.2)
rule("NP -> AdvDeg NP^", "just me, only you, even my mom (as degree words before a noun phrase)", -0.4)
rule("NP -> Adv NP^", "just me, only you, also my sister", -0.3)
rule("NP -> NP^ 'and' 'stuff' | NP^ 'or' 'something' | NP^ 'and' 'everything' | NP^ 'or' 'whatever' | "
     "NP^ 'and' 'all'", "a vague tail", -0.05)

# ---- adjective phrases ----------------------------------------------------------------------------------------------
rule("AdjP -> Adj^", "an adjective")
rule("AdjP -> AdjC^ | AdjS^", "a comparative, a superlative")
rule("AdjP -> AdvDeg AdjP^", "a degree word before it (really good, so tired, too hot)")
rule("AdjP -> Adv AdjP^", "an adverb before it (always busy, never ready, super chill)", -0.2)
rule("AdjP -> AdjP^ PP", "with a preposition phrase (good at games, scared of spiders, tired of school)", -0.15)
rule("AdjP -> AdjP^ VPto", "with a to-phrase (happy to help, hard to say)", -0.15)
rule("AdjP -> AdjP^ Sbar", "with a clause (glad that you came, sorry if i was rude)", -0.3)
rule("AdjP -> AdjC^ ThanP | AdjP^ ThanP", "better than that")
rule("ThanP -> Than NP^ | Than S^ | Than VPg^ | Than AdvP^ | Than PP^", "than something")
rule("AdjP -> 'more' AdjP^ | 'less' AdjP^ | 'most' AdjP^ | 'the' 'most' AdjP^", "more fun, most beautiful", -0.05)
rule("AdjP -> 'as' AdjP^ 'as' NP | 'as' AdjP^ 'as' S | 'as' AdjP^ 'as' 'possible' | 'so' AdjP^ Sbar",
     "as good as it gets, so tired that...", -0.05)
rule("AdjP -> 'kind' 'of' AdjP^ | 'sort' 'of' AdjP^ | 'a' 'little' AdjP^ | 'a' 'bit' AdjP^ | "
     "'a' 'little' 'bit' AdjP^", "a hedge before it (kind of tired, a bit cold)")
rule("AdjP -> 'not':neg 'that' AdjP^ | 'not':neg 'very' AdjP^ | 'not':neg 'too' AdjP^ | 'not':neg 'so' AdjP^",
     "not that deep, not very good: a negation")
rule("AdjP -> AdjP^ 'enough' | AdjP^ 'af' | AdjP^ 'as' 'hell' | AdjP^ 'as' 'heck' | AdjP^ 'ish' | AdjP^ 'tho'",
     "a tail (good enough, tired af, cold as hell)", -0.05)
rule("AdjP -> AdjP^ Cc AdjP:conj", "joined (tired and bored)", -0.15)
rule("AdjP -> AdjP^ AdvP AdjP:conj", "not sad just tired, not hot but warm", -0.2)
rule("AdjP -> Vn^", "a participle as a describing word (bored, tired, done, excited)", -0.25)
rule("AdjP -> Vg^", "an -ing word as a describing word (boring, amazing, annoying)", -0.45)
rule("AdjP -> Neg:neg AdjP^", "not good, not bad", -0.1)

# ---- adverb phrases -----------------------------------------------------------------------------------------------
rule("AdvP -> Adv^ | AdvT^ | AdvF^", "an adverb")
rule("AdvP -> AdvNeg^:neg", "never")
rule("AdvP -> AdvDeg AdvP^", "really often, so late, too much")
rule("AdvP -> AdvDeg^", "a degree word alone (so, too, very: i love it so much)", -0.6)
rule("AdvP -> 'right' AdvT^ | 'right' 'here' | 'right' 'there' | 'right' 'away' | 'just' AdvT^ | 'until' AdvT^ | "
     "'till' AdvT^ | 'since' AdvT^ | 'by' AdvT^ | 'for' AdvT^ | 'from' AdvT^", "right now, just now, until now")
rule("AdvP -> 'at' 'all' | 'a' 'lot' | 'for' 'real' | 'of' 'course' | 'by' 'the' 'way' | 'to' 'be' 'honest' | "
     "'not' 'really' | 'kind' 'of' | 'sort' 'of' | 'pretty' 'much' | 'so' 'much' | 'too' 'much' | 'very' 'much' | "
     "'all' 'the' 'time' | 'most' 'of' 'the' 'time' | 'in' 'general' | 'for' 'sure' | 'for' 'now' | "
     "'at' 'least' | 'at' 'first' | 'at' 'last' | 'at' 'the' 'moment' | 'right' 'now' | 'these' 'days' | "
     "'back' 'then' | 'every' 'now' 'and' 'then' | 'once' 'in' 'a' 'while' | 'from' 'time' 'to' 'time' | "
     "'more' 'or' 'less' | 'no' 'matter' 'what' | 'as' 'well' | 'in' 'my' 'opinion' | 'all' 'day' | "
     "'all' 'night' | 'all' 'week' | 'a' 'little' | 'a' 'bit' | 'a' 'little' 'bit' | 'even' 'more' | "
     "'not' 'yet' | 'not' 'anymore' | 'not' 'much' | 'like' 'that' | 'like' 'this' | 'so' 'far' | "
     "'last' 'night' | 'last' 'week' | 'next' 'week' | 'this' 'weekend' | 'the' 'other' 'day' | 'for' 'a' 'while' | "
     "'for' 'ages' | 'in' 'a' 'bit' | 'in' 'a' 'while' | 'any' 'more' | 'any' 'longer' | 'no' 'longer' | "
     "'on' 'purpose' | 'by' 'accident' | 'in' 'person' | 'online' | 'at' 'home' | 'at' 'work' | 'at' 'school' | "
     "'over' 'there' | 'up' 'here' | 'down' 'here' | 'out' 'here' | 'back' 'home' | 'for' 'once' | 'together'",
     "set adverb phrases")
rule("AdvP -> AdvP^ 'too' | AdvP^ 'though' | AdvP^ 'enough' | AdvP^ 'already'", "a tail", -0.1)
rule("AdvP -> NP 'ago'^ | NP 'later'^ | NP 'before'^ | NP 'after'^", "two days ago, a week later", -0.05)
rule("AdvP -> AdvP^ Cc AdvP:conj", "joined (now and then, here and there)", -0.15)
rule("AdvP -> Neg:neg AdvP^", "not really, not always, not now", -0.05)

# ---- preposition phrases --------------------------------------------------------------------------------------------
rule("PP -> P^ NP", "a preposition and its noun phrase")
rule("PP -> To^ NP", "to and a noun phrase (to the store, to my mom)", -0.05)
rule("PP -> P^ VPg", "a preposition and an -ing phrase (about going, after work, before sleeping)", -0.05)
rule("PP -> P^ WhCl", "a preposition and a wh-clause (about what you said)", -0.15)
rule("PP -> P^ AdvP", "a preposition and an adverb (from here, until now, for now)", -0.2)
rule("PP -> P^ PP", "two prepositions (from under the bed, out of the house)", -0.3)
rule("PP -> AdvDeg PP^ | Adv PP^", "right after work, just before bed, even in summer", -0.15)
rule("PP -> PP^ Cc PP:conj", "joined (at home or at work)", -0.15)
rule("PP -> P^", "a preposition alone: stranded or a particle (where are you from, come on)", -0.7)
rule("PP -> 'because' 'of' NP^ | 'instead' 'of' NP^ | 'instead' 'of' VPg^ | 'out' 'of' NP^ | 'next' 'to' NP^ | "
     "'in' 'front' 'of' NP^ | 'thanks' 'to' NP^ | 'such' 'as' NP^ | 'all' 'over' NP^ | 'up' 'to' NP^ | "
     "'away' 'from' NP^ | 'close' 'to' NP^ | 'according' 'to' NP^ | 'apart' 'from' NP^ | 'ahead' 'of' NP^ | "
     "'on' 'top' 'of' NP^ | 'in' 'the' 'middle' 'of' NP^ | 'at' 'the' 'end' 'of' NP^ | 'as' 'for' NP^ | "
     "'other' 'than' NP^ | 'rather' 'than' NP^ | 'except' 'for' NP^ | 'due' 'to' NP^ | 'along' 'with' NP^ | "
     "'right' 'next' 'to' NP^ | 'outside' 'of' NP^ | 'inside' 'of' NP^ | 'kind' 'of' 'like' NP^ | 'just' 'like' NP^",
     "multi-word prepositions")
rule("PP -> 'like' NP^ | 'like' VPg^", "like something (like my dad, like gaming)", -0.1)
