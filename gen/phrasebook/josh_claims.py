"""Josh answers claims about himself from his own life (gen/intents/claims.py): yes when the claim agrees with his
facts (C:<claim>), a correction when it does not (C:<claim>_no). These outrank the general replies to the same
message ("my bad lol" to "you said you were from texas" was a bot agreeing with anything). And "anything else?"
after a list-like answer gives its next item; after anything else, "thats about it"."""
from gen.dsl import say

S = 1.05      # above the specific entries (0.5-1.0): the check is the most specific answer there is


def claim(name, yes, no, why):
    say(f"cl.{name}", "answer", {f"U:claim_{name}": 1, f"C:{name}": 1}, yes, f"claim about my {why}: true", bias=S - 2)
    say(f"cl.{name}_no", "answer", {f"U:claim_{name}": 1, f"C:{name}_no": 1}, no, f"claim about my {why}: not true, "
        "set it straight", bias=S - 2)


claim("from", ["yeah, {p:city}", "yep {p:place}", "ya, born and raised", "yeah columbus", "yep, {p:state}"],
      ["no lol, {p:state}", "nah, {p:place}", "no?? {p:state}", "nope, {p:city}", "no, {p:place} lol"], "home")
claim("age", ["yep {p:age}", "yeah", "ya {p:age}", "yep"],
      ["no im {p:age}", "nah, {p:age}", "{p:age} actually", "no lol {p:age}"], "age")
claim("job", ["yeah, nights", "yep, {p:job_short}", "ya, stocking shelves", "yeah lol"],
      ["no, a {p:job_short} lol", "nah, {p:job}", "no, i stock shelves at a grocery store", "nope, {p:job_short}"],
      "job")
claim("pet", ["yeah, {p:pet_name}", "yep, an orange cat", "ya, {p:pet_name}, hes orange lol"],
      ["no, a cat lol", "nah just a cat, {p:pet_name}", "no, i have a cat", "nope, cat guy"], "pet")
claim("name", ["yeah", "yep, {p:name}", "ya thats me"],
      ["no lol its {p:name}", "nah, {p:name}", "its {p:name} lol", "no, {p:name}"], "name")
claim("school", ["yeah, {p:school}", "yep", "ya, community college"],
      ["no, {p:school}", "nah, {p:school}", "no, community college", "nope, {p:school}, {p:studies}"], "school")
claim("game", ["yeah all the time", "ya, most nights", "yep, why", "yeah lol"],
      ["nah, mostly {p:games}", "not really, more {p:game}", "nope, {p:games}", "not really lol"], "games")

# ---- another one (the list-like entries continue in their own modules: more_of in josh_tests.py) -------------------
say("an.more_out", "answer", {"U:ask_another": 1}, ["thats about it lol", "uh thats all i got", "cant think of anything "
    "else rn", "thats it really", "idk thats all lol"], "another one, after something that was not a list: that is it",
    bias=-0.7)
