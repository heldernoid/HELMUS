"""Question types: the shape of a question, whatever its subject. With the vocabulary's themes (U:theme_<topic>, from
gen/topics.py) they let a reply answer a question no pattern was written for: "what kind of soup do you make" is a
'what is your / what kind do you' question about food, and Josh can answer it from what he eats. Replies keyed on a
theme and a question type are the last resort before a fallback (josh_themes_*.py), scoring below every specific entry."""
from gen.dsl import intent, unit

intent("qt_like", ["do you like|love|enjoy|prefer|hate|mind", "are you into", "^ you into", "are you a fan of", "you a fan of",
                   "are you big on", "how do you feel about", "what do you think of|about", "thoughts on", "is * good"],
       "asks whether Josh likes something",
       yes=["do you like soup", "are you into hiking", "you a fan of jazz", "how do you feel about tea", "thoughts on sushi"],
       no=["i like soup", "you like me lol", "what do you like to do"], unless=["ask_hobby"])
intent("qt_have", ["do you have|own", "have you got", "^ you got", "do you got", "got any", "^ any @food|@pet|@family|@game"],
       "asks whether Josh has something",
       yes=["do you have a bike", "have you got a dog", "you got siblings", "got any plans"],
       no=["i have a bike", "you have to try it", "do you have to go"], unless=["F:w:to"])
intent("qt_ever", ["have you ever", "^ [have] you ever", "did you ever", "^ ever", "you ever been|tried|seen|had|done|played"],
       "asks whether Josh has ever done something",
       yes=["have you ever broken a bone", "you ever tried sushi", "ever been to europe", "did you ever play soccer"],
       no=["i have never", "best day ever", "whatever"])
intent("qt_what_your", ["what is your", "what are your", "what kind|type|sort of * do|did|would you", "which * do you",
                        "what * do you", "what is * go to", "what is your go to", "who is your", "how is your", "tell me about your"],
       "asks what Josh's something is (his kind, his usual, his go-to)",
       yes=["what kind of soup do you make", "whats your go to sneakers", "which music do you like", "tell me about your car"],
       no=["what is that", "what kind of question is that", "whats up"])
intent("qt_do_you", ["^ [and|so|but] do|did|can|could|would|will|are|were you", "^ you play|do|go|watch|cook|read|drive|know|use|get|make"],
       "a yes/no question about what Josh does",
       yes=["do you cook", "can you swim", "you play any instruments", "would you go skydiving", "did you go out last night"],
       no=["you are funny", "do it", "i can swim"])
unit("user_tells", {"S:any": 1.0, "F:c:me": 1.0, "U:question": -1.0}, "the user tells something about themselves (not a question)",
     bias=-1.0)
