"""Short answers, and where exactly. Shared by every persona.

A person who asks "where r u from" reads the next message, however short, as the answer: "mozambique" is a place,
not a keyboard smash. short_answer fires on a message of a word or two; the memory answered_where (gen/memory.py:
the persona asked where the user is from, last turn) says how to read it, and the place is copied into user_place.
Then "where is it?" is about that place (ask_where_thing, with the memory user_place_fresh).

ask_where_detail: "where in ohio?", "what part?", "whereabouts": the persona's area, not just its state.
"""
from gen.dsl import check, intent, register_when

intent("only_laugh", ["^ @laugh $", "^ @laugh @laugh $"], "a message that is only laughter (lol, lmao lol)",
       yes=["lol", "lmao lol"], no=["london lol", "lol yes"])
intent("short_answer",
       ["^ {ans} $", "^ {ans:content} {x:content} $", "^ {ans} @laugh $", "^ {ans} what about you $", "^ {ans} how about you $", "^ {ans} you $",
        "^ in {ans} $", "^ from {ans} $", "^ {ans} lol $", "^ {ans} haha $"],
       "a message of a word or two: read in the light of what the persona just asked",
       yes=["mozambique", "texas lol", "london wbu", "in paris", "mozambique u?"],
       no=["where are you from", "i am from ohio and you", "what do you mean by that"],
       unless=["greet", "only_laugh", "ack", "yes", "no", "thanks", "bye", "how_are_you", "insult", "accuse_bot",
               "compliment", "yes_no_answer"])
register_when("user_place", "short_answer", "ans", "M:answered_where",
              "a short answer to 'where r u from': where the user is from", phrase=True)
intent("short_name", ["^ {nm:t:Np} $", "^ {nm:unknown} $", "^ {nm:t:Np} @laugh $", "^ it is {nm:t:Np} $",
                      "^ i am {nm:t:Np} $", "^ {nm:t:Np} what about you $", "^ {nm:t:Np} you $"],
       "a bare name (sam, its jess): an answer when the persona just asked or said a name",
       yes=["sam", "its jess", "mike lol", "priya wbu"], no=["weird", "cool", "lol", "nice name"],
       unless=["greet", "only_laugh", "ack", "yes", "no", "thanks", "bye", "insult", "compliment"])
register_when("user_name", "short_name", "nm", "M:answered_name", "a bare name right after names came up: the user's")
intent("short_age", ["^ {age:#num} $", "^ {age:#num} @laugh $", "^ {age:#num} what about you $", "^ {age:#num} you $",
                     "^ {age:#num} years old $", "^ i am {age:#num} $", "^ like {age:#num} $"],
       "a bare age (19, 25 lol): an answer when the persona just asked or said its age",
       yes=["19", "25 lol", "21 wbu", "like 30"], no=["19 dogs", "what is 19 plus 2"])
register_when("st_user_age", "short_age", "age", "M:answered_age", "a bare age right after ages came up: the user's")
check("user_same_age", "st_user_age", "age", "is the user the persona's age ('19' to a 19-year-old: same)")
intent("yes_no_answer", ["^ [@laugh] @yes|@no [@laugh] $", "^ sometimes|kinda|occasionally|rarely|barely $",
                         "^ not really $", "^ yes and no $", "^ a little $", "^ i do $", "^ i am $", "^ i do not $",
                         "^ i am not $"],
       "a bare yes or no (or sometimes, kinda): an answer to a yes/no question just asked",
       yes=["yes", "nah", "yeah lol", "sometimes", "not really", "i do"], no=["yes i am from ohio", "no idea"])
check("user_same_place", "user_place", "city state place area grew_up",
      "is the user from the persona's own place ('ohio' to someone from ohio: same!)")

intent("ask_where_detail",
       ["where in {place}", "what|which part|city|town|area|side|neighborhood", "where exactly", "where about",
        "where in the state"],
       "asks where exactly the persona lives (where in ohio?, what part?)",
       yes=["where in ohio?", "what part of ohio", "what part", "which city", "where exactly", "what neighborhood",
            "what town are you in"],
       no=["where are you from", "where in the world is that", "what part of the game"],
       unless=["F:w:world", "F:w:game", "F:w:movie", "F:w:show", "F:w:book", "F:w:song"])

intent("ask_where_thing",
       ["where is it", "where is that", "where is that at", "where even is that", "where is it at",
        "do you know where * is", "you know where * is", "where is {x} $", "is that in"],
       "asks where something is (a place the user just named: 'where is it?')",
       yes=["where is it", "do you know where mozambique is", "do you know where is mozambique?",
            "where is that even", "where even is that"],
       no=["where are you", "where is your house", "where is the bathroom lol"])
