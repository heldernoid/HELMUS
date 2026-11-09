"""More of the grammar: the constructions beyond the core, so it reads anyone who writes to a persona: the polite and
formal English people use with an older stranger ("Could you please tell me...", "Have you got any grandchildren?",
"I was wondering whether..."), sentence-level constructions (an -ing phrase or a what-clause as the subject, "so do
i", "had better", "would rather"), and the chat hedges and measures ("at like 5", "19 years old"). Shared by every
persona."""
from gen.dsl import rule

# ---- subjects that are not plain noun phrases -----------------------------------------------------------------------
rule("NP -> VPg^", "an -ing phrase as a noun phrase (playing games is fun, i hate doing laundry)", -0.25)
rule("NP -> WhCl^", "a what-clause as a noun phrase (what you said is true, i like what you did)", -0.35)
rule("NP -> VPto^", "a to-phrase as a subject (to be honest is hard)", -0.8)
rule("NP -> 'both' NP^ 'and' NP | 'either' NP^ 'or' NP | 'neither' NP^ 'nor' NP", "both..., either..., neither...")
rule("Nom -> Nom^ Np", "a noun and a name after it (my brother jake, my cat biscuit)", -0.35)
rule("NP -> Np^ Ord | Ord 'of' Np^ | 'the' Ord 'of' Np^", "dates (march 3rd, the 3rd of march)", -0.1)
rule("NP -> 'like' NP^", "chat's 'like' before an amount (like 5 hours, like a lot)", -0.4)
rule("NP -> 'about' Num^ | 'around' Num^ | 'over' Num^ | 'under' Num^ | 'almost' Num^ | 'nearly' Num^ | "
     "'only' Num^ | 'at' 'least' Num^", "about 5, over 20, at least 3", -0.1)
rule("NP -> 'the' 'one'^ | 'this' 'one'^ | 'that' 'one'^ | 'which' 'one'^ | 'the' 'other' 'one'^ | "
     "'the' 'same'^ | 'the' 'rest'^ | 'the' 'others'^ | Poss 'own'^", "the one, this one, my own")
rule("NP -> 'each' 'other' | 'one' 'another'", "each other")

# ---- measures and amounts before a describing word ------------------------------------------------------------------
rule("AdjP -> NP AdjP^", "a measure before it (19 years old, 6 feet tall, two hours long)", -0.35)
rule("AdjP -> 'too' AdjP^ VPto | 'so' AdjP^ 'that' S", "too tired to talk, so tired that...", -0.05)
rule("AdjP -> 'not' 'as' AdjP^ 'as' NP | 'nowhere' 'near' 'as' AdjP^", "not as bad as..., nowhere near as good")

# ---- polite and formal ------------------------------------------------------------------------------------------
rule("Sq -> Md:modal NP:subj 'please' VPbare^ | 'please' Sq^ | Sq^ 'please'", "could you please..., ... please")
rule("Sq -> Md:modal NP:subj 'possibly' VPbare^ | Md:modal NP:subj 'kindly' VPbare^", "could you possibly...")
rule("Sq -> Md:modal NP:subj 'mind' VPg:comp^ | Md:modal Neg:neg NP:subj 'mind' VPg:comp^",
     "would you mind telling me...")
rule("Sq -> Hv:q NP:subj 'got' NP:obj^ | Hz:q NP:subj 'got' NP:obj^ | Hv:q Neg:neg NP:subj 'got' NP:obj^",
     "have you got any..., has she got...")
rule("Sq -> Hv:perf NP:subj Been^ | Hz:perf NP:subj Been^", "the rest understood (how have you been)", -0.1)
rule("VPfin -> Hv:perf Been^ | Hz:perf Been^ | Hd:past Been^", "have been, the rest understood (i have been)", -0.4)
rule("S -> 'how' 'do' 'you' 'do' | 'pleased' 'to' 'meet' 'you' | 'it' 'is' 'nice' 'to' 'meet' 'you' | "
     "'thank' 'you' 'for' VPg^ | 'thanks' 'for' VPg^ | 'thanks' 'for' NP^ | 'thank' 'you' 'for' NP^ | "
     "'sorry' 'for' VPg^ | 'sorry' 'about' NP^ | 'sorry' 'to' VPb^ | 'sorry' Sbar^ | 'i' 'am' 'sorry' 'to' 'hear' 'that'",
     "polite set phrases", -0.02)
rule("Simp -> 'please' 'do' | 'go' 'ahead' | 'feel' 'free' VPto^ | 'do' 'tell' | 'have' 'a' AdjP 'day' | "
     "'have' 'a' 'good' 'one' | 'take' 'your' 'time'", "set requests")

# ---- sentence-level constructions -------------------------------------------------------------------------------
rule("S -> 'so' Do:do NP:subj^ | 'so' BeP NP:subj^ | 'so' Md:modal NP:subj^ | 'so' Hv:perf NP:subj^ | "
     "'neither' Do:do NP:subj^ | 'neither' BeP NP:subj^ | 'neither' Md:modal NP:subj^ | 'nor' Do:do NP:subj^",
     "so do i, neither am i", -0.02)
rule("S -> NP:subj 'too'^ | NP:subj 'either'^ | NP:subj 'neither'^ | 'same' 'for' NP^ | 'same' 'with' NP^",
     "me too, me neither, same for me", -0.3)
rule("VPfin -> Hd:past 'better' VPb^ | Md:modal 'rather' VPbare^ | 'ought' VPto^ | 'would' 'rather' VPbare^ | "
     "Md:modal 'better' VPb^", "had better, would rather, ought to")
rule("VPfin -> 'used' VPto^:past | 'gotta' VPb^ | 'got' VPto^", "used to, gotta, got to", -0.02)
rule("S -> 'it' 'is' Pred^ Sbar | 'it' 'is' Pred^ VPto | 'it' 'was' Pred^ VPto | 'it' 'is' Pred^ WhCl",
     "it is nice that..., it is hard to say, it was fun to watch", -0.02)
rule("S -> WhCl:subj VPfin^", "what you said is true, what i mean is...", -0.5)
rule("NP -> 'whoever'^ VPfin:comp | 'whatever'^ VPfin:comp | 'whatever'^ S/NP:comp", "whoever made this, whatever "
     "you want", -0.1)
rule("Sbar -> 'if' 'so' | 'if' 'not' | 'if' 'anything' | 'if' 'you' 'want' | 'if' 'you' 'can' | "
     "'if' 'possible' | 'when' 'possible' | 'unless' 'you' 'want' 'to'", "if so, if not, if you want", -0.05)
rule("Sw -> 'how' AdjP^ BeP NP:subj | 'how' AdjP^ 'is' 'that' | 'what' 'a' Nom^ | 'what' Nom^ | 'how' AdjP^",
     "exclamations (how cool is that, what a day, how nice)", -0.2)
rule("WhNP -> P WhNP^ | WhD Nom^ PP", "a preposition before the question word (in which city, for whom)", -0.1)
rule("WhAdvP -> P WhAdvP^", "for how long, since when, from where", -0.1)
rule("Sw -> 'how' 'about' S^ | 'how' 'about' 'we' VPb^ | 'what' 'if' 'we' VPb^ | 'why' 'do' 'not' 'we' VPb^ | "
     "'why' 'not' VPb^", "how about we..., why dont we..., why not ask", -0.02)

# ---- chat hedges and fillers inside phrases ------------------------------------------------------------------------
rule("PP -> P^ 'like' NP | P^ 'about' NP | P^ 'around' NP", "at like 5, for about an hour, at around noon", -0.2)
rule("AdjP -> 'like' AdjP^ | 'literally' AdjP^ | 'actually' AdjP^ | 'honestly' AdjP^", "like so tired, literally dead", -0.15)
rule("S -> 'i' 'mean' 'like' S^ | 'like' S^ | 'literally' S^ | 'ok' 'so' S^ | 'okay' 'so' S^ | 'well' S^ | "
     "'so' 'yeah' S^ | 'anyway' S^ | 'anyways' S^ | 'idk' S^ | 'yes' 'but' S^ | 'no' 'but' S^ | 'i' 'mean' 'yes' S^",
     "a filler before the statement", -0.05)
rule("S -> S^ 'or' 'something' | S^ 'and' 'stuff' | S^ 'i' 'guess' | S^ 'i' 'think' | S^ 'you' 'know' | "
     "S^ 'i' 'mean' | S^ 'like' | S^ 'honestly' | S^ 'for' 'real' | S^ 'lol' 'lol' | S^ 'haha' 'yeah'",
     "a filler after the statement", -0.05)
rule("Sq -> 'you':subj 'think'^ S:comp | 'you':subj 'ever' VPd^ | 'you':subj 'ever' VPn^ | 'ever' VPd^ | "
     "'ever' VPn^ | 'you':subj 'still' VPg^ | 'you':subj VPg^", "chat questions without do or have (you think so?, "
     "you ever been?, ever tried it?, you still there?)", -0.3)
rule("Sq -> 'any' Nom^", "any plans?, any pets? (a question without its verb)", -0.1)
rule("Sq -> 'got' NP^ | 'want' NP^ | 'need' NP^ | 'want' 'to' VPb^",
     "chat questions without a subject (got a minute?, want to play?)", -0.45)
