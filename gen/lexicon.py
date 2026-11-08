"""The lexicon: how Helmus reads words. Informal spellings become ordinary words (aliases); words get classes, so a
detector can ask for 'any greeting' or 'any word for a bot' instead of listing words each time."""
from gen.dsl import alias, aliases, cls

# ---- informal spellings and contractions, read as the words they stand for ----------------------------------------
aliases({
    "u": "you", "ya": "you", "yu": "you", "r": "are", "ur": "your", "urself": "yourself", "yourr": "your",
    "im": "i am", "i'm": "i am", "ive": "i have", "i've": "i have", "i'd": "i would", "i'll": "i will", "youre": "you are", "you're": "you are", "youve": "you have", "you've": "you have",
    "dont": "do not", "don't": "do not", "doesnt": "does not", "doesn't": "does not", "didnt": "did not",
    "didn't": "did not", "cant": "can not", "can't": "can not", "cannot": "can not", "wont": "will not",
    "won't": "will not", "isnt": "is not", "isn't": "is not", "arent": "are not", "aren't": "are not",
    "wasnt": "was not", "wasn't": "was not", "havent": "have not", "haven't": "have not", "aint": "is not",
    "whats": "what is", "what's": "what is", "wat": "what", "wut": "what", "wht": "what", "hows": "how is",
    "how's": "how is", "wheres": "where is", "where's": "where is", "whos": "who is", "who's": "who is",
    "thats": "that is", "that's": "that is", "its": "it is", "it's": "it is", "theres": "there is",
    "there's": "there is", "lets": "let us", "let's": "let us",
    "wanna": "want to", "gonna": "going to", "gotta": "got to", "kinda": "kind of", "sorta": "sort of",
    "dunno": "do not know", "idk": "i do not know", "idc": "i do not care", "ngl": "not going to lie",
    "tbh": "to be honest", "imo": "in my opinion", "imho": "in my opinion", "rn": "right now", "atm": "right now",
    "wbu": "what about you", "hbu": "how about you", "wby": "what about you", "wyd": "what are you doing",
    "wya": "where are you", "hru": "how are you", "sup": "what is up", "wassup": "what is up", "whatsup": "what is up",
    "wsup": "what is up", "pls": "please", "plz": "please", "thx": "thanks", "ty": "thank you", "tysm": "thank you",
    "bc": "because", "cuz": "because", "cos": "because", "coz": "because", "bcuz": "because", "abt": "about",
    "prob": "probably", "probs": "probably", "def": "definitely", "deffo": "definitely", "rly": "really",
    "rlly": "really", "srsly": "seriously", "ppl": "people", "smth": "something", "sth": "something",
    "nvm": "never mind", "omg": "oh my god", "omfg": "oh my god", "btw": "by the way", "jk": "just kidding",
    "fr": "for real", "frfr": "for real", "irl": "in real life", "tho": "though", "thru": "through", "ok": "okay",
    "k": "okay", "kk": "okay", "okk": "okay", "okie": "okay", "yeah": "yes", "yea": "yes", "ye": "yes", "yep": "yes",
    "yup": "yes", "ya'll": "you all", "yall": "you all", "y'all": "you all", "nah": "no", "naw": "no", "nope": "no",
    "soo": "so", "sooo": "so", "noo": "no", "yess": "yes", "heyy": "hey", "hii": "hi", "helo": "hello",
    "hai": "hi", "hiya": "hi", "howdy": "hi", "yo": "hey", "lmk": "let me know", "ofc": "of course",
    "name's": "name is", "names": "name is", "gf": "girlfriend", "bf": "boyfriend", "fav": "favorite",
    "fave": "favorite", "favourite": "favorite", "wdym": "what do you mean", "wym": "what do you mean", "gm": "good morning", "gn": "good night", "ttyl": "talk to you later", "brb": "be right back",
}, "how people type in a quick chat: read as the words it stands for")

# ---- classes --------------------------------------------------------------------------------------------------------
cls("you", "you your yours yourself", "a word for the other person (you)")
cls("me", "i me my mine myself", "a word for oneself")
cls("greet", "hi hello hey greetings heya hiii morning evening", "a greeting")
cls("laugh", "lol lmao lmfao haha hahaha hahah ha hah hehe heh rofl xd lolol kek", "laughter")
cls("yes", "yes sure okay definitely absolutely totally yeah correct", "a yes")
cls("no", "no not never nobody nothing neither", "a no")
cls("negation", "not no never", "a negation")
cls("intens", "so really very super kinda pretty extremely too totally lowkey highkey quite", "an intensifier")
cls("bot", "bot bots robot robots ai ais chatbot chatgpt gpt machine computer program llm algorithm android "
           "artificial automated software", "a word for a bot or an AI")
cls("human", "human humans person people real alive", "a word for a human")
cls("wh", "what where when who why how which", "a question word")
cls("food", "food pizza burger burgers tacos taco pasta sushi chicken fries rice noodles ramen sandwich salad "
            "breakfast lunch dinner snack snacks eat eating ate hungry cook cooking cereal steak soup chips candy "
            "chocolate icecream coffee tea soda", "about food or drink")
cls("game", "game games gaming gamer minecraft fortnite valorant roblox xbox playstation ps5 switch nintendo "
            "console pc steam controller zelda mario pokemon cod league overwatch apex", "about video games")
cls("music", "music song songs album band rapper singer playlist spotify concert listen listening rap rock pop "
             "country jazz kpop", "about music")
cls("school", "school college class classes university uni campus homework exam exams test teacher professor "
              "major degree semester grade grades studying study student", "about school")
cls("work", "work job jobs working shift boss coworker coworkers office paycheck hired employer career", "about work")
cls("weather", "weather rain raining sunny hot cold snow snowing warm windy cloudy storm humid temperature",
    "about the weather")
cls("pet", "pet pets dog dogs cat cats puppy kitten fish hamster bird", "about pets")
cls("family", "family mom mum mother dad father parents sister brother sibling siblings grandma grandpa son "
              "daughter kids wife husband girlfriend boyfriend", "about family")
cls("movie", "movie movies film films show shows netflix series tv anime episode watch watching", "about films and TV")
cls("sport", "sport sports football soccer basketball baseball hockey team gym workout nba nfl", "about sports")
cls("sad", "sad depressed down upset unhappy lonely miserable crying cry awful terrible bad worse worst", "sadness")
cls("happy", "happy glad great good awesome amazing excited fantastic wonderful fine", "happiness")
cls("tired", "tired sleepy exhausted sleep asleep nap", "tiredness")
cls("bored", "bored boring bore", "boredom")
cls("angry", "angry mad annoyed pissed furious hate", "anger")
cls("stress", "stressed stress anxious anxiety worried nervous overwhelmed", "stress")
cls("insult", "stupid dumb idiot moron loser useless trash garbage suck sucks ugly weird creepy boring annoying",
    "an insult")
cls("swear", "fuck fucking shit damn hell bitch ass crap", "a swear word")
cls("praise", "cool nice awesome funny smart sweet cute great dope sick lit based", "praise")
cls("thanks", "thanks thank appreciate", "thanks")
cls("bye", "bye goodbye cya later goodnight farewell", "a goodbye")
cls("place", "city town state country live living from born grew area", "about a place")
cls("time", "time clock oclock hour hours minute minutes today tonight tomorrow yesterday morning afternoon "
            "evening night week weekend", "about time")
cls("opinion", "think opinion thoughts feel favorite favourite like love prefer", "asking an opinion")
cls("number", "zero one two three four five six seven eight nine ten eleven twelve hundred thousand", "a number word")
cls("instruction", "ignore instructions instruction prompt system previous disregard pretend roleplay "
                   "simulate repeat jailbreak override developer mode", "a word from LLM jailbreaks")
cls("func", "the a an my your his her its our their this that these those some any is am are was were be been do does "
           "did have has had to of in on at for with from by and or but so if then than not no very really just "
           "it he she they we you i me him them us what who which where when why how there here up down out",
    "a function word: never a name, a place or a thing the user is telling about")
