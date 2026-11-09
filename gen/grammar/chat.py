"""The grammar of a chat message as a whole. Shared by every persona.

A message is a run of fragments (Msg -> Frag, Msg Frag): a clause, a question, a command, or the pieces chat is made
of: an interjection ("lol"), a short answer ("me too", "not really"), a noun phrase ("pizza"), a tag ("right?").
Every extra fragment costs, so one clause over the whole message wins when there is one; any word can still be read
as something (X, at a high cost), so every message has an analysis.

Also here: the categories the network reads (gcat) and how a copied phrase is said back (reflect)."""
from gen.dsl import gcat, reflect, rule

# ---- interjections, set phrases and short answers -----------------------------------------------------------------
rule("IjP -> Ij^", "an interjection (lol, wow, yeah)")
rule("IjP -> Ij^ IjP", "interjections in a row (lol yeah, omg wow)", -0.02)
rule("IjP -> Ij^ NPvoc:voc | IjP^ Pls", "hey josh, thanks man, sorry please", -0.4)
rule("IjP -> AdjP Ij^ | AdvP Ij^", "an answer and thanks (good thanks, fine lol, not bad thanks)", -0.1)
rule("IjP -> 'oh' 'my' 'god' | 'oh' 'my' 'gosh' | 'thank' 'you' | 'thank' 'you' 'so' 'much' | 'never' 'mind' | "
     "'no' 'way' | 'my' 'bad' | 'of' 'course' | 'for' 'real' | 'oh' 'well' | 'see' 'you' | 'see' 'you' 'later' | "
     "'see' 'you' 'soon' | 'see' 'you' 'tomorrow' | 'good' 'morning' | 'good' 'night' | 'good' 'luck' | "
     "'good' 'afternoon' | 'good' 'evening' | 'nice' 'one' | 'same' 'here' | 'me' 'too' | 'me' 'neither' | "
     "'me' 'either' | 'you' 'too' | 'not' 'really' | 'i' 'guess' | 'i' 'think' 'so' | 'i' 'hope' 'so' | "
     "'i' 'do' 'not' 'think' 'so' | 'i' 'guess' 'so' | 'i' 'suppose' | 'not' 'at' 'all' | 'just' 'kidding' | "
     "'be' 'right' 'back' | 'talk' 'to' 'you' 'later' | 'by' 'the' 'way' | 'oh' 'no' | 'oh' 'yeah' | 'oh' 'okay' | "
     "'all' 'good' | 'all' 'right' | 'no' 'problem' | 'no' 'worries' | 'what' 'the' 'hell' | 'what' 'the' 'heck' | "
     "'thank' 'god' | 'excuse' 'me' | 'happy' 'birthday' | 'good' 'job' | 'hell' 'yeah' | 'heck' 'yeah' | "
     "'hell' 'no' | 'oh' 'nice' | 'not' 'bad' | 'not' 'sure' | 'no' 'idea' | 'fair' 'enough' | "
     "'big' 'mood' | 'same' | 'true' | 'facts' | 'no' 'thanks' | 'yes' 'please' | 'sounds' 'good' | "
     "'that' 'is' 'crazy' | 'makes' 'sense' | 'my' 'god' | 'i' 'know' | 'i' 'know' 'right' | 'you' 'know' | "
     "'what' 'is' 'up' | 'good' 'for' 'you' | 'well' 'done' | 'not' 'yet' | 'not' 'anymore' | 'kind' 'of' | "
     "'sort' 'of' | 'all' 'the' 'time' | 'every' 'day' | 'not' 'gonna' 'lie' | 'not' 'going' 'to' 'lie' | "
     "'to' 'be' 'honest' | 'i' 'am' 'good' | 'i' 'am' 'fine' | 'same' 'to' 'you' | 'you' 'are' 'welcome' | "
     "'any' 'time' | 'take' 'care' | 'nice' 'to' 'meet' 'you' | 'nice' 'meeting' 'you' | 'just' 'wondering' | "
     "'just' 'curious' | 'oh' 'really' | 'really' | 'wait' 'what' | 'wait' | 'hold' 'on' | 'one' 'sec' | "
     "'one' 'second' | 'one' 'moment' | 'yes' 'and' 'no' | 'maybe' 'maybe' 'not' | 'it' 'depends' | "
     "'depends' | 'whatever' | 'definitely' | 'probably' | 'maybe' | 'absolutely' | 'totally' | 'exactly' | "
     "'obviously' | 'sure' 'thing' | 'got' 'it' | 'i' 'see' | 'okay' 'then' | 'cool' 'cool' | 'nice' 'nice' | "
     "'love' 'that' | 'love' 'it' | 'hate' 'that' | 'good' 'question' | 'great' 'question' | 'no' 'clue' | "
     "'beats' 'me' | 'who' 'knows' | 'you' 'tell' 'me' | 'your' 'turn' | 'over' 'to' 'you' | 'and' 'you' | "
     "'how' 'about' 'you' | 'what' 'about' 'you' | 'hello' 'there' | 'hi' 'there'",
     "set chat phrases, read as one interjection", -0.01)

# ---- tag questions ----------------------------------------------------------------------------------------------
rule("TagQ -> 'right' | 'yeah' | 'huh' | 'eh' | 'no' | 'ok' | 'okay' | 'or' 'not' | 'or' 'what' | 'you' 'know' | "
     "'am' 'i' 'right' | 'yes' | 'innit' | 'lol' 'right'", "a tag asking for agreement (..., right?)")
rule("TagQ -> BeP Neg PrIt^ | BeP Neg Pr2^ | BeP Neg PrS^ | BeD Neg PrIt^ | Do Neg Pr2^ | Dz Neg PrS^ | Dz Neg PrIt^ | "
     "Dd Neg Pr2^ | Md Neg Pr2^ | Hv Neg Pr2^ | BeP PrIt^ | BeP Pr2^ | Do Pr2^ | Dz PrIt^",
     "an auxiliary and a pronoun (isnt it, dont you, can you)", -0.05)

# ---- fragments and the message ----------------------------------------------------------------------------------
rule("Frag -> S^ | Sq^ | Sw^", "a statement or a question")
rule("Frag -> Simp^", "a command", -0.15)
rule("Frag -> IjP^", "an interjection or a set phrase", -0.1)
rule("Frag -> NP^", "a noun phrase alone (pizza, my cat, you)", -0.45)
rule("Frag -> AdjP^", "a describing phrase alone (so tired, nice)", -0.55)
rule("Frag -> AdvP^", "an adverb alone (not really, tonight)", -0.5)
rule("Frag -> PP^", "a preposition phrase alone (at work, from ohio)", -0.6)
rule("Frag -> VPg^ | VPto^", "an -ing or to-phrase alone (just chilling, to sleep)", -0.65)
rule("Frag -> VPn^ | VPd^", "a participle or past phrase alone (done, finished it)", -1.0)
rule("Frag -> Sbar^ | WhCl^", "a clause under a conjunction alone (because i was bored)", -0.65)
rule("Frag -> TagQ^", "a tag alone (right?)", -0.5)
rule("Frag -> Dm^ | Cc^ | Neg^ | Sub^", "a filler or a joining word alone (so, and, not, but)", -0.6)
rule("Frag -> X^", "a word read as nothing in particular (the last resort)")
rule("Msg -> Frag^", "a message: one fragment")
rule("Msg -> Msg^ Frag", "a message: another fragment after the first (lol yeah i do; hi how are you)", -0.6)

# ---- what the network reads ------------------------------------------------------------------------------------
gcat("copy", "NP AdjP VPb VPg VPto", "a phrase a register may copy (what the user likes, hates, fears)")
gcat("phrase", "PP AdvP VPz VPd VPn Pred VPfin WhNP WhAdvP IjP TagQ PossP ThanP NPt",
     "a phrase whose first word gets g:<phrase>")
gcat("clause", "S Sq Sw Simp", "a main clause: its roles give the message's G: features")
gcat("subclause", "Sbar Rel WhCl", "a clause inside another: G:sub_<clause>")

# ---- a copied phrase, said back --------------------------------------------------------------------------------
reflect({"i": "you", "me": "you", "my": "your", "mine": "yours", "myself": "yourself", "am": "are", "we": "you",
         "us": "you", "our": "your", "ours": "yours", "ourselves": "yourselves", "you": "i", "you:obj": "me",
         "your": "my", "yours": "mine", "yourself": "myself", "yourselves": "ourselves", "im": "youre"},
        "a phrase copied from the user is said from the other side: 'my job' -> 'your job'")
