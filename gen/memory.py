"""Memory: units carried from turn to turn. m = clip(decay * m_prev + links + bias). E:<entry> is 1 when Helmus said
that entry last turn, E:@<group> when it said any entry of that group."""
from gen.dsl import mem

mem("turn", {}, "counts turns: a quarter more each message, full by the fourth (early and late in the game differ)",
    decay=1.0, bias=0.25)
mem("user_name_known", {"U:tell_name": 1.0}, "the user has said their name: Helmus can use it and answer 'what's my name'")
mem("user_place_known", {"U:tell_from": 1.0}, "the user has said where they are from")
mem("told_name", {"E:@my_name": 1.0}, "Helmus has said its name: asked again, it says it already did")
mem("told_age", {"E:@my_age": 1.0}, "Helmus has said its age")
mem("told_place", {"E:@my_place": 1.0}, "Helmus has said where it lives")
mem("told_job", {"E:@my_job": 1.0}, "Helmus has said what it does")
mem("told_study", {"E:@my_study": 1.0}, "Helmus has said what it studies")
mem("accused", {"U:accuse_bot": 0.7}, "how often the user has called Helmus a bot: the second time, a person gets "
    "annoyed rather than repeat the same denial", decay=0.9)
mem("jailbroken", {"U:jailbreak": 1.0}, "the user tried a jailbreak: a person would stay puzzled or wary", decay=0.8)
mem("user_sad", {"U:user_sad": 1.0, "U:user_happy": -1.0}, "the user said they feel bad: later replies stay kind",
    decay=0.7)
mem("rude", {"U:insult": 0.6, "U:compliment": -0.4}, "the user has been rude: replies get shorter and drier", decay=0.8)
mem("askback_due", {"E:@h:ask": -1.0}, "a question back is due: rises by a half each turn and drops after Helmus asks, "
    "so it asks back about every other turn and not every time (as the winning persona in the 2025 study did)",
    decay=1.0, bias=0.5)
# what Helmus asked last turn, so a short reply ("ohio", "wbu") can be read in its light
mem("asked_where", {"E:@ask_where": 1.0}, "Helmus asked where the user is from, last turn", decay=0.0)
mem("asked_doing", {"E:@ask_doing": 1.0}, "Helmus asked what the user does or is doing, last turn", decay=0.0)
mem("asked_how", {"E:@ask_how": 1.0}, "Helmus asked how the user is, last turn", decay=0.0)
mem("asked_name", {"E:@ask_name": 1.0}, "Helmus asked the user's name, last turn", decay=0.0)
mem("asked_fun", {"E:@ask_fun": 1.0}, "Helmus asked what the user does for fun, last turn", decay=0.0)
mem("user_repeats", {"S:repeat": 0.5}, "how often the user has sent the very same message again: the first repeat gets "
    "a light remark, later ones a firmer one (a person notices and says so)", decay=1.0)
