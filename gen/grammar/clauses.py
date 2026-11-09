"""The grammar's clauses: statements, questions, commands, and the clauses inside them. Shared by every persona.

  S     a statement (i like pizza; chat drops subjects and be: "went to the store", "you good")
  Sq    a yes/no question, by its inverted auxiliary (do you like pizza, are you a bot, can you hear me)
  Sw    a wh-question (what do you like, where are you from, how old are you, who made you)
  Simp  a command or request (tell me about yourself, do not lie, let me know)
  Sbar  a clause under a conjunction (because i was bored, if you want, that you like it)
  Rel   a relative clause (the game i play, someone who gets it)
  WhCl  a wh-clause inside a sentence (i know what you mean, tell me where you live)

The roles marked here (subj, wh, q, sub, conj, voc) and in the verb group (neg, past, fut...) become the message's G:
features: who the subject is, whether the main clause is negated, asked, past...
"""
from gen.dsl import rule

# ---- statements -------------------------------------------------------------------------------------------------
rule("S -> NP:subj VPfin^", "a subject and its verb group")
rule("S -> VPfin^", "no subject: chat drops it (went to the store, love that, sounds good)", -0.9)
rule("S -> NPpro:subj Pred^", "no be after a pronoun: chat drops it (you good, u there, that crazy)", -0.6)
rule("NPpro -> Pr1^ | Pr2^ | PrS^ | PrIt^ | PrO^ | Dem^", "a pronoun subject")
rule("S -> VPg^:prog", "no subject and no be: chat drops both (just chilling at home)", -0.5)
rule("S -> Ex:subj BeP^ NP:pred | Ex:subj BeD^:past NP:pred | Ex:subj BeP^ Neg:neg NP:pred | "
     "Ex:subj BeD^:past Neg:neg NP:pred", "there is, there was (there is a dog outside): 'there' is the subject")
rule("S -> Ex:subj Md^:modal Be NP:pred | Ex:subj Hz^:perf Been NP:pred | Ex:subj 'will'^:fut Be NP:pred",
     "there could be, there has been, there will be")
rule("S -> 'it':subj 'is'^ Pred | 'that':subj 'is'^ Pred", "it is..., that is...", -0.05)
rule("S -> AdvP S^", "an adverb first (honestly i love it, today i slept in)", -0.1)
rule("S -> S^ AdvP", "an adverb last (i love it honestly)", -0.12)
rule("S -> PP S^", "a preposition phrase first (at work i just stock shelves)", -0.2)
rule("S -> S^ PP", "a preposition phrase last", -0.4)
rule("S -> NPt S^", "a time phrase first (last night i played valorant)", -0.1)
rule("S -> Sbar:sub S^", "a clause first (if you want, we can talk)", -0.1)
rule("S -> S^ Sbar:sub", "a clause last (i stayed in because it rained)", -0.15)
rule("S -> S^ Cc S:conj", "statements joined (i like it but it is expensive)", -0.15)
rule("S -> Cc S^", "a statement that goes on from before (and then i left, but i like it)", -0.25)
rule("S -> Ij S^ | S^ Ij", "an interjection with it (lol i hate it, i hate it lol)", -0.05)
rule("S -> Dm S^ | S^ Dm", "a filler with it (honestly i love it, i love it though)", -0.1)
rule("S -> S^ TagQ:q", "a tag question at the end (you like it right, it is cold isnt it)", -0.1)
rule("S -> NPvoc:voc S^ | S^ NPvoc:voc", "calling the other person by name (josh you there, thanks man)", -0.6)
rule("NPvoc -> Np^ | 'man' | 'bro' | 'dude' | 'bud' | 'buddy' | 'sir' | 'girl' | 'guys' | 'everyone' | 'mate' | "
     "'fam' | 'homie' | 'bestie' | 'babe' | 'honey' | 'sweetie' | 'friend' | 'bruh' | 'lol'",
     "a name or a word for the person, said to them")
rule("S -> S^ 'too' | S^ 'though' | S^ 'tho' | S^ 'either' | S^ 'anyway' | S^ 'lol' | S^ 'haha' | S^ 'ngl' | "
     "S^ 'tbh' | S^ 'fr' | S^ 'rn' | S^ 'then' | S^ 'again'", "a tail (i like it too, i am tired tho)", -0.05)
rule("S -> 'i' 'mean' S^ | 'i' 'guess' S^ | 'i' 'think' S^ | 'i' 'feel' 'like' S^ | 'i' 'swear' S^ | "
     "'i' 'bet' S^ | 'you' 'know' S^ | 'to' 'be' 'honest' S^ | 'not' 'going' 'to' 'lie' S^ | 'in' 'my' 'opinion' S^ | "
     "'by' 'the' 'way' S^ | 'oh' 'my' 'god' S^ | 'for' 'real' S^",
     "a hedge before a statement (i mean it is fine, ngl i love it): the statement is the main clause", -0.05)

# ---- yes/no questions -------------------------------------------------------------------------------------------
rule("Sq -> Do:q NP:subj VPb^ | Dz:q NP:subj VPb^ | Dd:past NP:subj VPb^", "do you..., does it..., did you...")
rule("Sq -> Do:q Neg:neg NP:subj VPb^ | Dz:q Neg:neg NP:subj VPb^ | Dd:past Neg:neg NP:subj VPb^",
     "do not you..., did not you... (dont you like it)")
rule("Sq -> Do:q NP:subj Neg:neg VPb^ | Dd:past NP:subj Neg:neg VPb^", "do you not..., did you not...")
rule("Sq -> Md:modal NP:subj VPbare^ | Md:modal Neg:neg NP:subj VPbare^", "can you..., would you...", -0.01)
rule("Sq -> 'will':fut NP:subj VPbare^ | 'will':fut Neg:neg NP:subj VPbare^", "will you..., will it...")
rule("Sq -> BeP:q NP:subj Pred^ | BeD:past NP:subj Pred^", "are you..., is it..., were you...")
rule("Sq -> BeP:q Neg:neg NP:subj Pred^ | BeD:past Neg:neg NP:subj Pred^ | BeP:q NP:subj Neg:neg Pred^",
     "are not you..., is it not...")
rule("Sq -> Hv:perf NP:subj VPn^ | Hz:perf NP:subj VPn^ | Hd:past NP:subj VPn^ | Hv:perf NP:subj AdvF VPn^",
     "have you..., has it..., have you ever...")
rule("Sq -> Hv:perf NP:subj Been Pred^ | Hz:perf NP:subj Been Pred^ | Hv:perf Neg:neg NP:subj VPn^",
     "have you been..., have not you...")
rule("Sq -> BeP:q Ex:ex NP:subj | BeD:past Ex:ex NP:subj | BeP:q Neg:neg Ex:ex NP:subj",
     "is there..., was there..., are there any...")
rule("Sq -> Do:q NP:subj^ | Dz:q NP:subj^ | Dd:past NP:subj^ | BeP:q NP:subj^ | BeD:past NP:subj^ | "
     "Md:modal NP:subj^ | Hv:perf NP:subj^ | Hz:perf NP:subj^ | 'will':fut NP:subj^",
     "the question with the rest understood (do you?, are you?, can you?)", -0.35)
rule("Sq -> Sq^ AdvP | Sq^ PP | Sq^ Sbar:sub | Sq^ NPt", "an adjunct after the question (do you play a lot, do you "
     "work tonight)", -0.15)
rule("Sq -> Sbar:sub Sq^", "a clause first (if you won, would you quit)", -0.1)
rule("Sq -> AdvP Sq^ | Dm Sq^ | Ij Sq^ | Cc Sq^ | Sq^ Ij | Sq^ Dm", "a word before or after the question (so do you "
     "game, wait are you a bot, do you like it lol)", -0.15)
rule("Sq -> Sq^ 'or' 'not' | Sq^ 'or' 'what' | Sq^ 'or' 'nah' | Sq^ 'or' 'no' | Sq^ 'too' | Sq^ 'though' | "
     "Sq^ 'tho' | Sq^ 'rn' | Sq^ 'then' | Sq^ 'still' | Sq^ 'yet' | Sq^ 'again'", "a tail (are you a bot or not)", -0.05)
rule("Sq -> Sq^ Cc Sq:conj | Sq^ Cc VPb:conj", "questions joined (do you game or do you read)", -0.15)
rule("Sq -> Sq^ NPvoc:voc | NPvoc:voc Sq^", "calling the other person by name", -0.6)
rule("Sq -> 'you' 'know' Sq^ | 'i' 'mean' Sq^ | 'by' 'the' 'way' Sq^ | 'be' 'honest' Sq^ | 'honestly' Sq^ | "
     "'quick' 'question' Sq^ | 'so' 'like' Sq^", "a lead-in before the question", -0.05)

# ---- wh-questions -----------------------------------------------------------------------------------------------
rule("WhNP -> WhN^", "what, who")
rule("WhNP -> WhD Nom^", "which game, what music, whose car")
rule("WhNP -> 'what' 'kind' 'of' Nom^ | 'what' 'kinds' 'of' Nom^ | 'what' 'type' 'of' Nom^ | 'what' 'sort' 'of' Nom^ | "
     "'which' 'one' | 'which' 'ones' | 'which' 'of' NP^ | 'what' 'part' 'of' NP^", "what kind of music, which one")
rule("WhNP -> 'how' 'many' Nom^ | 'how' 'much' Nom^ | 'how' 'many'^ | 'how' 'much'^", "how many, how much")
rule("WhNP -> WhN^ 'else' | WhN^ 'exactly' | WhN^ 'the' 'hell' | WhN^ 'the' 'heck' | WhN^ 'on' 'earth' | WhN^ 'even'",
     "what else, what the hell, who even")
rule("WhAdvP -> WhA^", "where, when, why, how")
rule("WhAdvP -> 'how' AdjP^ | 'how' AdvP^", "how old, how long, how often")
rule("WhAdvP -> 'how' 'come' | WhA^ 'else' | WhA^ 'exactly' | WhA^ 'the' 'hell' | WhA^ 'the' 'heck' | "
     "WhA^ 'on' 'earth' | WhA^ 'even' | 'since' 'when' | 'until' 'when' | 'what' 'time'", "how come, why the hell")
rule("Sw -> WhNP:whsubj VPfin^", "the question word as the subject (who made you, what happened)", -0.1)
rule("Sw -> WhNP:wh BeP^ NP:subj | WhNP:wh BeD^:past NP:subj | WhNP:wh BeP^ Neg:neg NP:subj",
     "what is your name, who are you, what was that")
rule("Sw -> WhNP:wh Sq/NP^", "the question word as the object (what do you like, who are you talking to)")
rule("Sw -> WhAdvP:wh Sq^", "where, when, why or how and a question (where do you live, why are you sad)")
rule("Sw -> WhAdvP:wh BeP^ NP:subj | WhAdvP:wh BeD^:past NP:subj", "how are you, where are you, how was it")
rule("Sw -> WhAdvP:wh NP:subj Pred^ | WhAdvP:wh NP:subj VPfin^ | WhAdvP:wh NP:subj Been^", "chat without the "
     "auxiliary (where you at, how you doing, why you ask, how you been)", -0.5)
rule("Sw -> WhNP:wh NP:subj Pred/NP^ | WhNP:wh NP:subj VPfin/NP^", "chat without the auxiliary (what you doing, "
     "what u mean)", -0.5)
rule("Sw -> WhNP:wh VPto/NP^ | WhAdvP:wh VPto^", "what to do?, how to play?", -0.4)
rule("Sw -> WhNP^:wh | WhAdvP^:wh", "the question word alone (what?, why?, how so)", -0.3)
rule("Sw -> 'what':wh 'about' NP^ | 'how':wh 'about' NP^ | 'how':wh 'about' VPg^ | 'what':wh 'about' VPg^ | "
     "'what':wh 'if' S^ | 'why':wh 'not' | 'how':wh 'come' S^ | 'how':wh 'so' | 'what':wh 'for' | "
     "'what':wh 'about' 'it' | 'what':wh 'do' 'you' 'mean' | 'what':wh 'is' 'up' | "
     "'what':wh 'is' 'up' 'with' NP^ | 'what':wh 'is' 'it' 'like' | 'what':wh 'is' 'that' 'like' | "
     "'why':wh 'do' 'you' 'ask' | 'how':wh 'do' 'you' 'know' | 'what':wh 'makes' 'you' 'think' 'that' | "
     "'who':wh 'cares' | 'what':wh 'now' | 'what':wh 'then' | 'what':wh 'is' 'new'",
     "set wh-questions (what about you, how about you, what if..., why not)", -0.02)
rule("Sw -> Sw^ AdvP | Sw^ PP | Sw^ Sbar:sub | Sw^ NPt", "an adjunct after the question (what do you do for fun, "
     "where are you from originally)", -0.15)
rule("Sw -> Sbar:sub Sw^", "a clause first (if you could have any superpower what would it be)", -0.1)
rule("Sw -> AdvP Sw^ | Dm Sw^ | Ij Sw^ | Cc Sw^ | Sw^ Ij | Sw^ Dm", "a word before or after the question (so what "
     "do you do, lol what)", -0.15)
rule("Sw -> Sw^ 'though' | Sw^ 'tho' | Sw^ 'then' | Sw^ 'again' | Sw^ 'rn' | Sw^ 'lol' | Sw^ 'exactly' | "
     "Sw^ 'anyway' | Sw^ 'today' | Sw^ 'tonight' | Sw^ 'now'", "a tail (what is your name again)", -0.05)
rule("Sw -> Sw^ Cc Sw:conj | Sw^ Cc Sq:conj", "questions joined (where are you from and what do you do)", -0.15)
rule("Sw -> Sw^ NPvoc:voc | NPvoc:voc Sw^", "calling the other person by name", -0.6)
rule("Sw -> 'so' Sw^ | 'wait' Sw^ | 'okay' Sw^ | 'quick' 'question' Sw^ | 'by' 'the' 'way' Sw^ | "
     "'out' 'of' 'curiosity' Sw^ | 'just' 'curious' Sw^ | 'i' 'mean' Sw^", "a lead-in before the question", -0.05)
rule("Sq/NP -> Do:q NP:subj VPb/NP^ | Dz:q NP:subj VPb/NP^ | Dd:past NP:subj VPb/NP^",
     "do you..., with the question word missing (what do you like)")
rule("Sq/NP -> Do:q Neg:neg NP:subj VPb/NP^ | Dd:past Neg:neg NP:subj VPb/NP^", "do not you..., with the gap")
rule("Sq/NP -> Md:modal NP:subj VPbare/NP^ | Md:modal Neg:neg NP:subj VPbare/NP^",
     "can you..., with the gap (what can you do, what would you say)", -0.01)
rule("Sq/NP -> 'will':fut NP:subj VPbare/NP^", "will you..., with the gap (what will you do)")
rule("Sq/NP -> BeP:q NP:subj Pred/NP^ | BeD:past NP:subj Pred/NP^ | BeP:q Neg:neg NP:subj Pred/NP^",
     "are you..., with the gap (what are you doing, who were you with)")
rule("Sq/NP -> Hv:perf NP:subj VPn/NP^ | Hz:perf NP:subj VPn/NP^ | Hd:past NP:subj VPn/NP^",
     "have you..., with the gap (what have you done)")
rule("S/NP -> NP:subj VPfin/NP^", "a statement with a noun phrase missing (the game [i play _], what [you mean _])")
rule("S/NP -> NP:subj Pred/NP^", "the same without be (what [you doing _])", -0.5)
rule("S/NP -> VPfin^", "a statement whose subject is the gap (who do you think [_ will win])", -0.1)
rule("S/NP -> S/NP^ AdvP | S/NP^ PP | AdvP S/NP^", "adjuncts around a statement with the gap", -0.15)

# ---- commands and requests ----------------------------------------------------------------------------------------
rule("Simp -> VPb^", "a command: the base verb phrase with no subject (tell me about yourself)", -0.45)
rule("Simp -> Do:do Neg:neg VPb^ | Do:do Neg:neg Be Pred^ | 'never':neg VPb^", "do not (dont lie, dont be weird)")
rule("Simp -> Be Pred^", "be (be honest, be nice)", -0.1)
rule("Simp -> Let^ NP:obj VPb:comp", "let me know, let us go: 'let' is the verb")
rule("Simp -> Pls Simp^ | Simp^ Pls | 'please' 'just' Simp^ | 'just' Simp^", "please")
rule("Simp -> Simp^ Cc Simp:conj", "commands joined (come here and look)", -0.15)
rule("Simp -> Ij Simp^ | Simp^ Ij | Dm Simp^ | AdvP Simp^", "a word around the command", -0.12)
rule("Simp -> Simp^ NPvoc:voc", "a command to someone by name (come on man)", -0.6)
rule("Simp -> 'go' VPb^ | 'come' VPb^ | 'try' VPb^", "go eat, come see, try it", -0.2)
rule("Simp -> Simp^ 'then' | Simp^ 'already' | Simp^ 'now' | Simp^ 'lol' | Simp^ 'pls' | Simp^ 'again'", "a tail", -0.05)

# ---- clauses inside clauses -------------------------------------------------------------------------------------
rule("Sbar -> Sub:sub S^ | Comp S^", "because..., if..., when..., that...")
rule("Sbar -> Sub:sub Sq^", "if..., whether... with a question's word order (if can you)", -0.8)
rule("Sbar -> Sub:sub VPg^ | Sub:sub AdjP^ | Sub:sub PP^ | Sub:sub NP^", "while driving, if possible, because covid",
     -0.45)
rule("Sbar -> 'so' 'that' S^ | 'even' 'though' S^ | 'even' 'if' S^ | 'as' 'long' 'as' S^ | 'as' 'soon' 'as' S^ | "
     "'as' 'if' S^ | 'as' 'though' S^ | 'in' 'case' S^ | 'now' 'that' S^ | 'only' 'if' S^ | 'just' 'because' S^ | "
     "'ever' 'since' S^ | 'right' 'after' S^ | 'right' 'before' S^ | 'the' 'second' S^ | 'every' 'time' S^ | "
     "'by' 'the' 'time' S^ | 'so' 'much' 'that' S^ | 'except' 'that' S^ | 'given' 'that' S^",
     "multi-word conjunctions")
rule("Sbar -> 'like' S^", "like i said, like you care", -0.35)
rule("Sbar -> AdvP Sbar^ | Sbar^ Cc Sbar:conj", "just because..., because... and because...", -0.2)
rule("Rel -> 'who':rel VPfin^ | 'that':rel VPfin^ | 'which':rel VPfin^", "who lives here, that i like")
rule("Rel -> 'that':rel S/NP^ | 'who':rel S/NP^ | 'which':rel S/NP^ | 'whom':rel S/NP^", "that i play, who i met")
rule("Rel -> S/NP^", "a relative clause without 'that' (the game i play)", -0.35)
rule("Rel -> 'where':rel S^ | 'when':rel S^ | 'whose':rel Nom VPfin^", "the place where i work, the day when...", -0.5)
rule("Rel -> VPg^ | VPn^", "people living here, a game called...", -0.6)
rule("WhCl -> WhNP:wh S/NP^", "what you mean, who i am")
rule("WhCl -> WhNP:wh VPfin^", "who did it, what happened")
rule("WhCl -> WhAdvP:wh S^", "where you live, why you left, how it works")
rule("WhCl -> WhNP:wh VPto/NP^ | WhAdvP:wh VPto^", "what to do, how to play")
rule("WhCl -> 'whether':wh S^ | 'if':wh S^ | 'whether':wh 'or' 'not' S^", "whether..., if...", -0.1)
rule("WhCl -> WhNP:wh NP:subj BeP^ | WhAdvP:wh NP:subj BeP^", "what your name is, where it is", -0.1)
