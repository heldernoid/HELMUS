"""Small talk: daily life and personal details, what interrogators do in 61% of the 2025 Turing-test games (Jones &
Bergen). Plans, routine, food, work and school, home, family, pets, car, money, hometown, travel, recent events, the
user telling about themselves, and the short follow-ups ("really?", "since when?", "what kind?") that only make sense
after the last thing said. Every intent is named for what a reply needs to know. Core intents (gen/intents/core.py)
already cover the broad asks (where from, job, family, pets, hobbies): these go one detail deeper and do not redeclare
them. Patterns are written in the expanded form the reader produces ("you", "do not", "what are you doing")."""
from gen.dsl import INTENTS, aliases, cls, compile_pattern, intent, mem, register

# ---- informal spellings of this domain ------------------------------------------------------------------------------
aliases({
    "2nite": "tonight", "2night": "tonight", "tonite": "tonight", "2day": "today",
    "tmrw": "tomorrow", "tmr": "tomorrow", "tmw": "tomorrow", "tmrow": "tomorrow", "2moro": "tomorrow",
    "2morrow": "tomorrow", "tomoz": "tomorrow", "tommorow": "tomorrow", "tomorow": "tomorrow",
    "wknd": "weekend", "wkend": "weekend", "bday": "birthday", "b'day": "birthday", "vacay": "vacation",
    "xmas": "christmas", "brekkie": "breakfast", "brekky": "breakfast", "apt": "apartment", "yrs": "years",
    "doin": "doing", "goin": "going", "nothin": "nothing", "workin": "working", "chillin": "chilling",
    "eatin": "eating", "watchin": "watching", "playin": "playing",
    "whatcha": "what are you", "watcha": "what are you",
    "what'd": "what did", "where'd": "where did", "how'd": "how did", "when'd": "when did",
    "dog's": "dog", "cat's": "cat", "nm": "not much", "nmu": "not much you",
    "whereabouts": "where", "neighbour": "neighbor", "neighbours": "neighbors", "neighbourhood": "neighborhood",
    "flavour": "flavor", "flavours": "flavors",
}, "how people type small talk in a quick chat: read as the words it stands for")

# ---- word classes of this domain ------------------------------------------------------------------------------------
cls("st_holiday", "thanksgiving christmas halloween easter holidays holiday hanukkah diwali vacation break summer",
    "a holiday or a break from school or work")
cls("st_meal", "breakfast lunch dinner brunch supper", "a meal of the day")
cls("st_sibling", "sibling siblings brother brothers sister sisters bro sis sibs twin stepbrother stepsister",
    "a brother or a sister")
cls("st_parent", "mom mum mother dad father parents parent mommy daddy folks stepmom stepdad mama", "a parent")
cls("st_partner", "girlfriend boyfriend partner wife husband fiance fiancee bae", "a romantic partner")
cls("st_animal", "pet pets dog dogs cat cats puppy puppies kitten kittens kitty doggo pup bunny rabbit hamster fish "
                 "bird parrot lizard snake turtle ferret gecko", "a pet animal")
cls("st_roommate", "roommate roommates roomie roomies housemate housemates flatmate flatmates", "a roommate")
cls("st_dwelling", "house apartment flat dorm condo trailer townhouse duplex", "a kind of home")
cls("st_school", "school college uni university class classes campus", "a school or its classes")
cls("st_hw", "homework exam exams test tests finals midterm midterms quiz quizzes assignment assignments essay "
             "project", "schoolwork or an exam")
cls("st_year", "freshman sophomore junior senior freshmen", "a year of high school or college")
cls("st_spot", "home work school college uni class office library mall store gym party job campus",
    "a place a person can be at right now")
cls("st_inside", "bed room bedroom class car office kitchen basement couch school college", "a place a person can "
    "be in right now")
cls("st_dest", "work school class college campus uni job office", "a place a person commutes to")
cls("st_workv", "work worked working", "a form of the verb work")
cls("st_badadj", "sucks sucked awful terrible rough long stressful exhausting tiring boring annoying brutal "
                 "miserable horrible bad hell", "a complaint word for a day or a job")
cls("st_goodadj", "good great fun easy chill fine nice okay alright decent amazing awesome", "a word for a good "
    "day or a good job")
cls("st_tired", "tired sleepy exhausted drained", "tiredness (without sleep words, so 'did you sleep' is not it)")
cls("st_placeadj", "nice fun boring big small safe pretty cool dangerous expensive cheap quiet busy crowded dead",
    "a word for what a town is like")
cls("st_evaladj", "fun hard good boring easy cool difficult tough bad stressful enjoyable interesting worth",
    "a word for judging an activity")
cls("st_nowverb", "watching playing cooking cleaning reading studying listening scrolling texting gaming chilling "
                  "relaxing laying lying sitting drawing writing walking driving shopping", "an activity going on now")
cls("st_planverb", "going visiting seeing meeting working hanging heading driving flying leaving traveling "
                   "travelling", "a verb of a plan")
cls("st_when", "today tonight tomorrow later weekend", "a time a plan is for")
cls("st_illness", "cold flu headache fever migraine covid stomachache cough", "an illness")
cls("st_nation", "american british english canadian australian irish scottish european mexican", "a nationality")
cls("st_session", "chat game study test experiment conversation session", "this chat or the study")
cls("st_agenum", [str(n) for n in range(10, 100)] + "ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
                 "eighteen nineteen twenty thirty forty fifty sixty seventy".split(), "a number that can be an age")


def _slots(intent_name, slot, patterns, why):
    """extra slot detectors for an intent's register: they are not linked to the intent (it fires from its own,
    tighter patterns, such as 'i am @st_agenum $'), they only mark which word to copy when it does. The DSL has no
    '{slot} of a class', so the class test and the copy live in separate detectors."""
    for i, p in enumerate(patterns):
        d, s = compile_pattern(f"{intent_name}.slot{i}", p, why)
        INTENTS[intent_name]["slots"].setdefault(slot, []).append(d)


def _plans(w):
    """the ways of asking someone's plans for a time `w` (a pattern fragment such as 'tonight' or '* weekend')"""
    return [f"what [are] you doing {w}", f"what are you up to {w}", f"any plans [for] {w}",
            f"you [got|have] [any] plans [for] {w}", f"your plans [for] {w}", f"doing anything [fun|special] {w}",
            f"you going to do {w}", f"what is the plan [for] {w}",
            f"^ [you] got [any] plans [for] {w}", f"^ plans [for] {w}"]


# ==== plans ==========================================================================================================
intent("st_ask_plans_today", _plans("today") + ["what are you doing * rest of [the] day",
                                                "you going to do * rest of [the] day"],
       "asks what Helmus is doing or planning for the rest of today",
       yes=["what are you doing today?", "wyd today", "any plans for today", "u got plans today?",
            "whatcha doing today", "what r ur plans for today", "what are you gonna do for the rest of the day",
            "doing anything fun today?"],
       no=["what did you do today", "i have plans today", "what are you doing tonight", "what are you doing",
           "what did you eat today"])
intent("st_ask_plans_tonight", _plans("tonight|later") + ["you going out tonight|later", "your going out tonight"],
       "asks what Helmus is doing tonight or later",
       yes=["what are you doing tonight?", "wyd tonight", "any plans tonight", "u going out tonight?",
            "whatcha doing later", "got plans for tonight?", "what are you gonna do tonight"],
       no=["i am going out tonight", "what did you do last night", "what are you doing this weekend",
           "what are you doing today", "i have plans tonight"])
intent("st_ask_plans_tomorrow", _plans("tomorrow"),
       "asks what Helmus is doing tomorrow",
       yes=["what are you doing tomorrow?", "wyd tmrw", "any plans for tomorrow", "u got plans tomorrow?",
            "what are you up to tomorrow", "doing anything tomorrow"],
       no=["i have plans tomorrow", "what did you do yesterday", "do you work tomorrow"])
intent("st_ask_plans_weekend", _plans("* weekend") + ["^ [your|any] [big] weekend plans", "your weekend plans",
                                                      "plans for the weekend"],
       "asks what Helmus is doing this weekend",
       yes=["what are you doing this weekend?", "any plans for the weekend", "weekend plans?",
            "wyd this weekend", "u got plans this weekend", "doing anything fun this weekend",
            "what are your plans for the weekend", "whats the plan for the weekend"],
       no=["what did you do last weekend", "how was your weekend", "i have plans this weekend", "i work weekends",
           "what do you do on weekends"])
intent("st_ask_plans_holiday", ["what [are] you doing for [the] @st_holiday", "what [are] you doing this @st_holiday",
                                "plans for [the] @st_holiday", "any @st_holiday plans", "your @st_holiday plans",
                                "you [got|have] [any] plans * @st_holiday", "you going anywhere * @st_holiday",
                                "what do you do for @st_holiday", "how do you celebrate", "you celebrate @st_holiday",
                                "doing anything for [the] @st_holiday", "you going home for [the] @st_holiday",
                                "you excited for @st_holiday", "you going to do for [the] @st_holiday"],
       "asks Helmus's plans for a holiday or a break (Thanksgiving, Christmas, summer, spring break)",
       yes=["what are you doing for thanksgiving?", "any christmas plans", "plans for the holidays?",
            "are you going anywhere for spring break", "how do you celebrate christmas",
            "what are you doing this summer", "u going home for thanksgiving?", "doing anything for xmas"],
       no=["what did you do for halloween", "how was your thanksgiving", "i love christmas",
           "what are you doing this weekend"])
intent("st_ask_plans_after", ["you doing after this|that", "you going to do after this|that", "you do after this",
                              "plans after this", "you doing after [the] @st_session", "you do after [the] @st_session",
                              "what is next for you", "after this what are you"],
       "asks what Helmus will do after this chat or study",
       yes=["what are you doing after this?", "wyd after this", "what r u gonna do after this",
            "any plans after this?", "what will you do after the study", "whats next for you"],
       no=["after this i am going to bed", "what are you doing", "what did you do before this",
           "what are you doing tonight"])
intent("st_ask_before_this", ["you doing before this|that|now", "you do before this", "you up to before [this]",
                              "were you doing earlier", "did you do earlier", "before this what [were|did] you"],
       "asks what Helmus was doing before this chat",
       yes=["what were you doing before this?", "what did u do before this", "what were you up to before this",
            "wyd before this", "what were you doing earlier", "before this what were you doing"],
       no=["what are you doing after this", "what are you doing now", "have you done this before",
           "i was gaming before this"])

# ==== routine: sleep, food, getting around, the day ===================================================================
intent("st_ask_wake_time", ["you [just] wake up", "you [just] woke up", "you [just] waking up",
                            "what time [did|do] you get up", "when [did|do] you get up", "you get up early",
                            "you up early", "you get out of bed"],
       "asks when Helmus woke up or usually gets up",
       yes=["what time did you wake up", "when did u wake up today", "did you just wake up?",
            "what time do you get up for work", "u just woke up?", "are you just waking up lol"],
       no=["i just woke up", "wake up!", "how did you sleep", "what time do you go to bed"])
intent("st_ask_sleep_quality", ["how did you sleep", "!time did you sleep", "you sleep well|good|okay|alright|enough",
                                "how much sleep", "hours of sleep", "you get [any|enough] sleep", "you sleep at all",
                                "you been sleeping", "you sleep last night"],
       "asks how well or how much Helmus slept",
       yes=["how did you sleep?", "did u sleep well", "how much sleep did you get", "did you get any sleep",
            "you sleep ok?", "have you been sleeping enough"],
       no=["i slept well", "what time did you sleep", "i can't sleep", "go to sleep", "when do you go to bed"])
intent("st_ask_bedtime", ["time [do|did] you [usually] go to bed|sleep", "time [do|did] you sleep",
                          "when [do|did] you [usually] go to bed|sleep", "when do you sleep", "how late [do|did] you stay up",
                          "you [usually|always|normally|ever|often] stay up late", "your bedtime", "sleep schedule", "you going to bed|sleep soon"],
       "asks when Helmus goes to bed or how late it stays up",
       yes=["what time do you go to bed?", "when do u usually go to sleep", "how late do you stay up",
            "do you stay up late", "do u normally stay up late", "whats your sleep schedule like", "what time did you go to bed last night",
            "are you going to bed soon"],
       no=["how did you sleep", "i go to bed late", "go to sleep", "what time do you wake up"])
intent("st_ask_morning_person", ["!am !not !good [a] morning person", "!am [a] night owl", "!am [a] night person",
                                 "!am [an] early bird", "morning or night", "you like mornings"],
       "asks whether Helmus is a morning person or a night owl",
       yes=["are you a morning person?", "morning person or night owl?", "r u a night owl", "are you an early bird",
            "night person?", "do you like mornings"],
       no=["i am a morning person", "i'm not a morning person", "good morning person", "this morning",
           "i am a night owl"])
intent("st_ask_ate_today", ["what did you eat", "what you eat today", "what did you have for @st_meal",
                            "what did you have to eat", "did you eat", "have you eaten", "you had @st_meal",
                            "^ had @st_meal", "last thing you ate", "eat anything today", "what was your @st_meal"],
       "asks what Helmus has eaten today (the classic 'what did you have for breakfast')",
       yes=["what did you eat today?", "what did u have for breakfast", "have you eaten yet", "did you eat lunch",
            "what was the last thing you ate", "had breakfast yet?", "wat u eat today"],
       no=["what are you eating", "what is for dinner", "i ate pizza", "what is your favorite food",
           "do you eat meat"])
intent("st_ask_meal_plans", ["what is for @st_meal", "you having for @st_meal", "you going to eat",
                             "you going to have for @st_meal", "you making for @st_meal", "you cooking",
                             "@st_meal plans", "what will you eat", "you getting for @st_meal",
                             "your @st_meal situation|plan|plans", "what is the @st_meal situation|plan"],
       "asks what Helmus will eat next (dinner plans)",
       yes=["what's for dinner?", "what are you having for dinner", "what are you gonna eat",
            "what are u making for lunch", "dinner plans?", "what are you cooking tonight",
            "hows ur lunch plan looking", "what is the dinner situation over there"],
       no=["what did you have for dinner", "what are you eating", "i am having pizza for dinner",
           "do you cook"])
intent("st_ask_eating_now", ["you eating", "you drinking", "you snacking", "you [@intens] hungry", "your eating"],
       "asks whether Helmus is eating or drinking right now, or hungry",
       yes=["what are you eating?", "are you eating rn", "whatcha drinking", "are you hungry", "r u eating",
            "you snacking on something?"],
       no=["what did you eat", "i am eating", "do you like eating", "i am hungry"])
intent("st_ask_cook", ["you cook", "can you cook", "know how to cook", "who cooks", "who does the cooking",
                       "you a good cook", "you like cooking", "you cook for yourself"],
       "asks whether Helmus cooks",
       yes=["do you cook?", "can u cook", "do you know how to cook", "who cooks at your house",
            "are you a good cook", "do you cook for yourself"],
       no=["i cook a lot", "what are you cooking", "i can cook", "my mom cooks"])
intent("st_ask_commute", ["how [do|did] you get to @st_dest", "your commute", "you commute", "how long * commute",
                          "how far is [your] work|school|job|campus", "you drive to", "you walk to", "you bike to",
                          "you take the bus|train|subway|metro", "how do you get around", "you ride the bus"],
       "asks how Helmus gets to work or school, or gets around",
       yes=["how do you get to work?", "how long is ur commute", "do you drive to school", "do u take the bus",
            "how far is work from your place", "how do you get around"],
       no=["i drive to work", "do you have a car", "how do you get to the next level", "where do you work"])
intent("st_ask_daily_routine", ["what is your [typical|normal|average|usual] day like",
                                "typical|normal|average|usual day", "what do you do all day",
                                "what do you do every day|everyday", "what do you [usually] do during the day",
                                "your [daily] routine", "your day * look like", "you [usually] do on [the] weekend|weekends",
                                "you [usually] like to do on [the] weekend|weekends", "your weekends"],
       "asks what Helmus's ordinary day or weekend looks like",
       yes=["what's your day like?", "what is a typical day for you", "what do u do all day",
            "whats ur daily routine", "what does your day usually look like", "what do you do on weekends",
            "what do you usually do on the weekend", "what are your weekends like"],
       no=["how was your day", "how is your day", "what did you do today", "what is today",
           "what did you do last weekend", "i do nothing on weekends"])
intent("st_ask_day_recap", ["how was your day", "how has your day been", "how did your day go", "how was today",
                            "what did you do today", "what have you done today", "what you do today",
                            "did you do anything [fun|cool] today", "do anything [fun|cool] today",
                            "anything * happen today", "your day go"],
       "asks how Helmus's day went so far (past, not plans)",
       yes=["how was your day?", "how has your day been", "what did you do today", "did you do anything fun today",
            "how did your day go", "anything interesting happen today", "how was today"],
       no=["what are you doing today", "how is your day", "how was your weekend", "my day was good"],
       unless=["st_ask_plans_today"])
intent("st_ask_tired", ["are [not] you [@intens] @st_tired", "you sound|seem|look [@intens] @st_tired",
                        "you must be [@intens] @st_tired", "you are [@intens] @st_tired", "your [@intens] @st_tired"],
       "asks whether Helmus is tired",
       yes=["are you tired?", "you sound tired", "r u sleepy", "you must be exhausted", "aren't you tired",
            "you seem tired lol"],
       no=["i am tired", "i'm so sleepy", "did you sleep well", "are you bored"])
intent("st_ask_busy", ["are [not] you [@intens] busy", "you busy", "your busy", "am i bothering you",
                       "you have time to chat|talk"],
       "asks whether Helmus is busy right now",
       yes=["are you busy?", "you busy rn", "r u busy", "are you busy today", "aren't you busy",
            "am i bothering you"],
       no=["i am busy", "are you bored", "busy day", "i have been busy"])
intent("st_ask_vices", ["!what do you drink $", "!what do you drink @laugh $", "you drink alcohol|beer|wine|liquor|booze|much",
                        "you even drink", "old enough to drink", "you get drunk", "been drunk", "you smoke",
                        "you vape", "you get high", "you party", "you smoke weed"],
       "asks whether Helmus drinks, smokes, vapes or parties",
       yes=["do you drink?", "do u smoke", "do you vape", "do you smoke weed lol", "do you drink alcohol",
            "do you party much", "ever been drunk?"],
       no=["do you drink coffee", "i smoke", "what do you drink", "smoke detector"])

# ==== work ===========================================================================================================
intent("st_ask_schedule_today", ["you work today|tomorrow|tonight|later", "you working today|tomorrow|tonight|later",
                                 "you have work today|tomorrow|tonight|later", "you have work $", "you got work",
                                 "your next shift", "^ work today|tomorrow|tonight", "you off today|tomorrow|work",
                                 "you have|got class|classes|school|lecture today|tomorrow|later|tonight",
                                 "you have|got class|classes|school $", "your next class", "is there school"],
       "asks whether Helmus has work or class today, tomorrow or later",
       yes=["do you work today?", "are u working tomorrow", "do you have work later", "when is your next shift",
            "you got work tonight?", "are you off today", "do you have class today?", "do u have school tomorrow",
            "when is your next class"],
       no=["i work today", "i have work tomorrow", "where do you work", "how was work", "i have class tomorrow",
           "what classes are you taking"])
intent("st_ask_shift", ["what shift", "your shifts", "how long [is|are] your shift|shifts", "what are your hours",
                        "your work hours", "how many hours * work", "you work nights|weekends|mornings|evenings|overnight|days",
                        "you work full|part time", "full time or part time", "full or part time", "when do you work",
                        "what days do you work", "what time do you start|finish", "what time do you get off",
                        "what time do you work", "when do you get off"],
       "asks Helmus's work hours and shifts",
       yes=["what shift do you work?", "how many hours do you work a week", "do you work nights",
            "full time or part time?", "what days do u work", "how long are your shifts",
            "what time do you get off work"],
       no=["i work nights", "do you work today", "where do you work", "how was your shift"])
intent("st_ask_boss_coworkers", ["your boss|manager|supervisor|bosses", "your coworkers|coworker|colleagues",
                                 "people you work with", "work friends", "friends at work",
                                 "you like the people at work"],
       "asks about Helmus's boss or coworkers",
       yes=["how is your boss?", "do you like your boss", "is ur manager nice", "what's your boss like",
            "do you like your coworkers", "do you have work friends"],
       no=["my boss is annoying", "you are the boss", "who is the boss", "be your own boss",
           "my coworkers are weird"])
intent("st_ask_like_job", ["you like|love|hate|enjoy your job|work", "you like|love|hate|enjoy working",
                           "!what is your job", "how is work", "how is the job", "how is your job",
                           "how is it at work", "is work good|fun|okay|hard|boring", "you like it at work",
                           "is it a good job"],
       "asks whether Helmus likes its job, or how work is going in general",
       yes=["do you like your job?", "do u like working there", "is your job fun", "how's work",
            "how is the job going", "do you hate your job lol", "do you enjoy your work"],
       no=["what is your job", "i like my job", "how was work today", "do you like your boss"])
intent("st_ask_work_recap", ["how was [your] work|shift|job", "how did [your] work|shift go", "was work",
                             "how was it at work"],
       "asks how Helmus's last shift went",
       yes=["how was work?", "how was your shift", "how was work today", "how did work go",
            "was work busy today", "how did your shift go"],
       no=["how is work", "how was school", "i was at work", "work was long"])
intent("st_ask_job_tenure", ["how long [have] you [been] @st_workv", "how long have you had * job",
                             "when did you start @st_workv|there", "your first job", "how long have you been there"],
       "asks how long Helmus has had its job",
       yes=["how long have you worked there?", "how long u been working there", "how long have you had that job",
            "when did you start working there", "is it your first job", "how long have you worked at the store"],
       no=["i have worked there for a year", "how long is your shift", "how long have you lived there",
           "do you work there"])
intent("st_ask_pay", ["how much do you make|earn", "how much [do] you make|earn", "you make an|per hour",
                      "paid an|per hour", "they pay you", "does it pay [well|good]", "is the pay",
                      "your salary|wage|wages", "how much does it pay", "you make good money"],
       "asks how much Helmus earns",
       yes=["how much do you make?", "how much do u make an hour", "what do they pay you", "is the pay good",
            "whats your salary", "does it pay well"],
       no=["how much are you getting paid for this", "i make 15 an hour", "pay attention", "how much is it"])
intent("st_ask_job_duties", ["what do you do at work|there", "what do you [actually] do there", "what do you [actually] do at work",
                             "what do you do at your job", "your job involve|entail", "what is your job like",
                             "like working there|at", "what kind of work|job", "what do you do all day at work"],
       "asks what Helmus actually does at its job",
       yes=["what do you do at work?", "what do you actually do there", "what does your job involve",
            "what's your job like", "what kind of work do you do", "what is it like working there"],
       no=["what do you do", "what do you do for work", "what is your job", "what do you do for fun"])

# ==== school =========================================================================================================
intent("st_ask_classes", ["what classes|courses|class|subjects|subject", "how many classes|courses",
                          "you taking * classes|courses", "what are you studying", "you majoring in",
                          "favorite class|subject", "best|worst class|subject", "your classes like"],
       "asks what classes or subjects Helmus takes",
       yes=["what classes are you taking?", "how many classes do u have", "what are you studying",
            "what are u majoring in", "whats your favorite subject", "what courses r u taking"],
       no=["i have class later", "i am taking classes", "are you in class right now", "what is your job"])
intent("st_ask_grades", ["your grades|gpa|marks", "you get good grades", "a good student", "good at school",
                         "did you pass", "how did you do on * test|exam|final|finals|midterm|midterms|quiz",
                         "you failing", "straight as"],
       "asks how Helmus does at school (grades, tests)",
       yes=["how are your grades?", "whats your gpa", "are you a good student", "do you get good grades",
            "did you pass", "how did you do on your exam"],
       no=["my grades are bad", "what grade are you in", "pass me the salt", "i passed"])
intent("st_ask_school_year", ["what year are you", "what year of college|school|uni", "what grade [are] you",
                              "are you a|in @st_year", "you graduate|graduating|graduated",
                              "high school or college", "you [still] in high|middle school", "you still in school|college",
                              "how many years left"],
       "asks what year or grade Helmus is in, or when it graduates",
       yes=["what year are you in?", "what grade are you in", "are you a senior", "when do you graduate",
            "are you in high school or college", "did you graduate yet", "r u still in high school"],
       no=["what year is it", "i am a senior", "what year were you born", "i graduated last year"])
intent("st_ask_like_school", ["you like|love|hate|enjoy [your] @st_school", "you like|love|hate|enjoy studying",
                              "how is school|college|uni|class", "how are [your] classes|teachers|professors",
                              "how is your school|college", "is school|college|uni|class hard|fun|easy|boring|good|tough|okay",
                              "your teachers|professors"],
       "asks whether Helmus likes school, or how school is going in general",
       yes=["do you like school?", "how is college", "is school hard", "do u like your classes",
            "how are your professors", "do you hate school lol", "how's uni going"],
       no=["i like school", "how was school today", "where do you go to school", "what classes are you taking"])
intent("st_ask_school_recap", ["how was [your] school|class|classes|college|uni|lecture|exam|test",
                               "how did [your] class|school|exam|test go", "how was [your] day at school|college|uni",
                               "was school|class [@intens] good|fun|okay|boring|long", "did school|class go okay|well"],
       "asks how Helmus's last school day or exam went",
       yes=["how was school?", "how was your day at school", "was class boring", "how was class today", "how was ur exam", "how did class go", "how was uni"],
       no=["how is school", "how was work", "i was at school", "school was fun"])
intent("st_ask_school_where", ["where [do] you go to @st_school", "what|which school|college|uni|university",
                               "where [do] you study", "what high school", "where are you in school"],
       "asks which school or college Helmus goes to",
       yes=["where do you go to school?", "what college do u go to", "which uni", "where do you study",
            "what school r u at"],
       no=["do you go to school", "i go to school in ohio", "how is school"])
intent("st_ask_homework_exams", ["you have [a|any] @st_hw", "you got [a|any] @st_hw", "did you do [your] homework",
                                 "you done [your] homework", "you finish [your] homework", "any @st_hw",
                                 "how much homework", "you studying for"],
       "asks whether Helmus has homework or exams",
       yes=["do you have homework?", "did you do your homework", "any exams coming up", "do u have a test tomorrow",
            "how much homework do you get", "are you studying for finals"],
       no=["i have homework", "my homework is hard", "that was a test", "is this a test"])

# ==== home ===========================================================================================================
intent("st_ask_live_with", ["who [do] you live with", "you live alone|solo", "you live by yourself",
                            "!can|could you live with", "you [still] live at home", "you have your own place|apartment",
                            "you live on your own"],
       "asks who Helmus lives with",
       yes=["who do you live with?", "do you live alone", "do u live with your parents", "do you live by yourself",
            "do you still live at home", "do you have your own place"],
       no=["i live with my mom", "where do you live", "i live alone", "can you live with that"])
intent("st_ask_roommate", ["you have [a|any] @st_roommate", "your @st_roommate", "any @st_roommate",
                             "how many @st_roommate", "you live with [any] @st_roommate",
                             "you share [an|your|a] apartment|place|house|flat"],
       "asks about Helmus's roommates",
       yes=["do you have roommates?", "how many roommates do you have", "do you share an apartment", "do u have a roommate", "how is your roommate", "any roommates?",
            "are your roommates cool", "do you have a flatmate"],
       no=["my roommate is annoying", "i need a roommate", "i live with roommates"])
intent("st_ask_home_type", ["house or [an] apartment|flat|condo|dorm", "apartment|flat|dorm or [a] house",
                            "you live in [a|an] @st_dwelling", "you rent", "you pay rent", "your rent",
                            "how much is rent", "your @st_dwelling", "your place like|big|small|nice",
                            "you own [a|your|the] house|home|place"],
       "asks what kind of home Helmus lives in",
       yes=["do you live in a house or apartment?", "do u rent", "what is your house like",
            "how big is your apartment", "do you live in a dorm", "do you pay rent", "is your place nice"],
       no=["i live in an apartment", "my house is big", "describe your room", "rent a movie"])
intent("st_ask_room", ["your room|bedroom|walls|desk|setup", "what is in your room", "describe [your] room|bedroom",
                         "what is on your wall", "you share [a] room|bedroom", "you have your own room"],
       "asks about Helmus's room or desk setup",
       yes=["what's your room like?", "do you have your own room", "do you share a room", "describe ur room", "is your room clean", "what does your bedroom look like",
            "what is your setup like", "what color are your walls"],
       no=["my room is messy", "there is no room", "i am in my room", "chat room"])
intent("st_ask_location_now", ["you at [the] @st_spot", "you still at [the] @st_spot", "^ your at [the] @st_spot",
                               "are you home|outside|inside|indoors", "you in [your|the|a] @st_inside", "you still in [your|the|a] @st_inside",
                               "where are you [at] right now", "where are you now", "where are you sitting",
                               "where are you typing|chatting|sitting"],
       "asks where Helmus is right now (home, work, in bed)",
       yes=["are you at home?", "r u home rn", "where are you right now", "are you in bed lol", "are you at work",
            "are you in your room", "where are you sitting", "ur at school?"],
       no=["i am at home", "where are you from", "are you good at school", "i am in bed"])
intent("st_ask_lived_there_long", ["how long [have] you [been] lived|living", "you always lived", "you lived there long",
                                   "lived * your whole life", "when did you move", "did you move there|here",
                                   "you moved there|here"],
       "asks how long Helmus has lived where it lives",
       yes=["how long have you lived there?", "have you always lived there", "how long u been living there",
            "when did you move there", "have you lived there your whole life", "did you move there or grow up there"],
       no=["i have lived here for 10 years", "where do you live", "do you live alone", "move your body"])
intent("st_ask_want_to_move", ["you want to move", "you ever move", "would you move", "!did you move away|out",
                               "where would you * live", "you stay there forever"],
       "asks whether Helmus wants to move somewhere else",
       yes=["do you want to move?", "would you ever move away", "where would you like to live",
            "do u wanna move out", "would you move to california"],
       no=["i want to move", "when did you move", "move your body", "when did you move out"])

# ==== family and relationships =======================================================================================
intent("st_ask_sibling_count", ["how many @st_sibling", "!am [an] only child", "you the oldest|youngest|middle|eldest|baby",
                                "older or younger", "younger or older", "brothers|brother or [a] sisters|sister",
                                "sisters|sister or [a] brothers|brother", "how big is your family",
                                "how many * in your family", "big family"],
       "asks how many siblings Helmus has, or its place among them",
       yes=["how many siblings do you have?", "are you an only child", "are you the oldest", "older or younger?",
            "do you have brothers or sisters", "how big is your family", "how many people are in your family"],
       no=["i have two sisters", "i'm an only child", "how many cats do you have", "i am the oldest"])
intent("st_ask_sibling_about", ["your [little|big|older|younger|baby|twin] @st_sibling", "you and your @st_sibling",
                                  "you fight with [your] @st_sibling", "you close to|with [your] @st_sibling"],
       "asks about one of Helmus's siblings (age, what they are like)",
       yes=["how old is your sister?", "do you fight with your brother", "are you close with your siblings", "what's your brother like", "do you get along with your siblings",
            "what does ur sister do", "is your little sister annoying", "your bro cool?"],
       no=["my sister is annoying", "do you have a sister", "i have a brother", "you are like a brother to me"])
intent("st_ask_parents", ["how is|are your @st_parent", "your @st_parent do", "your @st_parent like",
                          "are your @st_parent", "is your @st_parent", "with your @st_parent", "to your @st_parent",
                          "your @st_parent work|job", "how old is|are your @st_parent"],
       "asks about Helmus's parents",
       yes=["what do your parents do?", "do you get along with ur parents", "are your parents strict",
            "how is your mom", "what does your dad do for work", "are your parents still together"],
       no=["my mom is annoying", "do you live with your parents", "ur mom lol", "your mom"],
       unless=["st_ask_live_with"])
intent("st_ask_family_close", ["close to|with your family", "get along with your family", "see your family",
                               "your family close", "you visit your family", "your family like"],
       "asks how close Helmus is with its family",
       yes=["are you close with your family?", "do you get along with your family", "do you see your family much",
            "is your family close", "do you visit your family often"],
       no=["i am close with my family", "my family is close", "do you have family"])
intent("st_ask_relationship", ["you dating", "your dating", "you have a|any @st_partner", "^ [you] got a @st_partner",
                               "you seeing anyone|someone", "you in a relationship", "been in a relationship",
                               "you taken $", "^ single $", "you single", "relationship status", "your @st_partner",
                               "you ever had a @st_partner"],
       "asks whether Helmus is dating anyone",
       yes=["are you dating anyone?", "do u have a gf", "are you seeing anyone", "r u in a relationship",
            "are you taken", "whats your relationship status", "single?", "have you ever had a girlfriend"],
       no=["i have a girlfriend", "my boyfriend is mad", "i am single", "are you taken over by robots"])
intent("st_ask_crush", ["you have a crush", "you got a crush", "your crush", "any crushes|crush",
                        "you like anyone|someone|anybody", "you crushing on"],
       "asks whether Helmus has a crush",
       yes=["do you have a crush?", "who's your crush", "any crushes", "do u like anyone", "do you like someone rn"],
       no=["i have a crush on her", "do you like anime", "my crush ignored me"])
intent("st_ask_future_family", ["you [ever] want [to] [have] kids|children", "you [ever] want a family",
                                "you [ever] want to get married", "would you [ever] get married", "you want to marry"],
       "asks whether Helmus wants kids or to get married someday",
       yes=["do you want kids?", "do you want to get married someday", "would you ever get married",
            "do u want children", "do you want a family one day"],
       no=["i want kids", "are you married", "do you have kids", "i want to get married"])

# ==== pets ===========================================================================================================
intent("st_ask_pet_name", ["your @st_animal name", "your @st_animal called|named", "what is the @st_animal name|called",
                           "name of your @st_animal", "what did you name [your|the] @st_animal|it|him|her"],
       "asks the name of Helmus's pet",
       yes=["what's your dog's name?", "whats ur cats name", "what is your cat called", "what did you name your dog",
            "what's the name of your cat", "what did u name it"],
       no=["my dog's name is max", "what is your name", "name a dog breed", "do you have a dog"])
intent("st_ask_pet_breed", ["what breed", "what kind|type of @st_animal", "your @st_animal look like",
                            "what color|colour is your @st_animal", "is it a mutt|purebred"],
       "asks what breed or kind Helmus's pet is, or what it looks like",
       yes=["what breed?", "what kind of dog is it", "what type of cat", "what does your cat look like",
            "what color is your dog", "what breed is your dog"],
       no=["i have a lab", "what kind of music", "what color is your hair", "dog breeds are cool"])
intent("st_ask_pet_age", ["how old is [your|the] @st_animal", "how long [have] you had [your|the] @st_animal",
                          "how long [have] you had it|him|her", "when did you get [your|the] @st_animal",
                          "where did you get [your|the] @st_animal", "is it|he|she a puppy|kitten"],
       "asks how old Helmus's pet is or how long it has had it",
       yes=["how old is your dog?", "how old is ur cat", "how long have you had your cat", "how long have u had him",
            "when did you get your dog", "is it a puppy"],
       no=["how old are you", "my dog is 5", "how old is your sister", "how long have you had that job"])
intent("st_ask_pet_personality", ["your @st_animal like", "is your @st_animal", "does your @st_animal",
                                  "does it|he|she bite|scratch|bark", "a good boy|girl", "you walk your @st_animal",
                                  "is it|he|she friendly|cute|fluffy|lazy|fat|chonky|mean", "your @st_animal do",
                                  "love your @st_animal"],
       "asks what Helmus's pet is like",
       yes=["is your dog nice?", "what's your cat like", "does it bite", "is he a good boy",
            "do you walk your dog every day", "is she fluffy", "does your cat sleep with you"],
       no=["my dog is nice", "what is your dog's name", "is it raining", "how old is your cat",
           "what color is your dog"],
       unless=["st_ask_pet_name", "st_ask_pet_breed", "st_ask_pet_age"])
intent("st_ask_pet_pic", ["pic|pics|picture|pictures|photo|photos of [your|the] @st_animal",
                          "pic|pics|picture|pictures|photo|photos of it|him|her", "@st_animal pic|pics|picture|pictures|photo|photos",
                          "show me [your|the] @st_animal", "can i see [your|the] @st_animal"],
       "asks for a photo of Helmus's pet",
       yes=["send a pic of your dog", "can i see your cat", "dog pics?", "show me your cat",
            "any pictures of your dog"],
       no=["send me a pic", "i saw a dog", "can i see you"])

# ==== car and money ==================================================================================================
intent("st_ask_car", ["you have|got [a] car|truck|license|licence", "you have your license|licence", "what car|truck",
                      "kind|type of car", "what do you drive", "do you drive", "can you drive", "your car|truck|license",
                      "know how to drive"],
       "asks whether Helmus has a car or drives",
       yes=["do you have a car?", "what car do u drive", "what do you drive", "can you drive",
            "do you have your license", "what kind of car is it", "is your car any good"],
       no=["i have a car", "my car broke down", "drive safe", "i can drive"])
intent("st_ask_money", ["you rich|broke|poor|loaded|wealthy", "your broke", "you have * money", "how much money",
                        "you have [any] savings", "you saving up|money", "you in debt"],
       "asks about Helmus's money situation",
       yes=["are you rich?", "r u broke lol", "how much money do you have", "do you have money",
            "do you have a lot of money", "are you saving up for anything"],
       no=["i am broke", "money is tight", "can you lend me money"])
intent("st_ask_spending", ["you spend * money", "spend your money", "what did you buy", "last thing you bought",
                           "you buy anything", "you bought", "you shop"],
       "asks what Helmus spends money on or bought recently",
       yes=["what do you spend your money on?", "did you buy anything", "what's the last thing you bought",
            "what did you buy today", "do you shop a lot", "what do u spend money on"],
       no=["i bought shoes", "buy me a drink", "i spend too much", "should i buy it"])

# ==== hometown =======================================================================================================
intent("st_ask_hometown_like", ["what is it like there", "what is it like living there|in|where",
                                "what is it like where you live", "what is it like in your", "like where you live",
                                "is it [@intens] @st_placeadj there", "how is it [over] there", "big city or [a] small town",
                                "how big is columbus", "is it|that [like|really] a [@intens] big|small city|town|place",
                                "your town|city|hometown|neighborhood|neighbourhood|area|state",
                                "you like living there|in|here", "you like it there",
                                "what is {place:unknown} like $", "known|famous for", "famous there|around"],
       "asks what Helmus's town is like, or what it is known for",
       yes=["what's it like there?", "what is it like where you live", "what is guadalajara like", "is it nice there", "how is it over there",
            "what's your town like", "do you like living there", "is it a big city", "what is it famous for",
            "what is columbus known for", "is that really a small town", "big city or small town?"],
       no=["what is it like being a bot", "is that a big deal", "is it cold there", "i like it here", "what is that like"],
       unless=["st_ask_local_slang"])
intent("st_ask_hometown_todo", ["what is there to do", "is there * to do", "anything to do there|around|in",
                                "what do people do there", "what do people do for fun", "what do you all do for fun",
                                "fun things to do", "things to do there|around", "best place to eat|go",
                                "where do people hang out", "where do you all hang out"],
       "asks what there is to do in Helmus's town",
       yes=["what is there to do there?", "is there much to do", "what do people do for fun there",
            "anything to do around there", "where do people hang out", "whats the best place to eat there"],
       no=["i have so much to do", "what do you do for fun", "there is nothing to do here"])
intent("st_ask_born_raised", ["you grow up there|here|in|around|near", "you grew up there|here|in",
                              "!when were you born", "you born there|in|here", "you originally", "from originally",
                              "you born and raised"],
       "asks whether Helmus was born or grew up where it lives",
       yes=["did you grow up there?", "were you born there", "where were you born", "are you originally from ohio",
            "where are you from originally", "were u born and raised there"],
       no=["when were you born", "i grew up in texas", "i was born there", "you were born yesterday lol"])

# ==== travel =========================================================================================================
intent("st_ask_travel_history", ["you travel", "you like [to] travel|traveling", "you [ever] traveled|travelled",
                                 "been anywhere", "places [have] you been|visited|traveled",
                                 "out of the country|state", "left the country|state", "been abroad|overseas",
                                 "you [ever] flown", "you [ever] been on a plane|flight", "you have a passport"],
       "asks whether and where Helmus has travelled",
       yes=["do you travel much?", "have you ever traveled", "been anywhere cool?", "have you been out of the country",
            "have u ever been on a plane", "do you have a passport", "do you like to travel"],
       no=["i love traveling", "i have been to france", "where have you been", "time travel is cool"])
intent("st_ask_been_to", ["you been to", "you ever been to", "^ [ever] been to", "you [ever] visited", "you ever gone to",
                          "you ever go to"],
       "asks whether Helmus has been to a named place (the place is copied when it is a name)",
       unless=["st_ask_concerts"],
       yes=["have you been to new york?", "have u ever been to europe", "ever been to canada?", "have you visited japan",
            "you been to florida?"],
       no=["i have been to paris", "where have you been", "i went to canada", "have you been busy"])
intent("st_ask_travel_wish", ["where [do] you want to go|travel|visit", "where would you * go|travel|visit",
                              "dream vacation|trip|destination", "you could go|travel anywhere", "bucket list",
                              "you want to visit", "place you want to visit|go"],
       "asks where Helmus would like to travel",
       yes=["where do you want to travel?", "if you could go anywhere where would you go", "whats your dream vacation",
            "where would you like to visit", "anything on your bucket list", "where do u wanna go someday"],
       no=["i want to go to japan", "where are you going", "i could go anywhere"])
intent("st_ask_last_trip", ["last vacation|trip|holiday", "you go on [a] vacation|trip", "you go anywhere",
                            "you travel this|last|recently", "your trip", "been on vacation"],
       "asks about Helmus's last trip or vacation",
       yes=["where did you go on your last vacation?", "did you go anywhere this summer", "how was your trip",
            "have you been on vacation recently", "where did u go on vacation"],
       no=["i went on vacation", "i want a vacation", "trip over", "where did you go"])

# ==== recent events ==================================================================================================
intent("st_ask_yesterday", ["you do yesterday", "you do last night", "you do * yesterday", "how was yesterday",
                            "you get|got up to yesterday|last", "were you up to yesterday|last",
                            "how was last night", "did you * last night", "did you * yesterday"],
       "asks what Helmus did yesterday or last night",
       yes=["what did you do yesterday?", "how was last night", "did u go out last night", "what did you do last night",
            "did you do anything fun yesterday", "how was yesterday", "what did u get up to last night"],
       no=["i went out last night", "what are you doing tonight", "yesterday was fun", "what did you do today"])
intent("st_ask_last_weekend", ["how was [your|the] weekend", "did you do * weekend", "you do last weekend",
                               "you get|got up to * weekend", "were you up to * weekend",
                               "did your weekend", "your weekend go", "was your weekend",
                               "did you have a [good|nice|fun] weekend"],
       "asks what Helmus did last weekend",
       yes=["how was your weekend?", "what did you do last weekend", "did you do anything fun this weekend",
            "how did your weekend go", "did you have a good weekend", "was your weekend fun",
            "what were u up to over the weekend", "what did you get up to this past weekend"],
       no=["what are you doing this weekend", "have a good weekend", "what do you do on weekends",
           "my weekend was boring"])
intent("st_ask_life_lately", ["you been up to", "you been doing lately|recently", "anything * lately|recently",
                              "how has life", "life treating you", "new with you", "going on in your life",
                              "new in your life", "you been busy", "you keeping busy", "been keeping busy"],
       "asks what has been going on in Helmus's life lately",
       yes=["what have you been up to?", "anything exciting happen lately", "whats new with you",
            "how has life been treating you", "what's going on in your life", "you been busy lately?",
            "what u been up to"],
       no=["what are you up to", "i have been busy", "what is new", "what do you want to do with your life"])
intent("st_ask_last_holiday", ["you do for @st_holiday", "how was [your] @st_holiday", "you dress up",
                               "were you for halloween", "your costume", "you dressed up", "trick or treating",
                               "you get for christmas|birthday|hanukkah", "did you celebrate"],
       "asks what Helmus did for a recent holiday (Halloween was last week)",
       yes=["what did you do for halloween?", "how was your halloween", "did you dress up",
            "what were you for halloween", "did you go trick or treating", "what did u get for christmas",
            "what was your costume"],
       no=["what are you doing for thanksgiving", "i love halloween", "i dressed up as a cat",
           "what do you do for fun"])
intent("st_ask_birthday", ["your birthday", "month were you born", "day were you born", "you born on",
                           "your zodiac", "your star sign", "what is your sign $"],
       "asks when Helmus's birthday is or its star sign",
       yes=["when is your birthday?", "whens ur bday", "what did you do for your birthday", "what month were you born",
            "what's your zodiac sign", "is it your birthday soon"],
       no=["it is my birthday", "happy birthday", "how old are you", "my bday is in may"])

# ==== personal details ===============================================================================================
intent("st_ask_appearance", ["what do you look like", "how do you look", "how tall", "your height", "your hair|eyes",
                             "describe yourself", "are you tall|short", "you have tattoos|piercings|glasses|freckles", "you have a beard",
                             "you wear glasses", "selfie", "pic|picture|photo of you|yourself"],
       "asks what Helmus looks like",
       yes=["what do you look like?", "how tall are you", "what color is your hair", "describe yourself",
            "do you have tattoos", "send a selfie", "are you tall"],
       no=["you look like a bot", "i am tall", "my hair is brown", "what does your dog look like"])
intent("st_ask_gender", ["boy|guy|man|male|dude or [a] girl|woman|female|gal",
                         "girl|female|woman or [a] boy|guy|man|male", "^ m or f", "^ f or m", "^ m / f", "your gender",
                         "your pronouns", "you a guy|girl|boy|dude|woman|female|male|chick"],
       "asks whether Helmus is a man or a woman",
       yes=["are you a boy or a girl?", "male or female", "m or f", "are you a guy", "what's your gender",
            "guy or girl?", "r u a girl"],
       no=["i am a guy", "my girlfriend", "boys and girls", "is your cat a boy or a girl"],
       unless=["F:c:st_animal"])
intent("st_ask_asl", ["^ asl", "^ a / s / l", "^ a s l $", "^ age sex location"],
       "asks age, sex and location in one go (old chat-room 'asl')",
       yes=["asl", "asl?", "age sex location", "a s l", "a/s/l", "asl pls", "asl lol"],
       no=["i am asleep", "as long as", "funny asl"])
intent("st_ask_nationality", ["your nationality", "what nationality", "are you @st_nation",
                              "you from the us|uk|states|usa|america|england|canada", "you from america|england|canada",
                              "you live in the us|uk|usa|states", "you live in america|england|canada",
                              "you in the us|uk|usa|states", "you in america|england|canada"],
       "asks Helmus's nationality or country",
       yes=["are you american?", "are you in the us", "what nationality are you", "are you from the us", "r u british",
            "do you live in america", "are you canadian"],
       no=["i am american", "american food", "where are you from"])
intent("st_ask_friends", ["you have * friends", "your friends", "your best friend", "your friend",
                          "you hang out with", "you go out much|a|often|lot", "you have a best friend"],
       "asks about Helmus's friends and social life",
       yes=["do you have friends?", "do you have a lot of friends", "what are your friends like",
            "who is your best friend", "do you hang out with friends much", "do you go out much"],
       no=["i have friends", "my friends are here", "are we friends", "you are my friend"])
intent("st_ask_wearing", ["you wearing", "you dressed", "your outfit", "you [still] in pajamas|pjs|pyjamas",
                          "what clothes"],
       "asks what Helmus is wearing",
       yes=["what are you wearing?", "what r u wearing rn", "are you still in pajamas", "describe your outfit",
            "are you dressed"],
       no=["i am wearing a hoodie", "dressed up for halloween", "wear a mask"])

# ==== the user tells about themselves ================================================================================
intent("st_tell_off_work", ["got off work|early|shift", "got off my shift", "got off of work",
                            "got out of [my] class|school|work|practice|lecture",
                            "done with [my] work|school|class|classes|shift", "finished [my] work|shift|class|classes",
                            "!you off work", "home from work|school|class|practice", "back from work|school|class"],
       "the user just finished work or class",
       yes=["i just got off work", "just got home from work", "i got out of class early", "finally done with work",
            "just finished my shift", "im off work now", "back from school"],
       no=["are you off work", "i have work", "i got off the bus", "when do you get off work"])
intent("st_tell_just_got_back", ["just got home|back", "^ i am back", "got back from", "just got in $", "^ back $"],
       "the user just got home or back from somewhere",
       yes=["i just got home", "just got back from the gym", "im back", "i got back from my trip yesterday",
            "just got in"],
       no=["when did you get back", "back to the topic", "brb", "i just got in trouble"])
intent("st_tell_at_home", ["i am at home", "i am home", "i am in [my] bed|room|bedroom|basement|kitchen",
                           "in my bed|room|bedroom", "^ in bed", "on the|my couch|sofa|bed",
                           "chilling|sitting|stuck|staying at home", "^ at home", "^ home $"],
       "the user says they are at home",
       yes=["i'm at home", "im home", "i am in my room", "in bed rn", "i'm on the couch", "just chilling at home",
            "stuck at home today"],
       no=["are you at home", "i am not home", "i am going home later", "my home is in ohio"])
intent("st_tell_at_work", ["i am at [the|my] work|school|college|uni|office|job|library|campus",
                           "i am in [a] class|school|meeting|lecture", "on [my|a|lunch] break", "i am working $",
                           "i am working right now", "^ at work|school", "^ in class"],
       "the user says they are at work or school right now",
       yes=["i'm at work", "im in class rn", "i am on my break", "at work lol", "i'm working right now",
            "i am at the library", "i'm at school"],
       no=["are you at work", "i work at a bank", "i am working on a project", "i am good at school"])
intent("st_tell_bored", ["i am [@intens] !not bored", "i was [@intens] bored", "^ [@intens] bored", "have nothing to do",
                         "nothing to do $", "nothing to do here|today|right|at", "bored out of my mind",
                         "i am getting bored"],
       "the user says they are bored",
       yes=["i'm bored", "so bored", "bored lol", "im so bored rn", "nothing to do here", "i have nothing to do",
            "bored out of my mind"],
       no=["you are boring", "i am not bored", "this is boring", "are you bored", "nothing to do with you"])
intent("st_tell_eating", ["i am eating|drinking|snacking", "i am having [my] @st_meal", "^ eating", "just ate",
                          "about to eat", "i am going to eat", "i am getting food", "!you eating my|a|an|some",
                          "i [just] ate", "had * for @st_meal", "i am having * for @st_meal"],
       "the user says they are eating or just ate",
       yes=["i'm eating", "i'm about to eat", "eating dinner rn", "just ate", "i'm having lunch", "i had pizza for dinner",
            "i ate a sandwich", "i am eating cereal lol", "hi, eating some leftovers rn"],
       no=["what are you eating", "are you eating a sandwich", "i am not eating", "do you like eating", "what did you have for dinner"])
intent("st_tell_hungry", ["i am [@intens] !not hungry|starving|starved|famished", "^ [@intens] hungry|starving",
                          "i need food", "i want food", "i could eat"],
       "the user says they are hungry",
       yes=["i'm hungry", "starving", "so hungry rn", "i need food", "im starving lol", "i could eat"],
       no=["are you hungry", "i am not hungry", "hunger games"])
intent("st_tell_just_woke", ["i [just] woke up", "just woke [up]", "^ [just] woke up", "just got up", "i [just] got up",
                             "i overslept", "i slept in|late", "i am [just] waking up"],
       "the user says they just woke up",
       yes=["i just woke up", "just woke up lol", "i overslept", "i slept in today", "woke up late", "just got up"],
       no=["did you just wake up", "wake up", "when did you wake up"])
intent("st_tell_going_to_bed", ["!you going to bed|sleep", "about to * sleep|bed|crash", "i should * sleep|bed",
                                "i need [to] sleep", "i need to go to bed", "past my bedtime"],
       "the user says they will go to sleep soon",
       yes=["i'm going to bed soon", "about to sleep", "i should go to bed", "gonna sleep after this", "i need sleep",
            "its past my bedtime lol"],
       no=["are you going to bed", "i can not sleep", "go to sleep", "i went to bed late"])
intent("st_tell_cant_sleep", ["can not sleep", "insomnia", "have not slept", "did not sleep", "up all night",
                              "barely slept", "no sleep"],
       "the user says they cannot sleep or did not sleep",
       yes=["i can't sleep", "cant sleep lol", "i have insomnia", "i didn't sleep at all", "i was up all night",
            "barely slept last night"],
       no=["can you sleep", "i slept well", "did you sleep"])
intent("st_tell_school_level", ["i am in high|middle school", "i am in college|uni|university|grad",
                                "i am a @st_year", "i am in my * year", "i am in year|grade", "i am a * student",
                                "i go to [a] college|uni|university", "i go to high school", "i [just] graduated",
                                "senior year"],
       "the user says what school or year they are in",
       yes=["i'm in high school", "im a junior", "i'm in college", "i am in my second year", "i'm a college student",
            "i just graduated", "i go to uni"],
       no=["are you in high school", "what year are you in", "my sister is in high school", "i am in my room"])
intent("st_tell_work_bad", ["i hate [my] job|work|boss|shift|coworkers|manager", "work|job|shift [was|is] [@intens] @st_badadj",
                            "my boss|manager|coworkers|coworker [is|are] [@intens] @st_badadj|@insult",
                            "long|rough|bad|hard day at work", "quit my job", "i got fired", "i got laid off"],
       "the user complains about work",
       yes=["i hate my job", "work sucks", "my boss is so annoying", "long day at work", "work was rough today",
            "i want to quit my job", "i got fired lol"],
       no=["do you like your job", "i love my job", "how was work", "work is fine"])
intent("st_tell_work_good", ["i love|like|enjoy my job|work|boss|coworkers", "work|job|shift was|is [@intens] @st_goodadj",
                             "i [just] got promoted", "i [just] got a raise", "i [just] got [the|a] job", "i [just] got hired", "new job"],
       "the user says work is going well or they got good news at work",
       yes=["i love my job", "work was good today", "i got promoted", "i just got a raise", "i got the job!",
            "work was chill", "i just started a new job"],
       no=["i hate my job", "do you like your job", "how was work", "good job lol"])
intent("st_tell_school_bad", ["i hate [my] @st_school|@st_hw", "@st_school|@st_hw [is|was|are] [@intens] @st_badadj",
                              "so much homework|studying", "lot of homework|studying|exams", "@st_hw * killing me",
                              "i [just] failed", "i have [a|an] @st_hw", "finals week"],
       "the user complains about school or exams",
       yes=["school sucks", "i hate school", "i have so much homework", "finals are killing me", "i failed my test",
            "i have a test tomorrow", "class was so boring"],
       no=["do you like school", "i love school", "how was school", "do you have homework"])
intent("st_tell_age", ["i am [only|just] @st_agenum $", "i am [only|just] @st_agenum @laugh",
                       "i am [only|just] @st_agenum [years] old", "i am @st_agenum years", "@st_agenum years old",
                       "i [just] turned @st_agenum", "turning @st_agenum", "i am @st_agenum and|too|also",
                       "^ @st_agenum m|f|male|female|guy|girl"],
       "the user says their age",
       yes=["i'm 19", "im 25 lol", "i am 30 years old", "i just turned 21", "19 years old", "i am nineteen",
            "im only 16", "19 m"],
       no=["how old are you", "i am 20 minutes away", "i have 19 cats", "my sister is 13"])
_slots("st_tell_age", "age", ["{age} years old", "i am only|just {age}", "turned|turning {age}",
                              "i am {age} years|and|too|also|@laugh", "i am {age} $", "^ {age} m|f|male|female|guy|girl"],
       "the word that is the user's age")
register("st_user_age", "st_tell_age", "age", "the age the user gave, kept for the rest of the chat")
intent("st_tell_grew_up", ["i grew up", "i was born in {where}", "i was born and raised",
                           "born and raised in", "!you originally from", "i moved here|there from", "we moved here|there",
                           "i moved to|from"],
       "the user says where they were born or grew up",
       yes=["i grew up in texas", "i was born in mexico", "i was born in a small town", "born and raised in chicago", "i'm originally from ohio",
            "i moved here from california", "i grew up near the beach"],
       no=["where did you grow up", "were you born there", "i was born in 2005", "are you originally from ohio"],
       unless=["F:shape:number"])
_slots("st_tell_grew_up", "place", ["grew up in {place:unknown}", "born in {place:unknown}",
                                    "originally from {place:unknown}", "raised in {place:unknown}",
                                    "moved here|there from {place:unknown}"],
       "the name of the place the user grew up in")
register("st_user_hometown", "st_tell_grew_up", "place", "where the user grew up, kept for the rest of the chat")
intent("st_tell_siblings", ["i have * @st_sibling", "my [little|big|older|younger|baby|twin] @st_sibling",
                            "i am [an] only child", "i am the oldest|youngest|middle|eldest", "i have no siblings",
                            "i do not have * @st_sibling"],
       "the user tells about their siblings",
       yes=["i have a sister", "i don't have any siblings", "i have two brothers", "i'm an only child", "my little sister is so annoying",
            "i am the oldest", "my brother plays games too"],
       no=["do you have siblings", "how old is your sister", "are you an only child"])
intent("st_tell_parents", ["my @st_parent", "me and my @st_parent", "my old man", "my family is|are"],
       "the user tells about their parents",
       yes=["my mom is so annoying", "me and my dad went fishing", "my family is kinda crazy", "my parents are strict", "my dad works nights", "my mom just called me",
            "my folks are visiting"],
       no=["your mom", "how is your mom", "do you live with your parents"])
intent("st_tell_living_situation", ["i live with", "i live alone|solo", "i live by myself", "i [still] live at home",
                                    "i have [a] @st_roommate", "my @st_roommate", "i live in [a|an] @st_dwelling",
                                    "i live in the dorms"],
       "the user tells who they live with or what kind of home",
       yes=["i live with my parents", "i live alone", "i live by myself", "i still live at home", "i have roommates",
            "my roommate is weird", "i live in an apartment", "i live in a dorm"],
       no=["who do you live with", "do you live alone", "i live in texas", "where do you live"])
intent("st_tell_relationship", ["i have a|an @st_partner", "my @st_partner", "i am [still] single", "i am married|engaged|taken",
                                "got dumped", "broke up", "i am dating", "my ex"],
       "the user tells about their relationship status",
       yes=["i have a girlfriend", "i'm single", "my bf is mad at me", "i just got dumped", "we broke up last week",
            "i'm married", "my ex texted me"],
       no=["are you single", "do you have a girlfriend", "your girlfriend", "single player game"])
intent("st_tell_plans", ["i have plans", "i got plans", "i am going out", "i am @st_planverb * @st_when",
                         "@st_when i am @st_planverb", "i have work|school|class tomorrow|tonight|later|today",
                         "i am working tonight|tomorrow|later"],
       "the user tells their plans",
       yes=["i'm going out tonight", "i have work tomorrow", "i am going to a party later",
            "this weekend im visiting my grandma", "i have plans tonight", "i'm seeing my friends tomorrow",
            "i got plans later"],
       no=["what are you doing tonight", "do you have plans", "i went out last night", "i am going to bed"])
intent("st_tell_doing_now", ["i am [just] @st_nowverb", "^ [just] @st_nowverb", "doing [my] homework|laundry|chores|dishes",
                             "i am [just] on my phone|computer|laptop", "i am in the middle of"],
       "the user says what they are doing right now",
       yes=["i'm watching tv", "im on my phone", "i'm in the middle of dinner", "playing games", "just chilling", "doing homework lol", "im cooking dinner",
            "watching netflix rn", "i am scrolling on my phone"],
       no=["i am doing good", "what are you watching", "i like watching tv", "do you play games"])
intent("st_tell_nothing_much", ["^ nothing much", "^ not much $",
                                "^ not much you|what|how|and|just|here|really|honestly|man|bro|@laugh",
                                "^ nothing really", "^ nothing $", "^ nothing @laugh $", "^ not a lot", "same old", "^ just the usual",
                                "^ the usual", "^ nothing just"],
       "the user says they are not doing much (an answer to 'wyd')",
       yes=["nothing much", "not much u?", "nm", "nothing really lol", "same old same old", "just the usual",
            "not a lot"],
       no=["not much of a gamer", "i do not know much", "i have nothing to do", "nothing is wrong"])
intent("st_tell_busy", ["i am [@intens] !not busy", "^ [@intens] busy", "busy day|week|morning", "so much to do",
                        "a lot to do", "lot going on", "!you been [@intens] busy", "swamped"],
       "the user says they are busy",
       yes=["i'm busy", "so busy today", "busy day", "i have so much to do", "i've been busy", "a lot going on rn",
            "im swamped"],
       no=["are you busy", "i am not busy", "have you been busy", "the store was busy"])
intent("st_tell_sick", ["i am [@intens] !not sick|ill $", "i am [@intens] !not sick|ill today|again|right|with|and|@laugh",
                        "i am getting sick", "i got sick", "i feel [@intens] sick|ill|nauseous", "i have [a|the] @st_illness",
                        "not feeling [@intens] well|good|great", "under the weather"],
       "the user says they are ill",
       yes=["i'm sick", "i have a cold", "i'm not feeling well", "i have the flu", "i have a headache", "i feel sick",
            "under the weather today"],
       no=["are you sick", "that's sick", "i am not sick", "i am sick of this"])
intent("st_tell_travel", ["i * been to", "i went on [a] vacation|trip|cruise", "i am going on [a] vacation|trip|cruise",
                          "got back from [my|a] vacation|trip", "i traveled|travelled|visited|flew", "my trip|vacation"],
       "the user tells about a trip",
       yes=["i've been to paris", "i went on vacation last month", "i'm going on a trip next week",
            "i just got back from my vacation", "i traveled to japan last year", "i visited my aunt in florida",
            "i have never been to europe"],
       no=["have you been to paris", "i want a vacation", "where did you go on vacation"])
intent("st_tell_pet", ["i [also] have [a|an|@number] @st_animal", "i have @st_agenum @st_animal", "i got [a|an] @st_animal",
                       "we have [a|an] @st_animal", "my @st_animal", "i [just] adopted [a|an] @st_animal"],
       "the user says they have a pet",
       yes=["i have a dog", "i got a cat lol", "i have two cats", "my dog is sleeping next to me", "we have a puppy",
            "i just adopted a kitten"],
       no=["do you have a dog", "i want a dog", "i hate dogs", "your dog sounds cute"])
intent("st_tell_pet_name", ["@st_animal name is {pet_name}", "@st_animal [is] called|named {pet_name}",
                            "i named him|her|it {pet_name}", "^ {pet_name:content} is my @st_animal"],
       "the user says their pet's name",
       yes=["my dog's name is max", "i named her luna", "biscuit is my cat", "my cat is called luna", "i have a dog named buddy", "my cats name is mittens",
            "we have a cat called tom", "my puppy is named rocky"],
       no=["my name is sam", "what is your dog's name", "my dog is cute", "name your dog"])
register("st_user_pet_name", "st_tell_pet_name", "pet_name", "the name of the user's pet, kept for the rest of the chat")
intent("st_tell_no_pet", ["i do not have [a|any] @st_animal", "i have no @st_animal", "^ no @st_animal",
                          "i am allergic to @st_animal", "my @st_parent will not let me"],
       "the user says they have no pet (or cannot have one)",
       yes=["i dont have pets", "i don't have a dog", "no pets", "i have no pets", "i'm allergic to cats",
            "my mom won't let me get a dog"],
       no=["i have a dog", "do you have pets", "i do not have time", "no way"])
intent("st_tell_car", ["my car|truck", "i [just] got a [new|used] car|truck", "i drive a|an", "i [just] got my license|permit",
                       "i do not have a car|license", "i can not drive", "i do not drive", "i have a car|truck"],
       "the user tells about their car or driving",
       yes=["my car broke down", "i just got a new car", "i drive a honda", "i got my license last week",
            "i don't have a car", "i can't drive lol"],
       no=["do you have a car", "what car do you drive", "can you drive"])
intent("st_tell_money", ["i am [@intens] !not broke|poor", "i [just] got paid", "^ payday", "it is payday",
                         "money is tight", "i need [some] money|cash", "spent all my money", "i have no money|cash"],
       "the user tells about their money",
       yes=["i'm broke", "i just got paid", "payday!", "money is tight rn", "i need money", "i spent all my money on games",
            "im so poor lol"],
       no=["are you broke", "how much money do you have", "i am not broke", "pay me"])
intent("st_tell_same", ["^ same $", "^ same here|honestly|though|to|bro|man|@laugh", "^ @laugh same", "^ me too",
                        "^ me neither|either", "^ relatable", "^ mood $", "^ i do too", "^ so do|am|did i",
                        "^ i am the same", "same with me", "^ same for me", "^ [yes|yeah] i feel that|you $", "^ felt $"],
       "the user says it is the same for them (me too, same)",
       yes=["same", "me too", "same here", "me neither lol", "lol same", "relatable", "so do i", "same tbh", "i feel u",
            "yea i feel that", "felt"],
       no=["the same thing happened", "is it the same", "same as what", "say the same", "i feel that you are a bot"])

# ==== follow-ups: read in the light of what was said last ============================================================
intent("st_followup_really", ["^ [oh|wait] really $", "^ [oh|wait] really @laugh $", "^ [oh|wait] really since|why|how|that",
                              "^ [oh|wait] for real $", "^ [oh|wait] for real though $", "^ [oh|wait] seriously $", "^ [oh|wait] seriously @laugh $", "are you serious",
                              "you serious", "is that|it true", "^ no kidding", "^ [are] you sure $"],
       "surprise or doubt about the last thing said (really? for real?)",
       yes=["really?", "for real?", "seriously?", "are you serious", "wait really", "is that true", "fr?",
            "oh really lol", "you sure?"],
       no=["really good", "i really like that", "seriously i am human", "true story"])
intent("st_followup_since_when", ["^ since when", "^ how long $", "^ how long @laugh $", "^ for how long", "how long has it been",
                                  "how long have you had it|that", "how long ago", "when did that|it start|begin|happen"],
       "asks since when or for how long (about the last thing said)",
       yes=["since when?", "how long?", "for how long", "how long has it been", "how long ago", "when did that start",
            "since when lol"],
       no=["how long is your commute", "how long have you worked there", "since i was a kid"])
intent("st_followup_like_it", ["you like|enjoy|love it|that $", "you like|enjoy|love it|that @laugh $", "is it|that [@intens] @st_evaladj $",
                               "is it|that [@intens] @st_evaladj @laugh", "is it any good", "^ how is it $", "what is it|that like $",
                               "what is it|that like for you", "what is it|that like @laugh"],
       "asks what the last thing mentioned is like: fun, hard, liked",
       yes=["do you like it?", "is it fun", "is that hard", "do you enjoy it", "is it any good", "is it boring lol",
            "how do you like it", "what is it like?", "whats that like", "what is that like for you"],
       no=["do you like it there", "i like it", "is it raining", "do you like pizza", "what is it like there",
           "what is it"])
intent("st_followup_what_kind", ["^ [like|but] what|which kind|type|sort $", "^ [like|but] what|which kind|type|sort @laugh $", "^ [like|but] what|which kind|type|sort of $", "^ which one $", "^ which one @laugh $",
                                 "^ [and|so] which ones $", "^ which ones @laugh $", "^ what ones $"],
       "asks what kind of the last thing mentioned",
       yes=["what kind?", "what kind of", "what type?", "which one", "like what kind", "what sort lol", "which one?",
            "so which ones?", "what ones"],
       no=["what kind of dog", "which one is the bot", "kinda", "what kind of music do you like"])
intent("st_followup_tell_more", ["tell me more", "^ go on $", "^ and then $", "^ elaborate", "^ how so", "in what way",
                                 "say more", "keep going", "^ what else $", "^ what else @laugh $", "^ and $", "^ like what",
                                 "^ such as", "for example $", "^ example $", "give me an example", "^ name one"],
       "asks for more about the last thing said, or an example",
       yes=["tell me more", "go on", "and then?", "elaborate", "how so", "what else?", "and?", "like what?",
            "such as?", "give me an example"],
       no=["go on then ask me", "and then i left", "what else do you do", "i like what you said"])
intent("st_followup_what_happened", ["what happened", "what is wrong $", "what is wrong @laugh",
                                     "what is wrong with it|that|him|her|your", "what is the matter", "what went wrong",
                                     "is everything okay|alright", "^ uh oh"],
       "asks what happened (after something bad was mentioned)",
       yes=["what happened?", "what's wrong", "uh oh what happened", "is everything ok", "what went wrong",
            "whats the matter"],
       no=["what is wrong with you", "nothing happened", "what happens next", "everything is okay"])
intent("st_followup_where", ["^ where $", "^ where @laugh $", "^ where at", "^ where exactly", "where is that|it $", "^ where was it|that $",
                             "where is that at"],
       "asks where (about the last thing said)",
       yes=["where?", "where at", "where is that", "where exactly", "whereabouts", "where is it?", "where was that?"],
       no=["where are you from", "where is the bathroom", "where do you live", "where is that from"])
intent("st_followup_when", ["^ when $", "^ when @laugh $", "when was that|this $", "when is it|that $", "^ what time $",
                            "^ what day $", "^ how soon", "^ when exactly"],
       "asks when (about the last thing said)",
       yes=["when?", "when was that", "when is it", "what time?", "what day", "when exactly", "how soon"],
       no=["what time is it", "when were you born", "when do you work"])
intent("st_followup_who", ["^ who $", "^ who @laugh $", "^ who is that|she|he", "^ who are they|those", "^ with who|whom",
                           "^ who with", "^ like who"],
       "asks who (about the last person mentioned)",
       yes=["who?", "who's that", "who is she", "with who?", "who with", "like who", "who are they"],
       no=["who are you", "who is the president", "who am i", "who is this"])
intent("st_followup_how_old", ["^ [wait] how old $", "^ [wait] how old @laugh $", "how old is he|she|it|that|this", "how old are they|those",
                               "^ what age $"],
       "asks how old the last person or thing mentioned is",
       yes=["how old?", "how old is she", "how old is he", "how old is it", "how old are they", "what age?"],
       no=["how old are you", "how old is your sister", "how old do you think i am"])
intent("st_followup_whats_its_name", ["what is his|her|their name", "what is it is name", "what are their name",
                                      "what is it|that called", "what is he|she called"],
       "asks the name of the last person, pet or thing mentioned",
       yes=["what's its name?", "what is her name", "whats his name", "what is it called", "what are their names",
            "what's that called"],
       no=["what is your name", "what is my name", "her name is luna", "what is it"])
intent("st_followup_how_was_it", ["^ how was it|that $", "^ how was it|that @laugh $", "how did it|that go", "was it fun|good|nice|cool|bad",
                                  "was it worth it", "did you have fun", "did you enjoy it"],
       "asks how the last thing mentioned went",
       yes=["how was it?", "how did it go", "was it fun", "did you have fun", "how was that", "did you enjoy it"],
       no=["how is it", "how was your day", "have fun", "was it you"])

# ==== one detail deeper, from the dev games: what interrogators ask after the first answer =============================
cls("st_snack", "chips crisps snack snacks candy cheetos doritos pringles lays", "a snack food")
cls("st_platform", "pc console xbox playstation ps5 ps4 switch nintendo mobile phone", "a gaming platform")

# work and school: the part of it, the money, how he got there
intent("st_ask_worst_part", ["what is the worst|hardest|toughest|most_annoying|most_boring part|bit",
                             "worst|hardest|toughest part|bit [of|about] it|that|this|your|the_job|work|school",
                             "what do you hate [the] most about it|that|your_job|your_work|the_job|work|school"],
                             "asks the worst or hardest part of the thing just talked about (the job, school)",
       yes=["what's the toughest part", "worst part of ur job?", "what do u hate most about it",
            "whats the most annoying part", "hardest part about school?"],
       no=["the worst part is i lost my keys", "my job is the worst", "worst day ever", "what is the worst movie",
           "what is the best part"])
intent("st_ask_best_part", ["what is the best|favorite|fun|funnest|easiest part|bit",
                            "best|favorite|easiest part|bit [of|about] it|that|this|your|the_job|work|school",
                            "what do you like [the] most about it|that|your_job|your_work|the_job|work|school"],
       "asks the best part of the thing just talked about (the job, school)",
       yes=["whats the best part", "favorite part of ur job", "what do u like most about it", "whats the easiest bit",
            "best part about school?"],
       no=["the best part is the food", "what is the best movie", "what is the worst part", "you are the best"])
intent("st_ask_money_or_enjoy", ["just|only for the money", "for the money or", "or [is] [it] just|only [for] the money",
                                 "or [is] [it] just|only a paycheck", "enjoy|like it or [is] [it] just|only",
                                 "you do it for the money"],
       "asks whether Helmus works only for the money or likes it",
       yes=["is it only for the money", "do u like it or is it just a paycheck", "you do it for the money right",
            "enjoy it or only the money?"],
       no=["i do it for the money", "how much money do you make", "money is tight", "do you like it"])
intent("st_ask_how_got_job", ["how did you end up working|doing there|that|it", "how did you get [that|the|your] job",
                              "how did you get into that|it", "why did you pick|choose that|this|the job|store",
                              "why that job", "how did you get hired", "how did you start working there"],
       "asks how Helmus came to have its job",
       yes=["how did u get that job", "how did you end up working there", "how did you get into that",
            "why did you choose that job", "how did u get hired"],
       no=["how did you end up here", "how did you get here", "why did you pick that name", "i got hired"])
# games
intent("st_ask_play_games", ["you play anything", "you play [any|video] games", "you game", "you a gamer",
                             "what do you play", "what games [do] you play", "you into games|gaming",
                             "you play anything yourself"],
       "asks whether Helmus plays anything (games, or a sport after sports talk)",
       yes=["do you play any games", "u a gamer?", "what games do u play", "you into gaming", "what do u play"],
       no=["i play games", "do you play guitar", "what sports do you play", "lets play a game"])
intent("st_ask_platform", ["what|which platform", "pc or [a] console|xbox|playstation|ps5|switch",
                           "console|xbox|playstation|ps5|switch or [a] pc", "xbox or [a] playstation|ps5",
                           "what do you play on", "you play on [the] @st_platform",
                           "you have [a|an] xbox|ps5|ps4|playstation|switch|console"],
       "asks what Helmus plays on (pc, console), or which platform",
       yes=["which platform?", "pc or console", "what do u play on", "do you play on xbox", "u have a ps5?"],
       no=["i play on pc", "my pc is slow", "pc stands for personal computer"])
intent("st_ask_game_rank", ["your rank", "what rank", "you ranked", "you play ranked", "your elo",
                            "how good are you at valorant|it|games|minecraft"],
       "asks Helmus's rank or how good it is at its game",
       yes=["what rank are u", "whats your rank in valorant", "do you play ranked", "how good are u at it"],
       no=["rank these", "my rank is gold", "what is your favorite game"])
intent("st_followup_good_at", ["you any good", "^ [are] you good at it|that", "are you [any] good at it|that",
                               "^ any good at it|that",
                               "you good at it|that"],
       "asks whether Helmus is good at the thing just mentioned",
       yes=["are u any good", "you good at it?", "are you good at that", "any good at that?"],
       no=["are you good", "you are good at this", "what are you good at"])

# food
intent("st_ask_usual_food", ["go [-] to meal|food|dinner|lunch|dish", "lazy meal|dinner|food|lunch",
                             "you eat|make|cook when you_are|your lazy", "what do you [usually] eat",
                             "what do you eat [the] most|every_day", "comfort food", "your usual meal|order"],
       "asks what Helmus usually eats, its go-to or lazy meal",
       yes=["what's your go to food", "what do u usually eat", "whats ur comfort food", "what do u make when ur lazy",
            "what do you eat the most"],
       no=["what did you eat", "i eat when i am bored", "what do you want to eat", "i am lazy"])
intent("st_ask_fav_snack", ["favorite flavor", "favorite @st_snack", "@st_snack brand",
                            "kind|type|brand of @st_snack", "what @st_snack [do] you", "go [-] to snack", "your snack"],
       "asks Helmus's favourite snack, chips or flavour",
       yes=["whats ur favourite flavour", "favorite chips?", "what kind of chips do u like", "best crisps brand", "what snacks do you like",
            "whats ur go to snack"],
       no=["i like chips", "snack time", "what is your favorite food"])
# music
intent("st_ask_last_song", ["last song [you] [listened|heard|played|liked]", "last thing you listened to",
                            "what song [are] you listening|playing", "song [is] stuck in your head",
                            "what are you listening to right now", "what was the last song"],
       "asks the last song Helmus listened to",
       yes=["what was the last song u played", "what song are you listening to", "got a song stuck in your head",
            "last thing u listened to?"],
       no=["i love this song", "what is your favorite song", "sing me a song"])
intent("st_ask_concerts", ["you [ever] go to concerts|gigs|shows|festivals|concert|gig",
                           "you [ever] been to a|any concert|concerts|gig|gigs|festival|festivals",
                           "^ [ever] been to a|any concert|concerts|gig|gigs|festival|festivals",
                           "the|your first|last concert|gig", "seen anyone|anybody live", "concerts|gigs much"],
       "asks whether Helmus goes to concerts",
       yes=["do you ever go to concerts", "been to any gigs", "whats the last concert you went to",
            "have you seen anyone live"],
       no=["i went to a concert", "i love live music", "this is a show"])
intent("st_ask_best_one", ["best|worst one [you] [have] [ever] been|seen|had|went|played",
                           "^ [and] [the] best|worst one $", "best|worst|favorite concert|gig|show you"],
       "asks the best or worst one of the things just mentioned (a concert, a trip)",
       yes=["best one u have been to?", "worst one you ever had", "best one?", "favorite concert you went to"],
       no=["you are the best one", "the best one is pizza", "which one is the best"])

# sleep
intent("st_ask_what_keeps_up", ["what keeps you up|awake", "why do you stay up [so] late",
                                "why are you [always] [up|awake] so late", "why do you sleep so late",
                                "what do you do [up] so_late|all_night"],
       "asks what keeps Helmus up late",
       yes=["what keeps u awake", "why do u stay up so late", "why are you always up so late",
            "what do you do all night"],
       no=["what keeps you going", "i stay up late", "why are you here"])

# home
intent("st_ask_garden", ["you grow anything|stuff", "you grow [any] plants|vegetables|veggies|food|flowers|tomatoes",
                         "you [have] [a] garden", "you like gardening", "you have a [back] yard", "you have a backyard",
                         "you have [any] plants", "any plants"],
       "asks whether Helmus gardens or grows anything",
       yes=["do you have a garden", "u grow any vegetables?", "do you have plants", "do u have a backyard"],
       no=["i grow tomatoes", "my garden is nice", "grow up"])
intent("st_ask_neighbors", ["your neighbors|neighbor", "any neighbors", "know your neighbors",
                            "neighbors you chat|talk", "you talk|chat to|with [your] neighbors"],
       "asks about Helmus's neighbours",
       yes=["do u know your neighbours", "what are your neighbors like", "any neighbors u talk to"],
       no=["my neighbors are loud", "love thy neighbor"])

# sports
mem("st_sports_talk", {"U:st_ask_watch_sports": 1.0, "U:fo_ask_sports_opinion": 1.0, "U:ks_ask_team_season": 1.0},
    "the user has been asking about sports this turn or the last few ('u play anything urself' then means a sport)",
    decay=0.8)
intent("st_ask_watch_sports", ["you watch [any] sports|sport", "you into sports", "you follow [any] sports",
                               "you do [any] sports|sport",
                               "you a sports fan|guy|person", "you like sports", "you watch much sports"],
       "asks whether Helmus watches sports",
       yes=["do you watch sports", "u into sports?", "are you a sports guy", "do u follow any sports",
            "do you do any sport"],
       no=["i watch sports", "sports are boring", "what sports do you play"])
# hometown: how people talk there (a dialect probe)
intent("st_ask_local_slang", ["people from|in your area|town|city|state|there say", "something people [there|here] say",
                              "local slang|saying|sayings|word|words", "say that others|other_people do not",
                              "words only people from", "what do you call * $", "you have an accent", "your accent"],
       "asks what people where Helmus lives say, its slang or accent, or what it calls something",
       yes=["any local slang where u live", "what do people in ur state say that no one else does",
            "what do u call a sub sandwich", "do you have an accent"],
       no=["what do you call a fish with no eyes", "people say i am weird", "what do you call your mom when she is mad"],
       unless=["ask_name"])
intent("st_followup_use_it", ["use it in a sentence", "how do you use it", "say it in a sentence", "use that in a sentence"],
       "asks Helmus to use the word it just said in a sentence",
       yes=["how do u use it", "use that in a sentence then", "say it in a sentence"],
       no=["how do you use a microwave", "i use it every day"])

# who: the surname
intent("st_ask_surname", ["your surname|lastname", "your last|family name", "^ [and] [your] surname $",
                          "what is your last name"],
       "asks Helmus's surname",
       yes=["whats ur surname", "and your family name?", "surname?", "what is ur last name"],
       no=["my surname is smith", "what is your name", "last name first"])

# family
intent("st_ask_have_kids", ["you have [any] kids|children", "you have a kid|child|baby|son|daughter", "you got [any] kids", "^ got [any] kids",
                            "you a dad|father|parent", "^ any kids"],
       "asks whether Helmus has children",
       yes=["do you have children", "got any kids?", "are you a dad", "any kids?"],
       no=["do you want kids", "i have kids", "kids are annoying"])
intent("st_followup_get_along", ["you [all|guys] get along", "you get along with them|him|her|everyone|each_other",
                                 "you close with them|him|her", "you [all|guys] close"],
       "asks whether Helmus gets along with the people just mentioned",
       yes=["do u guys get along", "you get along with them?", "are you close with her"],
       no=["get along with your family", "we get along", "i get along with everyone"])
intent("st_followup_who_named", ["who picked|chose|named it|that|those|them|him|her",
                                 "who came up with it|that|the_name", "where did the name come from",
                                 "why that name", "how did you pick|choose the name", "why is he|she|it called"],
       "asks who chose the name just mentioned (a pet's name)",
       yes=["who named him", "who came up with that", "where did the name come from", "why that name"],
       no=["who named the city", "i named him", "whats his name"])

# relationships and friends
intent("st_followup_how_meet", ["how did you [guys|two|all] meet", "how did you meet them|him|her|each_other",
                                "where did you meet them|him|her", "how do you know them|him|her",
                                "how did you [guys] become friends"],
       "asks how Helmus met the people just mentioned",
       yes=["how did u guys meet", "how do you know them", "where did you meet him", "how did you become friends"],
       no=["nice to meet you", "how do you know that", "where did you meet"])

# films and shows
intent("st_followup_whos_in_it", ["who is in it|that|the_movie|the_film|the_show", "who stars in it",
                                  "who plays in it", "who is the main character|actor", "who are the actors"],
       "asks who is in the film or show just mentioned",
       yes=["who stars in it", "who is in the movie", "who are the actors", "whos the main actor"],
       no=["who is in charge", "who is it", "who is in your family"])
mem("st_movie_talk", {"F:w:film": 1.0, "F:w:films": 1.0, "F:w:movie": 1.0, "F:w:movies": 1.0},
    "a film came up in the user's message, a turn or two ago", decay=0.7)
mem("st_show_talk", {"F:w:show": 1.0, "F:w:shows": 1.0, "F:w:series": 1.0, "F:w:tv": 1.0, "F:w:netflix": 1.0},
    "a tv show came up in the user's message, a turn or two ago", decay=0.7)

# social media
intent("st_ask_who_follow", ["who do you follow", "who are you following", "accounts [do] you follow",
                             "who do you watch [mostly]", "who do you watch on"],
       "asks who Helmus follows or watches online",
       yes=["who do u follow", "what accounts do you follow", "who do u watch mostly", "who do you watch on youtube"],
       no=["follow me", "i follow a lot of people", "who do you think is the bot"])
intent("st_ask_last_post", ["last thing you posted", "your last post|story|tweet", "what do you post",
                            "you post [a_lot|much|often|anything|stuff]", "when did you last post",
                            "last time you posted"],
       "asks what Helmus last posted online",
       yes=["what was ur last post", "do you post much", "when did u last post", "what do you post"],
       no=["i posted a pic", "post office", "i never post"])

