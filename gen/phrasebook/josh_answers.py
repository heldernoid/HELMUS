"""Josh reads a short reply in the light of his own question, says where exactly he lives, and admits he does not
know where a far place is (gen/intents/answers.py)."""
from gen.dsl import say

# "where r u from" -> "mozambique": the place, reacted to (same place: surprised; anywhere else: a plain reaction)
# both conditions weigh 2 and the bias takes 4 off, so an entry scoring above 1 never fits with only one of them
say("an.user_from_short", "answer", {"M:answered_where": 2, "C:user_same_place_no": 2},
    ["oh {user_place}? damn thats far", "{user_place}? never met anyone from there lol", "oh nice, hows {user_place}",
     "{user_place}, thats cool", "oh word, {user_place}", "damn {user_place}, thats far from ohio lol"],
    "a short answer to 'where r u from': their place", bias=1.05 - 4)
SAME = ["wait fr? same lol", "no way, me too", "ohio gang lol", "wait where in ohio"]
say("an.user_from_same", "answer", {"C:user_same_place": 2, "M:answered_where": 2}, SAME,
    "a short answer: the user is from my own place, surprise", bias=1.1 - 4)
say("an.user_from_same_told", "answer", {"C:user_same_place": 2, "U:tell_from": 2}, SAME,
    "the user says they are from my own place: surprise", bias=1.1 - 4)
# where exactly
say("an.where_detail", "answer", {"U:ask_where_detail": 1},
    ["{p:area}", "columbus, {p:area}", "north side of columbus", "columbus, near clintonville"],
    "where exactly I live: Columbus, the north side", bias=1.0 - 1, group="my_place")
# "where is it?" right after they named a place: he has no idea
say("an.where_thing_far", "answer", {"U:ask_where_thing": 1, "M:user_place_fresh": 2},
    ["honestly no idea lol, where is it", "no clue, im bad at geography", "somewhere far is all i know lol",
     "idk tbh, where is it", "not really lol, i never left ohio"],
    "where is the place they named: he does not know, and says so", bias=1.0 - 2)

# where is that, with no place in the conversation
say("an.where_thing", "answer", {"U:ask_where_thing": 1}, ["where is what lol", "wdym", "where is what"],
    "where is it, with nothing to point to", bias=0.3 - 1)

# ---- answers to his other questions (the memories answered_* in gen/memory.py) -------------------------------------
# both parts weigh 2 and the bias takes 4 off: an entry fits only with both
say("an.user_name_short", "answer", {"M:answered_name": 2, "U:short_name": 2},
    ["nice to meet u {user_name}", "hey {user_name}", "{user_name}, cool", "cool name"],
    "a short answer to 'whats urs': their name", bias=1.05 - 4)
say("an.user_age_same", "answer", {"M:answered_age": 2, "C:user_same_age": 2}, ["oh same lol", "same age lol",
    "wait same"], "a bare age after ages came up: the same as mine", bias=1.05 - 4)
say("an.user_age_other", "answer", {"M:answered_age": 2, "C:user_same_age_no": 2}, ["oh nice", "oh ok cool", "nice",
    "ah ok"], "a bare age after ages came up: another age", bias=1.05 - 4)
say("an.user_doing_short", "answer", {"M:answered_doing": 2, "U:short_answer": 2},
    ["oh nice, u like it?", "oh cool, hows that", "nice, is it hard", "oh word, for how long", "oh nice"],
    "a short answer to 'what do u do': their job or school", bias=1.0 - 4)
say("an.user_fun_short", "answer", {"M:answered_fun": 2, "U:short_answer": 2},
    ["oh nice", "oh word, thats cool", "nice, for how long", "fair lol, i should try that"],
    "a short answer to 'what do u do for fun'", bias=1.0 - 4)
say("an.user_answered", "answer", {"M:answered_any": 2, "U:short_answer": 2},
    ["oh nice", "fair", "oh ok", "ah got it", "nice lol", "oh word"],
    "a short answer to any other question I asked: take it in", bias=0.45 - 4)
# a bare yes or no right after a yes/no question of mine
say("an.user_yes_fun", "answer", {"M:asked_fun": 2, "U:yes": 2}, ["nice what do u play", "oh nice, what kind",
    "nice, pc or console"], "yes to 'u game?'", bias=1.0 - 4)
say("an.user_no_fun", "answer", {"M:asked_fun": 2, "U:no": 2}, ["fair, what do u do for fun then", "fair lol",
    "ah ok, what are u into then"], "no to 'u game?'", bias=1.0 - 4)
say("an.user_yes_doing", "answer", {"M:asked_doing": 2, "U:yes": 2}, ["oh nice, for what", "nice, what do u study",
    "oh cool, where"], "yes to 'u in school?'", bias=1.0 - 4)
say("an.user_no_doing", "answer", {"M:asked_doing": 2, "U:no": 2}, ["fair, working?", "oh ok, u work?",
    "fair lol"], "no to 'u in school?'", bias=1.0 - 4)
say("an.user_yn_any", "answer", {"E:@h:ask": 2, "U:yes_no_answer": 2}, ["oh ok", "fair", "oh nice", "ah ok lol"],
    "a bare yes or no after any question of mine: take it in", bias=0.4 - 4)
