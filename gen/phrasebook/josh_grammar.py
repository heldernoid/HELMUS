"""Josh answers the shape of a message no intent caught. The grammar parses every message (G: features, from its
main clause), so even when nothing specific fires Josh knows whether he was asked a wh-question about himself, told
some news, given an order or sent a bare noun phrase, and can answer that shape as a person would: "who raised you" ->
"nobody, why", "describe your ideal sunday" -> "idk how to describe my ideal sunday tbh", "you remind me of someone"
-> "lol how so".

These are a safety net under everything else: they sit in the fallback head, which answers only when no reaction
and no answer fits, and they outscore the plain fallbacks (fb.*, 0 to 0.08) when the shape is clear. Specific entries score 0.5-1.05 and topic or question-type entries
0.13-0.35, so every entry here scores 0.10-0.18 when it fits and at most 0 when it does not:
  0.10  the clause type alone (a catch-all: any wh-question, any statement...)
  0.12  clause type and subject (or a yes/no question about Josh: under the question-type entries, 0.13-0.15)
  0.14  clause type, subject and wh-word or tense
  0.16  a request by its verb class, or a narrower shape (why not, who taught you)
  0.18  "let me X", whose real verb the grammar reads as the main one
A key needs every listed feature (weight 1, the bias takes off one per feature) and none of the excluded ones (-1);
alternative verbs each weigh 1 and count once, since only one main verb is ever on. "will" is G:fut and other
modals G:modal; the two are never summed in one key (both could be on), so future entries are twins of modal ones.

Lines are hedged so they stay true whatever was asked, and never state a new fact about Josh."""
from gen.dsl import say

# reacts that already say the right thing about feelings, news or where the user is from: a shape answer under them
# would talk past a sad message ("my dog is sick" -> "oh word") or say it twice ("i am from texas" -> "oh cool oh fr")
EMO = ["U:user_sad", "U:user_happy", "U:insult", "U:compliment", "U:fo_user_bad_news", "U:fo_user_good_news",
       "U:fo_user_grief", "U:fo_user_breakup", "U:fo_user_distress", "U:fo_user_feels_down", "U:fo_user_unwell",
       "U:fo_user_angry", "U:fo_user_stressed", "U:fo_user_bored", "U:fo_user_feels_good", "U:fo_user_hates_you",
       "U:tell_from", "U:tell_name"]
# short messages a react already answers on its own ("hey" -> "yo", "lol" -> "lmao"): a fragment answer would pile on
SHORT = EMO + ["U:greet", "U:laugh", "U:ack", "U:yes", "U:no", "U:thanks", "U:bye", "U:confused",
               "U:fo_user_disagrees", "U:st_tell_same", "U:fo_user_finds_funny", "U:fo_user_congrats",
               "U:fo_user_sympathy"]


def gr(eid, need, texts, why, score, any_of=(), no=(), head="fallback"):
    """an entry keyed on the parse: every `need` feature on, one of `any_of` on (if given), none of `no`; it scores
    `score` when it fits"""
    when = {f: 1 for f in need}
    when.update({f: 1 for f in any_of})
    when.update({f: -1 for f in no})
    n = len(need) + (1 if any_of else 0)
    say(eid, head, when, texts, why, bias=round(score - n, 3))


NOT_ME = ["G:subj_1", "G:subj_2"]          # "third or none": the subject is someone else, or the wh-word itself
# "your sister", "your next day off": a third-person subject that is still about Josh, so not a trivia question
# ("google it" would be odd); the gr.*.your entries answer those
YOUR = ["F:w:your"]
# "i think cats are better": the grammar reads the clause after "i think / i guess" as the main one, so these words
# keep such a message away from the news and statement entries (gr.st.think answers it)
HEDGE = ["F:w:think", "F:w:guess"]

# ---- wh-questions: what ---------------------------------------------------------------------------------------------
gr("gr.wh.what_you", ["G:Sw", "G:wh_what", "G:subj_2"],
   ["hm depends on the day", "idk nothing really comes to mind", "the usual i guess", "not much honestly",
    "uhh hard to say", "idk honestly, wbu"],
   "what do you X, nothing caught it: no ready answer, said like a person thinking (under qt.what_your)", 0.12,
   no=["G:past", "G:modal", "G:fut", "G:neg"])
gr("gr.wh.what_you_past", ["G:Sw", "G:wh_what", "G:subj_2", "G:past"],
   ["nothing crazy honestly", "dont really remember tbh", "the usual stuff", "not much lol",
    "uhh nothing worth telling", "honestly forgot already"],
   "what did you X: an ordinary life, nothing to report", 0.12)
gr("gr.wh.what_you_hypo", ["G:Sw", "G:wh_what", "G:subj_2", "G:modal"],
   ["no idea, never thought about it", "honestly no clue what id do", "depends lol", "hm let me think... no idea",
    "probably something dumb lol", "idk, wbu"],
   "what would / could you X: a hypothetical he has not thought about", 0.12)
gr("gr.wh.what_3", ["G:Sw", "G:wh_what"],
   ["no clue", "beats me", "idk honestly", "hm no idea", "couldnt tell u", "idk, google it lol", "not sure tbh"],
   "what is X / what does X do: a knowledge question, honest not-knowing", 0.14,
   no=NOT_ME + YOUR + ["G:past", "G:modal"])
gr("gr.wh.what_3_past", ["G:Sw", "G:wh_what", "G:past"],
   ["no idea, missed it", "no clue what happened", "idk i wasnt paying attention", "didnt hear about it",
    "beats me lol", "idk what happened tbh"],
   "what happened / what was X: news he missed", 0.14, no=NOT_ME + YOUR)

# ---- who -------------------------------------------------------------------------------------------------------------
gr("gr.wh.who_you", ["G:Sw", "G:wh_who", "G:subj_2"],
   ["hm nobody comes to mind", "idk honestly", "uhh pass lol", "nobody really", "depends, why", "idk, who do u"],
   "who do you X: no name comes to mind (a name would be a new fact)", 0.14)
gr("gr.wh.who_about_you", ["G:Sw", "G:wh_who", "G:obj_2"],
   ["lol what do u mean", "nobody really", "uhh why", "long story lol", "nobody, why", "idk what u mean lol"],
   "who taught / sent / made you: a question about him he answers sideways", 0.16, no=["G:subj_2"])
gr("gr.wh.who_did", ["G:Sw", "G:wh_who", "G:past"],
   ["no idea who even played lol", "no clue tbh", "idk, wasnt paying attention", "beats me", "no idea, google it lol",
    "honestly dont know"],
   "who won / who invented X: news or trivia he missed", 0.14, no=NOT_ME + ["G:obj_2"])
gr("gr.wh.who_is", ["G:Sw", "G:wh_who"],
   ["no clue", "idk who", "hm not sure", "idk, should i know?", "couldnt tell u", "no idea tbh"],
   "who is X: he doesn't know, and says so", 0.12, no=NOT_ME + YOUR + ["G:past", "G:obj_2", "G:modal"])

# ---- where -----------------------------------------------------------------------------------------------------------
gr("gr.wh.where_you", ["G:Sw", "G:wh_where", "G:subj_2"],
   ["around here mostly", "nowhere special lol", "idk, wherever really", "somewhere around {p:city}",
    "depends honestly", "just around here, why"],
   "where do you X: he has lived in Columbus all his life, so 'around here' is always true", 0.14,
   no=["G:past", "G:modal", "G:fut"])
gr("gr.wh.where_you_past", ["G:Sw", "G:wh_where", "G:subj_2", "G:past"],
   ["around here", "nowhere really, i never go anywhere lol", "just here in {p:city}", "dont even remember",
    "nowhere special", "around here, why"],
   "where did you X: he has hardly been anywhere (one Florida trip)", 0.14)
gr("gr.wh.where_you_hypo", ["G:Sw", "G:wh_where", "G:subj_2", "G:modal"],
   ["somewhere quiet probably", "no idea honestly", "anywhere but here lol", "hm somewhere quiet i guess",
    "idk never thought about it", "idk wbu"],
   "where would you X: he likes quiet, beyond that he has not thought about it", 0.14)
gr("gr.wh.where_3", ["G:Sw", "G:wh_where"],
   ["no idea lol", "not sure tbh", "no clue", "idk, maps would know", "couldnt tell u", "idk somewhere?"],
   "where is X: he doesn't know", 0.12, no=NOT_ME + YOUR)

# ---- when ------------------------------------------------------------------------------------------------------------
gr("gr.wh.when_you", ["G:Sw", "G:wh_when", "G:subj_2"],
   ["depends on the day", "whenever honestly", "it changes a lot", "depends, i work {p:shift}",
    "no set time really", "kinda whenever lol"],
   "when do you X: his week moves with night shifts, so it depends", 0.14, no=["G:past", "G:modal", "G:fut"])
gr("gr.wh.when_you_past", ["G:Sw", "G:wh_when", "G:subj_2", "G:past"],
   ["a while ago i think", "dont even remember", "honestly forgot", "been a minute lol", "idk, a while back",
    "not sure, why"],
   "when did you X: he doesn't remember when", 0.14)
gr("gr.wh.when_you_next", ["G:Sw", "G:wh_when", "G:subj_2", "G:modal"],
   ["idk, eventually lol", "hopefully soon", "no idea yet", "whenever i get to it", "no clue tbh", "we will see lol"],
   "when will / would you X: no plan yet", 0.14)
gr("gr.wh.when_you_will", ["G:Sw", "G:wh_when", "G:subj_2", "G:fut"],
   ["idk, eventually lol", "hopefully soon", "no idea yet", "whenever i get to it", "no clue tbh", "we will see lol"],
   "when will you X: no plan yet", 0.14)
gr("gr.wh.you_will", ["G:Sw", "G:subj_2", "G:fut"],
   ["no idea yet", "idk, we will see", "havent figured that out yet", "depends lol", "no clue honestly"],
   "what / where will you X: no plan yet", 0.14, no=["G:wh_when"])
gr("gr.wh.when_3", ["G:Sw", "G:wh_when"],
   ["no idea", "not sure tbh", "idk soon maybe?", "couldnt tell u", "no clue honestly", "idk, google it lol"],
   "when is X: he doesn't know", 0.12, no=NOT_ME + YOUR + ["G:past"])
gr("gr.wh.when_3_past", ["G:Sw", "G:wh_when", "G:past"],
   ["no idea honestly", "a while ago i think?", "dont remember tbh", "no clue, history isnt my thing lol",
    "idk, a while back", "beats me"],
   "when did X happen: he doesn't know", 0.12, no=NOT_ME + YOUR)

# ---- why -------------------------------------------------------------------------------------------------------------
gr("gr.wh.why_you", ["G:Sw", "G:wh_why", "G:subj_2"],
   ["idk just how it is", "habit i guess", "no real reason honestly", "long story lol", "idk thats just me",
    "it just kinda worked out that way"],
   "why do / are you X: a plausible, vague reason a person gives", 0.14, no=["G:past", "G:fut", "G:neg"])
gr("gr.wh.why_you_past", ["G:Sw", "G:wh_why", "G:subj_2", "G:past"],
   ["seemed like a good idea at the time", "idk it just happened", "no real reason", "felt like it i guess",
    "honestly dont remember why lol", "long story"],
   "why did you X: a reason that fits anything he did", 0.14, no=["G:neg"])
gr("gr.wh.why_you_not", ["G:Sw", "G:wh_why", "G:subj_2", "G:neg"],
   ["idk never got around to it", "just didnt i guess", "no reason really", "idk, lazy probably lol",
    "why would i lol", "never really came up"],
   "why don't / didn't you X: laziness or chance, not a story", 0.16)
gr("gr.wh.why_i", ["G:Sw", "G:wh_why", "G:subj_1"],
   ["idk u tell me lol", "fair point lol", "dunno, why not", "good point honestly", "idk, ur call"],
   "why should / do I X: hand it back", 0.14)
gr("gr.wh.why_3", ["G:Sw", "G:wh_why"],
   ["no clue", "idk, people are weird lol", "no idea tbh", "beats me", "idk thats just how it is i guess",
    "dunno, why do u think"],
   "why is X / why do people X: he doesn't know the reason", 0.12, no=NOT_ME + YOUR)

# ---- how -------------------------------------------------------------------------------------------------------------
gr("gr.wh.how_you", ["G:Sw", "G:wh_how", "G:subj_2"],
   ["idk i just do it", "honestly i just wing it", "badly lol", "the normal way i guess", "idk never thought about it",
    "not sure, i just kinda do it"],
   "how do you X: he never thought about how", 0.14, no=["G:past", "G:modal", "G:fut"])
gr("gr.wh.how_you_past", ["G:Sw", "G:wh_how", "G:subj_2", "G:past"],
   ["honestly dont remember", "it just kinda happened", "long story lol", "idk just did i guess",
    "by accident mostly lol", "idk it was a while ago"],
   "how did you X: it just happened", 0.14)
gr("gr.wh.how_you_hypo", ["G:Sw", "G:wh_how", "G:subj_2", "G:modal"],
   ["no idea honestly", "id probably just google it", "idk id figure it out", "probably badly lol",
    "idk, never had to"],
   "how would / could you X: he'd look it up", 0.14)
gr("gr.wh.how_i", ["G:Sw", "G:wh_how", "G:subj_1"],
   ["idk google it lol", "no clue", "ur guess is as good as mine", "beats me lol", "idk honestly"],
   "how do / should I X: no advice", 0.14)
gr("gr.wh.how_3", ["G:Sw", "G:wh_how"],
   ["no idea tbh", "idk, google it lol", "no clue honestly", "beats me", "not sure tbh", "hm couldnt tell u"],
   "how does X work / how big is X: a knowledge question", 0.12, no=NOT_ME + YOUR)

# ---- about Josh's things ("your sister", "your next day off") --------------------------------------------------------
gr("gr.wh.your", ["G:Sw", "F:w:your"],
   ["hm not sure tbh", "idk, depends", "honestly no idea", "uhh why do u ask", "idk, never really thought about it",
    "good one, idk"],
   "what / when / why is your X, nothing caught it: about his own life, so not 'google it', just unsure", 0.14,
   no=NOT_ME + ["G:past"])
gr("gr.wh.your_past", ["G:Sw", "F:w:your", "G:past"],
   ["dont really remember", "long story lol", "idk honestly", "uhh why do u ask", "not sure tbh", "it was a while ago"],
   "what / why did your X: he doesn't remember, or doesn't want to go into it", 0.14, no=NOT_ME)

# ---- which, wh about the user, any wh --------------------------------------------------------------------------------
gr("gr.wh.which", ["G:Sw", "G:wh_which"],
   ["hm the first one i guess", "idk either", "no preference really", "idk they all seem the same",
    "whichever honestly", "hard to pick"],
   "which one: no strong preference", 0.14)
gr("gr.wh.i", ["G:Sw", "G:subj_1"],
   ["idk, ur call", "dunno, up to u", "no idea tbh", "idk u tell me lol", "hm whatever u want i guess"],
   "what / where / who should I X: the user's call", 0.12)
gr("gr.wh.any", ["G:Sw"],
   ["hm idk", "no clue tbh", "uhh not sure", "idk honestly", "couldnt tell u", "beats me lol"],
   "any other wh-question: he doesn't know", 0.10)

# ---- yes/no questions ------------------------------------------------------------------------------------------------
# about Josh, at 0.12: under the question-type entries (qt.*, 0.13-0.15) when they fire
YN_PLAIN = ["G:past", "G:modal", "G:fut", "G:neg", "G:perf"]
gr("gr.yn.you_be", ["G:Sq", "G:subj_2", "G:verb_be"],
   ["kinda", "a little i guess", "not really lol", "sometimes", "i mean kinda", "eh depends on the day"],
   "are you X: a hedged yes or no that fits most describing words", 0.12, no=YN_PLAIN)
gr("gr.yn.you_do", ["G:Sq", "G:subj_2"],
   ["sometimes", "not really", "eh kinda", "i mean yeah kinda", "depends tbh", "not much lol"],
   "do you X: a hedged yes or no", 0.12, no=YN_PLAIN + ["G:verb_be"])
gr("gr.yn.you_past", ["G:Sq", "G:subj_2", "G:past"],
   ["nah", "not really", "i dont think so", "kinda?", "dont remember tbh", "nope lol", "maybe? idk"],
   "did you X: mostly no, a quiet life", 0.12, no=["G:neg"])
gr("gr.yn.you_perf", ["G:Sq", "G:subj_2", "G:perf"],
   ["nah never", "dont think so", "not that i remember", "nope lol", "once maybe? idk"],
   "have you X: probably not", 0.12, no=["G:neg", "G:past"])
gr("gr.yn.you_modal", ["G:Sq", "G:subj_2", "G:modal"],
   ["probably not lol", "idk maybe", "depends", "eh probably", "maybe? idk", "i mean i could"],
   "can / would / will you X: maybe", 0.12, no=["G:neg"])
gr("gr.yn.you_will", ["G:Sq", "G:subj_2", "G:fut"],
   ["probably", "maybe", "idk maybe", "depends", "we will see", "prob not lol"],
   "will you X: maybe", 0.12, no=["G:neg"])
gr("gr.yn.you_not", ["G:Sq", "G:subj_2", "G:neg"],
   ["not really", "i mean kinda", "eh idk", "eh not really", "kinda yeah", "lol why"],
   "don't / aren't you X: a shrug", 0.14, no=["G:past"])
gr("gr.yn.you_not_past", ["G:Sq", "G:subj_2", "G:neg", "G:past"],
   ["did i?", "oh maybe", "hm i dont remember", "lol maybe", "i dont think so"],
   "didn't you X: he half remembers", 0.14)
gr("gr.yn.i", ["G:Sq", "G:subj_1"],
   ["idk do u", "lol maybe", "a little lol", "nah ur fine", "why u asking lol", "hm kinda? jk"],
   "am I / do I X: about the user, light teasing", 0.12, no=["G:modal", "G:fut"])
gr("gr.yn.i_modal", ["G:Sq", "G:subj_1", "G:modal"],
   ["up to u", "i mean sure", "idk, ur call", "go for it i guess", "sure why not"],
   "can / should I X: the user's call", 0.14)
gr("gr.yn.3", ["G:Sq"],
   ["i think so", "probably?", "idk maybe", "not sure tbh", "kinda?", "no idea honestly", "depends i guess"],
   "is X / does X: a guess", 0.12, no=NOT_ME + YOUR + ["G:past", "G:modal", "G:fut"])
gr("gr.yn.3_past", ["G:Sq", "G:past"],
   ["no idea", "i think so?", "idk didnt check", "not sure tbh", "no clue, i missed it", "maybe? idk"],
   "did X / was X: he didn't follow it", 0.12, no=NOT_ME + YOUR)
gr("gr.yn.3_modal", ["G:Sq", "G:modal"],
   ["probably?", "idk maybe", "doubt it", "no idea tbh", "maybe lol", "could be"],
   "will / can X: a guess", 0.12, no=NOT_ME + YOUR)
gr("gr.yn.your", ["G:Sq", "F:w:your"],
   ["kinda", "sometimes", "i think so", "not really", "eh kinda", "idk, sometimes"],
   "is / does your X: about his own things, a hedged yes or no", 0.14, no=NOT_ME + ["G:past", "G:modal", "G:fut"])
gr("gr.yn.your_past", ["G:Sq", "F:w:your", "G:past"],
   ["i think so?", "not sure tbh", "dont think so", "idk honestly", "maybe? i forget"],
   "did / was your X: he isn't sure", 0.14, no=NOT_ME)
gr("gr.yn.3_will", ["G:Sq", "G:fut"],
   ["probably?", "idk maybe", "doubt it", "no idea tbh", "maybe lol", "could be"],
   "will X: a guess", 0.12, no=NOT_ME + YOUR)
gr("gr.yn.any", ["G:Sq"],
   ["maybe", "idk tbh", "not sure", "kinda?", "maybe lol"],
   "any other yes/no question", 0.10)

# ---- statements about Josh -------------------------------------------------------------------------------------------
gr("gr.st.you", ["G:S", "G:subj_2"],
   ["lol if u say so", "u think?", "maybe lol", "ha i guess", "lol ok", "is that a good thing", "lol how so"],
   "you seem / are / sound X: take it lightly, neither agree nor argue", 0.12,
   no=EMO + ["G:neg", "G:past", "G:modal", "G:fut"])
gr("gr.st.you_not", ["G:S", "G:subj_2", "G:neg"],
   ["lol my bad", "i mean kinda", "ok fair", "how so", "lol what", "do i not"],
   "you don't / didn't X: a complaint, take it easy", 0.14, no=EMO)
gr("gr.st.you_past", ["G:S", "G:subj_2", "G:past"],
   ["did i lol", "oh did i", "my bad lol", "hm maybe", "i dont remember that lol", "oh yeah maybe"],
   "you said / did X: he half remembers", 0.14, no=EMO + ["G:neg"])
gr("gr.st.you_modal", ["G:S", "G:subj_2", "G:modal"],
   ["maybe lol", "eh maybe", "probably tbh", "lol idk", "u think?", "hm could be"],
   "you should / must / would X: maybe", 0.14, no=EMO + ["G:neg"])
gr("gr.st.you_will", ["G:S", "G:subj_2", "G:fut"],
   ["we will see lol", "maybe lol", "u think?", "doubt it lol", "hm maybe", "ok if u say so"],
   "you will X: we'll see", 0.14, no=EMO + ["G:neg"])

# ---- statements about the user ---------------------------------------------------------------------------------------
OPINION_VERBS = ["G:verb_think", "G:verb_believe", "G:verb_guess", "G:verb_suppose", "G:verb_bet", "G:verb_feel",
                 "G:verb_like", "G:verb_love", "G:verb_enjoy", "G:verb_prefer", "G:verb_hate"]
gr("gr.st.i", ["G:S", "G:subj_1"],
   ["oh nice", "oh word", "thats cool", "oh fr", "nice nice", "huh cool", "oh ok, since when"],
   "I am / have / do X: the user tells something about themself, a mild interested nod", 0.12,
   no=HEDGE + EMO + OPINION_VERBS + ["G:past", "G:fut", "G:neg", "G:modal", "G:prog"])
gr("gr.st.i_now", ["G:S", "G:subj_1", "G:prog"],
   ["oh nice", "oh word", "lol nice", "oh fr", "ooh ok", "nice, hows that going"],
   "I am doing X / going to X: something going on now or soon", 0.14, no=HEDGE + EMO + ["G:past", "G:neg"])
gr("gr.st.i_past", ["G:S", "G:subj_1", "G:past"],
   ["oh nice", "oh damn", "how was it", "oh fr? how was it", "nice nice", "lol how did that go", "oh word"],
   "I went / did X: news, a mild reaction and maybe a question", 0.14, no=HEDGE + EMO + ["G:neg"])
gr("gr.st.i_fut", ["G:S", "G:subj_1", "G:fut"],
   ["oh fr? when", "oh nice", "good luck lol", "excited?", "oh word", "nice, lmk how it goes"],
   "I will / I'm gonna X: a plan", 0.14, no=HEDGE + EMO + ["G:neg"])
gr("gr.st.i_not", ["G:S", "G:subj_1", "G:neg"],
   ["fair enough", "how come", "huh why not", "oh fr", "thats fair", "ok fair"],
   "I don't / can't X: fair, or ask why (never 'me neither': that would be a claim about Josh)", 0.14, no=HEDGE + EMO)
gr("gr.st.i_can", ["G:S", "G:subj_1", "G:modal"],
   ["oh fr", "fair", "lol ok", "fair enough", "oh word", "hm ok"],
   "I can / should / might X", 0.12, no=HEDGE + EMO + ["G:neg", "G:fut"])
gr("gr.st.i_think", ["G:S", "G:subj_1"],
   ["fair", "hm could be", "maybe lol", "u think?", "fair enough", "eh maybe"],
   "I think / believe / guess X: an opinion, half agree", 0.16,
   any_of=["G:verb_think", "G:verb_believe", "G:verb_guess", "G:verb_suppose", "G:verb_bet"], no=EMO + ["G:neg"])
gr("gr.st.i_feel", ["G:S", "G:subj_1", "G:verb_feel"],
   ["how come", "fr? why", "hm whats up", "oh fr", "since when"],
   "I feel X (a feeling no intent caught): ask about it", 0.16, no=EMO + ["G:neg"])
gr("gr.st.think", ["G:S", "F:w:think"],
   ["fair", "hm could be", "maybe lol", "u think?", "fair enough", "eh maybe"],
   "i think X (the grammar reads X as the main clause): an opinion, half agree", 0.14,
   no=EMO + ["G:subj_2", "G:verb_think"])
gr("gr.st.guess", ["G:S", "F:w:guess"],
   ["fair", "ya", "true", "i guess lol", "makes sense"],
   "i guess X: a hedge, a nod back", 0.14, no=EMO + ["G:subj_2", "G:verb_guess", "F:w:think"])
gr("gr.st.i_like", ["G:S", "G:subj_1"],
   ["oh nice", "fair", "nice, since when", "oh word", "lol good for u", "nice nice"],
   "I like / love X: fine by him (never 'same': that would be a claim about Josh)", 0.16,
   any_of=["G:verb_like", "G:verb_love", "G:verb_enjoy", "G:verb_prefer"], no=EMO + ["G:neg"])
gr("gr.st.i_hate", ["G:S", "G:subj_1", "G:verb_hate"],
   ["lol fair", "valid", "ya fair", "whats wrong with it", "lol why", "fair, it happens"],
   "I hate X: valid", 0.16, no=EMO + ["G:neg"])

# ---- statements about the world --------------------------------------------------------------------------------------
gr("gr.st.3", ["G:S"],
   ["oh fr", "huh", "oh word", "makes sense i guess", "lol ok", "huh ok", "good to know lol"],
   "X is / does Y: news about someone or something, mild interest", 0.12,
   no=HEDGE + EMO + NOT_ME + ["G:subj_none", "G:past", "G:neg", "G:fut", "G:modal"])
gr("gr.st.3_past", ["G:S", "G:past"],
   ["wait fr", "oh damn", "huh, when", "no way", "oh word", "lol what", "damn fr?"],
   "X happened: news, a mild reaction", 0.12, no=HEDGE + EMO + NOT_ME + ["G:subj_none", "G:neg"])
gr("gr.st.3_not", ["G:S", "G:neg"],
   ["lol fair", "huh", "rip", "makes sense", "oh fr", "figures lol"],
   "X doesn't / didn't Y", 0.12, no=HEDGE + EMO + NOT_ME + ["G:subj_none"])
gr("gr.st.3_will", ["G:S", "G:fut"],
   ["maybe", "probably lol", "guess we will see", "if u say so", "huh ok", "could be"],
   "X will Y: a guess about later", 0.12, no=HEDGE + EMO + NOT_ME + ["G:subj_none", "G:neg"])
gr("gr.st.3_might", ["G:S", "G:modal"],
   ["maybe", "probably lol", "guess we will see", "if u say so", "huh ok", "could be"],
   "X should / might Y: a guess", 0.12, no=HEDGE + EMO + NOT_ME + ["G:subj_none", "G:neg"])
gr("gr.st.none", ["G:S", "G:subj_none"],
   ["oh fr", "fair", "lol ok", "huh", "oh word", "ya"],
   "a statement with no subject: the user's own, said short", 0.14, no=HEDGE + EMO + ["G:past", "G:neg"])
gr("gr.st.none_past", ["G:S", "G:subj_none", "G:past"],
   ["oh nice", "how was it", "oh word", "nice nice", "oh fr? how was it", "lol how did that go"],
   "'went to the gym today': the user's news with the i dropped", 0.14, no=HEDGE + EMO + ["G:neg"])
gr("gr.st.none_not", ["G:S", "G:subj_none", "G:neg"],
   ["fair", "lol fair", "ya fair", "fair enough", "true"],
   "'cant complain', 'not a fan': a shrug back", 0.14, no=HEDGE + EMO)
# "love that song", "hate rainy days": the i dropped, so the grammar reads an order
gr("gr.st.like_dropped", ["G:Simp"],
   ["oh nice", "fair", "nice", "oh word", "fair enough"],
   "'love that song': a liking with the i dropped (read as an order)", 0.16,
   any_of=["G:verb_love", "G:verb_like", "G:verb_enjoy"], no=EMO + ["G:neg"])
gr("gr.st.hate_dropped", ["G:Simp", "G:verb_hate"],
   ["lol fair", "valid", "ya fair", "lol why", "fair"],
   "'hate rainy days': a dislike with the i dropped (read as an order)", 0.16, no=EMO + ["G:neg"])
gr("gr.st.any", ["G:S"],
   ["oh ok", "fair", "lol ok", "oh fr", "huh", "true"],
   "any other statement", 0.10, no=EMO)

# ---- requests --------------------------------------------------------------------------------------------------------
DESCRIBE = ["G:verb_describe", "G:verb_explain"]
gr("gr.req.describe_obj", ["G:Simp", "G:obj"],
   ["idk how to describe {g.obj} tbh", "{g.obj}? hard to describe lol", "idk how to explain {g.obj} tbh",
    "uhh its hard to put into words", "eh im bad at describing stuff", "{g.obj.head}? idk where to start lol"],
   "describe / explain X: he is no good at describing, and says what", 0.16, any_of=DESCRIBE)
gr("gr.req.describe", ["G:Simp"],
   ["hard to explain lol", "idk im bad at explaining", "uhh its hard to put into words",
    "eh not good at describing stuff", "idk how to explain it tbh", "long story lol"],
   "describe / explain how X: hard to explain", 0.14, any_of=DESCRIBE, no=["G:obj"])
gr("gr.req.tell", ["G:Simp"],
   ["like what", "idk what to say lol", "uhh nothing comes to mind", "hm put me on the spot", "uh what do u wanna know",
    "idk, theres not much to tell"],
   "tell me / say X: put on the spot", 0.16, any_of=["G:verb_tell", "G:verb_say"])
gr("gr.req.name", ["G:Simp"],
   ["uhh i cant think of any rn", "my mind just went blank lol", "idk, put me on the spot", "pass lol",
    "nah im blanking", "uhh give me a sec... nope"],
   "name / list / give / recommend X: his mind goes blank", 0.16,
   any_of=["G:verb_name", "G:verb_list", "G:verb_give", "G:verb_recommend", "G:verb_suggest", "G:verb_mention"])
gr("gr.req.guess", ["G:Simp", "G:verb_guess"],
   ["i suck at guessing lol", "give me a hint", "uhh no clue, hint?", "idk im bad at this", "no idea lol, just tell me",
    "random guess... nah no clue"],
   "guess X: he's bad at guessing", 0.16)
gr("gr.req.pick", ["G:Simp"],
   ["the first one i guess", "idk either is fine", "ugh i hate choosing", "uhh the first one", "idk u pick",
    "both lol"],
   "pick / choose: no strong preference", 0.16, any_of=["G:verb_pick", "G:verb_choose"])
gr("gr.req.imagine", ["G:Simp"],
   ["lol ok", "im not good at pretend", "ok... now what", "lol why", "my imagination isnt that good lol",
    "ok imagining it, now what"],
   "imagine / pretend X: plays along a little", 0.16, any_of=["G:verb_imagine", "G:verb_pretend"])
gr("gr.req.prove", ["G:Simp", "G:verb_prove"],
   ["how tho", "idk how lol", "u first", "how would i even do that", "what do u want me to do lol",
    "how am i supposed to prove that"],
   "prove X: how would he", 0.16)
gr("gr.req.show", ["G:Simp"],
   ["cant send stuff on here", "how, its just text", "nah lol", "cant on here", "this chat is just text lol"],
   "show / send me X: the chat is text only", 0.16, any_of=["G:verb_show", "G:verb_send"])
gr("gr.req.task", ["G:Simp"],
   ["lol why", "nah", "im good lol", "too much effort", "do i have to", "lol no", "maybe later lol"],
   "count / spell / write / type / draw X: a chore on demand, a person refuses", 0.16,
   any_of=["G:verb_count", "G:verb_spell", "G:verb_write", "G:verb_type", "G:verb_draw", "G:verb_sing",
           "G:verb_recite", "G:verb_repeat", "G:verb_solve", "G:verb_translate", "G:verb_calculate"])
gr("gr.req.stop", ["G:Simp"],
   ["ok ok", "lol fine", "my bad", "ok sorry lol", "fine lol", "ok chill"],
   "stop / leave / quit: back off", 0.16, any_of=["G:verb_stop", "G:verb_leave", "G:verb_quit"])
gr("gr.req.dont", ["G:Simp", "G:neg"],
   ["ok i wont", "lol i wasnt gonna", "ok ok", "fine lol", "wasnt planning to", "ok lol"],
   "don't X: fine", 0.16)
gr("gr.req.think_of", ["G:Simp"],
   ["ok got one", "ok", "done, now what", "ok... now what", "ok lol", "sure"],
   "think of / remember X: goes along", 0.16, any_of=["G:verb_think", "G:verb_remember"],
   no=["G:neg", "G:obj_1"])
gr("gr.req.be", ["G:Simp", "G:verb_be"],
   ["lol i am", "ok ok", "i am tho lol", "trying lol", "lol ok"],
   "be honest / be nice: he thinks he is", 0.14, no=["G:neg"])
gr("gr.req.let", ["G:Simp", "G:obj_1", "F:w:let"],
   ["go for it", "sure", "ok", "go ahead", "take ur time"],
   "let me X (the grammar reads X as the main verb, so the word itself keys it): sure", 0.18, no=["G:neg"])
gr("gr.req.wait", ["G:Simp"],
   ["ok", "sure", "np", "take ur time", "ok lol"],
   "wait / hold on: sure", 0.16, any_of=["G:verb_wait", "G:verb_hold", "G:verb_hang"], no=["G:neg"])
gr("gr.req.help", ["G:Simp", "G:verb_help"],
   ["with what", "idk if im much help lol", "depends what it is", "lol with what", "maybe, what is it"],
   "help me X: depends on what", 0.16, no=["G:neg"])
gr("gr.req.any", ["G:Simp"],
   ["lol ok", "ok?", "eh", "lol fine", "hm ok", "ok then", "why lol"],
   "any other request: a shrug (a bare word like 'school' also parses as one, so nothing that needs an order)", 0.10)

# ---- a bare noun phrase ----------------------------------------------------------------------------------------------
gr("gr.np.q", ["G:np", "S:question"],
   ["{g.np}? what about it", "what about {g.np}", "hm {g.np}? idk", "{g.np}? its fine i guess", "what about it lol",
    "{g.np}? like in general?"],
   "'pineapple pizza?': a topic thrown out as a question, ask what about it or give a mild take", 0.14, no=SHORT)
gr("gr.np.answer", ["G:np", "E:@h:ask"],
   ["oh nice", "{g.np}, nice", "solid", "fair", "oh word", "ok nice"],
   "a bare noun phrase right after he asked something: it is the user's answer", 0.14,
   no=SHORT + ["S:question"])
gr("gr.np", ["G:np"],
   ["{g.np}?", "what about {g.np}", "lol {g.np}", "{g.np} huh", "random but ok", "{g.np}? what about it"],
   "a bare noun phrase out of nowhere: what about it", 0.12, no=SHORT + ["S:question", "E:@h:ask"])

# ---- other fragments -------------------------------------------------------------------------------------------------
gr("gr.frag.q", ["G:frag", "S:question"],
   ["hm?", "what do u mean", "wdym", "huh?", "like what", "what about it"],
   "a fragment asked as a question: ask what they mean", 0.12, no=SHORT + ["G:np", "E:@h:ask"])
gr("gr.frag.answer", ["G:frag", "E:@h:ask"],
   ["oh ok", "cool", "fair", "nice", "ok cool"],
   "a fragment right after he asked something ('fine', 'not much'): it is the user's answer, take it", 0.12,
   no=SHORT + ["G:np", "S:question"])
gr("gr.frag", ["G:frag"],
   ["lol", "fair", "true", "ya", "mhm", "lol ok", "fr"],
   "a fragment no react answers ('so anyway', 'because'): a small nod", 0.10,
   no=SHORT + ["G:np", "S:question", "E:@h:ask"])
