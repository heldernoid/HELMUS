"""Claims about the persona, and asking for another one. Shared by every persona: the facts a claim is checked against
are named by the keys every persona table has (place, age, job, pet, name, school, games).

A claim is the interrogator telling the persona something about itself, often to test it: "you said you were from
texas", "you are 19 right?", "so you have a dog?", "wait you work at walmart?". A person confirms or corrects from
their own life ("no, ohio lol"); a bot that forgot agrees with anything. The claimed phrase is copied into a register
and checked against the persona's facts (dsl.check: C:<claim> if it agrees, C:<claim>_no if not); the persona's
phrasebook answers each.
"""
from gen.dsl import check, check_stop, intent, register

intent("claim_from",
       ["you are|were from {place}", "you live|lived in {place}", "you grew up in {place}", "are you from {place}",
        "do you live in {place}", "you said * from {place}", "you are|were based in {place}",
        "you are|were born in {place}", "were you born in {place}"],
       "says or checks where the persona is from (you said you were from texas, are you from ohio)",
       yes=["you said you were from texas", "you are from ohio right", "are you from canada", "u live in ohio?",
            "didnt you say you were from florida", "you grew up in columbus right?", "wait you live in new york",
            "are you from around here originally?"],
       no=["where are you from", "i am from ohio", "where do you live"])
register("claim_place", "claim_from", "place", "the place the user says the persona is from", phrase=True)
check("from", "claim_place", "city state place area grew_up", "is the claimed place one of the persona's")

intent("claim_age",
       ["you are|were {age:#num}", "are you {age:#num}", "you said you were {age:#num}",
        "you are {age:#num} years old", "you are like {age:#num}", "you turned {age:#num}"],
       "says or checks the persona's age (you are 19 right, didnt you say you were 25)",
       yes=["you are 19 right", "are you 25", "you said you were 21", "wait you are 30?", "didnt you say you were 19"],
       no=["how old are you", "i am 19", "you are a bot"])
register("claim_age", "claim_age", "age", "the age the user says the persona is")
check("age", "claim_age", "age", "is the claimed age the persona's")

intent("claim_job",
       ["you work at|for|in {job}", "do you work at|for|in {job}", "you said you work at|for|in {job}",
        "you worked at|for {job}", "you work as a|an {job}"],
       "says or checks where the persona works (wait you work at walmart?)",
       yes=["you work at walmart right", "do you work at a grocery store", "wait you work for amazon?",
            "you said you work at target"],
       no=["where do you work", "i work at walmart", "do you work"])
register("claim_job", "claim_job", "job", "the job the user says the persona has", phrase=True)
check("job", "claim_job", "job job_short job_detail", "is the claimed workplace the persona's")

intent("claim_pet",
       ["you have a|an {pet:@pet}", "do you have a|an {pet:@pet}", "you got a|an {pet:@pet}", "you said * a {pet:@pet}",
        "your {pet:@pet}", "you own a|an {pet:@pet}"],
       "says or checks the persona's pet (so you have a dog?)",
       yes=["so you have a dog?", "do you have a cat", "you said you had a dog", "wait you got a cat?",
            "hows your dog"],
       no=["do you have any pets", "i have a dog", "what pet do you have"])
register("claim_pet", "claim_pet", "pet", "the pet the user says the persona has")
check("pet", "claim_pet", "pet pet_detail", "is the claimed pet the persona's")

intent("claim_name",
       ["your name is {name}", "is your name {name}", "your name was {name}", "you are called {name}",
        "you said your name was|is {name}"],
       "says or checks the persona's name (your name is mike right)",
       yes=["your name is mike right", "is your name josh", "you said your name was tom", "wait your name is jake?"],
       no=["what is your name", "my name is sam", "is your name real", "is your name fake"],
       unless=["F:w:real", "F:w:fake", "F:w:actually"])
register("claim_name", "claim_name", "name", "the name the user says the persona has")
check("name", "claim_name", "name full_name", "is the claimed name the persona's")

intent("claim_school",
       ["you go to {school}", "do you go to {school}", "you study {school}", "you are studying {school}",
        "you said you go to {school}", "you are|were at {school} college|university|uni"],
       "says or checks the persona's school or subject (you go to ohio state right)",
       yes=["you go to ohio state right", "do you go to harvard", "you study biology?", "you said you go to osu"],
       no=["where do you go to school", "i go to ohio state", "do you go to school", "do you go to college"],
       unless=["F:w:where", "F:w:school", "F:w:college", "F:w:class", "F:w:work", "F:w:bed", "F:w:sleep"])
register("claim_school", "claim_school", "school", "the school or subject the user says the persona has", phrase=True)
check("school", "claim_school", "school school_type studies major", "is the claimed school or subject the persona's")

intent("claim_game",
       ["you play {game}", "do you play {game}", "you said you play {game}", "you like playing {game}"],
       "says or checks a game the persona plays (you play fortnite right)",
       yes=["you play fortnite right", "do you play minecraft", "you said you play league"],
       no=["what games do you play", "i play fortnite", "do you play games", "do you play any sports"],
       unless=["F:w:games", "F:w:any", "F:w:anything", "F:w:sports", "F:w:instruments", "F:w:what", "F:w:outside"])
register("claim_game", "claim_game", "game", "the game the user says the persona plays", phrase=True)
check("game", "claim_game", "games game old_game", "is the claimed game one the persona plays")

check_stop("a an the my your his her its at in on of from to for pet pets animal animals place city town state "
           "country old years year yrs around here there some any one right originally actually really",
           "words that say nothing against the persona's facts ('a', 'around here', 'right')")

# ---- another one ----------------------------------------------------------------------------------------------------
intent("ask_another",
       ["anything else $", "what else $", "something else $", "anything more $", "^ another $", "another one",
        "one more $", "give me another", "tell me another", "^ more $", "any more|others $", "any other ones",
        "^ and $", "is that all", "^ that is it $", "name another", "^ next $"],
       "asks for another one of what was just said (anything else?, another one)",
       yes=["anything else?", "that's right; anything else?", "another one", "what else", "give me another",
            "any others?", "is that all?", "one more"],
       no=["what else do you do", "i want another pizza", "anything else is fine", "something else happened"])
