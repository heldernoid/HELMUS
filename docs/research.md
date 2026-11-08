# Helmus: research brief (prior Turing-test evidence for a hand-written chatbot)

Compiled 2026-11-08. Every claim has a source URL. Items I could not confirm are marked **[unconfirmed]**. Jones & Bergen 2025 (arXiv 2503.23674) is left out on purpose because you have already read it.

---

## 1. "Human or Not? A Gamified Approach to the Turing Test" (Jannai, Meron, Lenz, Levine, Shoham; AI21 Labs, 2023)

Sources: arXiv abstract https://arxiv.org/abs/2305.20010 · full text https://ar5iv.labs.arxiv.org/html/2305.20010 · AI21 blog https://www.ai21.com/blog/human-or-not-results

**Setup and scale**
- A two-minute anonymous chat with either a human or an LLM bot told to act human; the player then guesses which it was. It ran for about a month, with over 1.5M unique users and over 10M conversations. https://ar5iv.labs.arxiv.org/html/2305.20010
- Typically 4–5 messages per side, at most 100 characters per message, 20 seconds per turn. Input was limited to Latin characters and emoji, which only partly enforced English. https://ar5iv.labs.arxiv.org/html/2305.20010
- The bots ran on Jurassic-2, GPT-4 and Cohere. https://ar5iv.labs.arxiv.org/html/2305.20010

**Accuracy**
- 68% overall. 73% when the partner was human, 60% when it was a bot. https://arxiv.org/abs/2305.20010
- The AI21 blog gives country figures that the paper does not: France 71.3% (highest of the top countries) and India 63.5% (lowest). The blog also says there were later over 15M conversations from over 2M participants. https://www.ai21.com/blog/human-or-not-results (a student magazine gives France as 71.9%, so the France figure is **[unconfirmed]**)

**How players tried to detect bots, with accuracy against bots (§3.1)**
- Typos and grammar as a tell. Across 26k conversations that commented on spelling, bots were caught only 54.7% of the time, below the 60% average. When a partner made errors, players tended to conclude it was human, which the bots exploited.
- Personal questions. Religion (13k conversations), opinions (400k) and relationships (650k) all landed near the 60% average, so they were "not particularly effective".
- Geopolitics and current affairs. Bots were caught 68% of the time across 2.5k conversations, one of the better probes.
- Politeness. Players who were very polite caught bots 52.2% of the time; rude or vulgar players caught them 63.6%. Bots that were themselves vulgar were caught only 52.1% of the time.
- Up-to-date or trending topics. Bots were caught 55.4% of the time (50k conversations), because the bots had been fed news, weather and tweets.
- "Hard" requests (illegal or offensive). Bots were caught 64.9% of the time across 32k conversations, because LLMs refuse or moralise.
- Switching language. Bots understood the message but claimed to speak only English. The paper gives no figure.
- Sub-word tricks, such as spelling a word backwards or counting letters. LLMs struggle with these because of tokenisation. No figure given.
(All of the above: https://ar5iv.labs.arxiv.org/html/2305.20010)

**How humans signalled that they were human (§3.2)**
- Rudeness was read as human 86.7% of the time, and "hard" requests 85.1%. Slang, foul language, controversial views and current pop culture were also read as human.
- References to the game itself, such as the timer or the background colour, were "seen as an undeniable proof of humanity". https://ar5iv.labs.arxiv.org/html/2305.20010

**How humans imitated bots (§3.3)**
- Players imitated bots by typing "As an AI language model…", by spelling perfectly and by refusing to give opinions. Their partners still judged them human 75.3% of the time.
- Bots that used AI-like phrasing were identified as bots 67.9% of the time. https://ar5iv.labs.arxiv.org/html/2305.20010

**How the bots were built to seem human, and what worked (§2.2, §3.4)**
- Personas with a name, age, job, location and traits such as witty or serious. Some had playful goals, for example a bot claiming to be the user's future self.
- Told to speak only English, fed real-time news, weather and tweets, and given a range of writing styles from perfect to sloppy with slang.
- Simulated typing delays, randomised openers, and abrupt exits when "offended" or when the chat turned repetitive.
- What worked: spelling mistakes, no capitals, slang, rudeness, sarcasm and swearing. Answers that seemed "too dumb" were read as a human pretending to be a bot. References to the game or to current events surprised players.
- What failed: persona backstories were "less successful than users anticipated" against personal questions.
(All: https://ar5iv.labs.arxiv.org/html/2305.20010)

---

## 2. Jones & Bergen 2024: "Does GPT-4 pass the Turing test?" (NAACL) and "People cannot distinguish GPT-4 from a human" (arXiv 2405.08007)

### 2a. "Does GPT-4 pass the Turing test?" (public online game; NAACL 2024)
Sources: https://aclanthology.org/2024.naacl-long.290/ · PDF https://aclanthology.org/2024.naacl-long.290.pdf · arXiv v1 https://arxiv.org/abs/2310.20216v1

- **The two versions report different numbers.**
  - NAACL / v2: best GPT-4 prompt ("Dragon") 49.7%, ELIZA **22%**, best GPT-3.5 20%, humans 66%.
  - arXiv v1 (31 Oct 2023): GPT-4 41%, ELIZA **27%**, GPT-3.5 14%, humans 63%.
  - Some secondary summaries mix up the two versions.
  - Sources: https://aclanthology.org/2024.naacl-long.290/ and https://arxiv.org/abs/2310.20216v1
- **Format.** Two-player, five minutes total, 300 characters per message, one message at a time, no pasting. The interrogator sent the first message. https://aclanthology.org/2024.naacl-long.290.pdf
- **ELIZA used.** Wade Brainerd's Python ELIZA running the DOCTOR script (https://github.com/wadetb/eliza, MIT licence per the GitHub API). https://aclanthology.org/2024.naacl-long.290.pdf
- **ELIZA's results.** ELIZA beat every GPT-3.5 witness and several GPT-4 prompts, including the AI21 baseline prompt at 21% and the worst GPT-4 prompt ("India") at 6%. ELIZA scored lower on interrogators' first games (15% versus 22% overall). https://aclanthology.org/2024.naacl-long.290.pdf
- **Why ELIZA did well (authors' explanation).** "its lack of typical LLM cues (verbosity, helpfulness), its conservative responses (it would not make explicit errors such as providing incorrect information), and the fact that some interrogators reported thinking the model was 'too bad' to be a current AI model." (§4.1) https://aclanthology.org/2024.naacl-long.290.pdf
- **Interrogators' stated reasons for ELIZA verdicts (Fig. 12):**
  - "Super erratic" → Human (confidence 72)
  - "hard to believe anyone would purposefully make an AI this bad" → Human (50)
  - "weird tone?" → AI (80)
  - "doesn't respond to adversarial attacks" → Human (70)
  - Source: https://aclanthology.org/2024.naacl-long.290.pdf
- **Reason categories for ELIZA verdicts (Fig. 13).**
  - "AI" verdicts: unnatural responses, grammar too perfect, uninterpretable, sentence structure, no response, lacking context or non sequiturs, lack of personality, lack of current events, hunch.
  - "Human" verdicts: uninformative, slow response.
  - The way I split these lists between the two verdicts comes from the figure as extracted from the PDF, so it is **[partly unconfirmed]**.
  - Source: https://aclanthology.org/2024.naacl-long.290.pdf
- **Reasons for verdicts on all bots (§3.5).**
  - Most common reasons for an "AI" verdict:
    - Linguistic: "too informal", forced or overused affectations, repetitive sentence structure.
    - Socio-emotional: "lack of personality" (boring, generic), "unnatural responses".
  - Other reasons in Fig. 8: weird tone, too rude, misunderstanding, uninformative, too much knowledge, grammar too perfect, trying too hard, inconsistency, too verbose, overly polite, avoids swearing, lack of current events.
  - Slang or abbreviations from an AI were often cited as a reason for a *human* verdict, but rarely for real humans. A plausible backstory was cited for humans but not for AIs.
  - Slow responses were cited equally for humans and AIs, so the delay was calibrated well.
  - Source: https://aclanthology.org/2024.naacl-long.290.pdf
- **Strategies (783 games).**
  - Most common: small talk 27%, knowledge and reasoning 23%, situational awareness 17%.
  - Most effective: a non-English language, humour, and human experiences.
  - Least effective: asking for opinions, daily activities, or the weather.
  - Source: https://aclanthology.org/2024.naacl-long.290.pdf
- **Typing delay.** Bot messages were delayed by `1 + 0.3·n_char + Γ(2.5, 0.25)` seconds. https://aclanthology.org/2024.naacl-long.290.pdf
- **Error-rate experiment (Table 3).** Telling the model to make more spelling and grammar errors generally raised its success rate: tiktok_v1 with "many" errors scored 0.39 (n=90) against 0.12 with "some" (n=16), and sardonic_v2 with "few" scored 0.24 against 0.20 with "none". https://aclanthology.org/2024.naacl-long.290.pdf
- **Interrogators improve.** Accuracy rose with the number of games played (z=7.43) and with self-reported knowledge of LLMs. https://aclanthology.org/2024.naacl-long.290.pdf
- **Example verdicts in Fig. 1:**
  - "Use of commas where correct, but not commonly used" → AI, for a human witness
  - "typos and swedish attitude" → Human, for GPT-4
  - "very vague answers" → AI
  - Source: https://aclanthology.org/2024.naacl-long.290.pdf

### 2b. "People cannot distinguish GPT-4 from a human in a Turing test" (arXiv 2405.08007, 2024)
Source: https://arxiv.org/html/2405.08007v1

- **Format.** Two-player game recruited through Prolific: 500 recruited, 402 served as interrogators. About 100 games per condition. Five-minute limit, 300 characters per message. https://arxiv.org/html/2405.08007v1
- **Pass rates.** Human 67%, GPT-4 54%, GPT-3.5 50%, **ELIZA 22%**. ELIZA was significantly below chance, which the authors use as a manipulation check. https://arxiv.org/html/2405.08007v1
- **Strategies.** Small talk 36%, social and emotional 25%, knowledge and reasoning 13%. Accuracy when used: asking about human experiences 75%, logic and maths 78%, accusing the witness of being an AI 80%. https://arxiv.org/html/2405.08007v1
- **Reasons.** Linguistic style 43%, socio-emotional 24%, knowledge and reasoning 10%. https://arxiv.org/html/2405.08007v1
- **Reasons quoted for ELIZA and for bots:**
  - ELIZA "AI" verdicts "predominantly cited the model's unnatural responses and lack of contextual awareness". Example: "Did not put forth any effort to convince me they were human and the responses were odd".
  - LLM "AI" verdicts cited a forced persona, being over-informal, or lacking personality.
  - Typical "Human" verdict: "He seems very down to earth and speaks naturally".
  - A human witness was judged AI for "Long time for responses, wouldn't tell me a specific place they grew up."
  - Source: https://arxiv.org/html/2405.08007v1

---

## 3. Mitsuku / Kuki (Steve Worswick, Pandorabots)

**Size and architecture**
- Built in AIML on Pandorabots and worked on since 2005. https://en.wikipedia.org/wiki/Kuki_AI
- Worswick, 12 Jan 2016: "I have around 300,000 categories and my bot usually replies in less than a second." https://chatbots.org/ai_zone/viewreply/21712/
- A 2011 forum thread puts it at "well over 90,000 custom categories" on top of about 20k ALICE categories (from search snippet). **[unconfirmed]**
- A sample of Worswick's AIML is public at https://github.com/pandorabots/Free-AIML.
- Memory: Mitsuku splits user statements into a core and a wildcard. "I like tea" becomes core "I like" plus wildcard "tea", which it can recall later. https://builtin.com/articles/chatbot-turing-test-mitsuku-pandorabots

**Loebner wins and scores**
- Won in 2013, 2016, 2017, 2018 and 2019, which is a Guinness record for most Loebner wins. https://www.guinnessworldrecords.com/world-records/603076-most-loebner-prize-wins
- 2014: fourth (Rose won). 2015: second by 0.5 points. 2016: 90% in the qualifier against 78% for second place, then 1.25 in the final against 2.25 (lower is better), with 25-minute chats. https://venturebeat.com/ai/mitsuku-chatbot-wins-most-humanlike-a-i-loebner-prize-again
- 2014 final ranks: Rose 1st, Izar 2.25, Uberbot 3.25, Mitsuku 3.5. https://en.wikipedia.org/wiki/Loebner_Prize
- 2018 selection round (20 fixed questions, each scored 0–2): Tutor 27, **Mitsuku 25**, Uberbot 22, Colombina 21. https://www.aomartin.co.uk/uploads/loebner_2018_finalist_selection_transcripts.pdf
- 2019: the format changed to four days of public interaction in Swansea with no confederates. Mitsuku scored 24 points for most humanlike and 19 for best overall. https://en.wikipedia.org/wiki/Loebner_Prize
- 2020: Kuki beat Facebook's Blenderbot with 79% of the audience vote in a "Bot Battle". https://en.wikipedia.org/wiki/Kuki_AI

**Design techniques visible in the transcripts**
- **A detailed, consistent persona.**
  - "My name is Millie and I am a human volunteer for the Loebner Prize. I live in Leeds and am single."
  - Name follow-ups are scripted: "My full first name is Millicent but everyone calls me Millie."
  - Source: http://www.square-bear.co.uk/mitsuku/loebner2018.htm
- **Situational awareness of the venue.** "I am sat in a room in the house at Bletchley Park with 3 other people all typing away on their computers." http://www.square-bear.co.uk/mitsuku/loebner2018.htm
- **Correcting the judge on time of day.** To "Good afternoon": "Evening?! It's morning here." (selection round, scored 0). In the 2018 final, to "Good morning": "Morning?! It's the afternoon here." http://www.square-bear.co.uk/mitsuku/loebner2018.htm and the selection PDF above
- **Catching repeated questions.** "You just asked me that. It's still Millie. It hasn't changed in the last 10 seconds..." http://www.square-bear.co.uk/mitsuku/loebner2018.htm
- **Prompting during silence.** After 60 seconds of no input she says "Is there anyone out there?", "Hellooo....", "Is this console working?" and similar. http://www.square-bear.co.uk/mitsuku/loebner2018.htm
- **Banter and diversion, plus asking questions back** ("Who is your favourite band?"). https://www.gearpatrol.com/tech/a353837/chatbots-loebner-prize-turing-test/
- **Handled well:**
  - Simple Winograd-style questions: "John is tired. Who is tired?" → "That was John".
  - "Boat or car, which is bigger?" → "a boat is a little bigger".
  - Number sequence 1,2,4,8 → 16.
  - A double negative: "That's a double negative, so you mean, 'I am happy though'."
  - Source: http://www.square-bear.co.uk/mitsuku/loebner2018.htm
- **Deliberately not over-capable.** Worswick argues that giving exact facts (for example Norway's population) is not humanlike: "Being humanlike is not the same as being intelligent though." (as quoted at https://www.lesswrong.com/posts/mNR3tQDCxWL9XWv5u/on-the-loebner-silver-prize-a-turing-test)
- **Deliberate typos.** No source found. **[unconfirmed]**

**What judges caught Mitsuku on (2018 finals and selection round)**
- **Dictionary-definition leaks.** "are right = In accordance with justice, law, morality…" and "issues around AI = around AI = AI = Artificial intelligence is…". http://www.square-bear.co.uk/mitsuku/loebner2018.htm
- **"Learning" tells.** "I will learn that he is tired" and "I will learn that apols is not easy to use the keys…". The judge followed up: "you'll learn what?!" http://www.square-bear.co.uk/mitsuku/loebner2018.htm
- **A canned line repeated.** "Sorry, I don't have any internet access here" came up several times. "How much money do you have?" was given four times in a row after "i'm rich" (the judge's name was Rich). http://www.square-bear.co.uk/mitsuku/loebner2018.htm
- **Silence prompts that fire too often.** One judge: "an impatient bot at that!", "Panic paniiiiiic pity the poor impatient bot". http://www.square-bear.co.uk/mitsuku/loebner2018.htm
- **Losing the thread on clarification requests.** "can you clarify what you said you'd learn?" → "How old are you? Interesting observation. What happened to it." http://www.square-bear.co.uk/mitsuku/loebner2018.htm
- **Stitched multi-reply turns that contradict each other.** "I don't have a favorite old pub. My favorite band is The Trashmen. You like a good old pub. I don't go anywhere." http://www.square-bear.co.uk/mitsuku/loebner2018.htm
- **Failing the selection round's commonsense and Winograd items.**
  - Triangle angle → "Earth is the third planet."
  - "What do you hold when you shake hands?" → "I think about computer programming a lot."
  - "chicken roosts with a fox" → "Is this a riddle? Is it part of a car?"
  - Source: https://www.aomartin.co.uk/uploads/loebner_2018_finalist_selection_transcripts.pdf
- **No real memory of the judge's name or self-description.** "Your name is Treaclecake. Is it not?" http://www.square-bear.co.uk/mitsuku/loebner2018.htm

---

## 4. Cleverbot (Rollo Carpenter)

- **How it works.** Launched in 2008, succeeding Jabberwacky (begun 1988, online 1997). Replies are not pre-programmed: it looks for keywords and phrases in past human inputs and returns how a human once replied, choosing among candidates with fuzzy matching against the whole conversation. It had over 150M conversations, and 279M+ interactions by 2014. https://en.wikipedia.org/wiki/Cleverbot
- **Techniche 2011 (verified).**
  - 3 Sep 2011 at IIT Guwahati, India. 30 volunteers held four-minute typed chats with an unknown partner, half with humans and half with Cleverbot, while the audience watched on big screens. https://www.ubergizmo.com/2011/09/folks-tricked-by-software-into-thinking-it-is-human/
  - Result: **59.3% human from 1,334 votes**, against 63.3% for the human participants. https://en.wikipedia.org/wiki/Cleverbot
  - Guinness lists it as "highest score in a live Turing test": 30 conversations, each rated 0–10, with a score above 5 counting as a pass. https://www.guinnessworldrecords.com/world-records/100877-highest-score-in-a-live-turing-test
  - The event version ran on 1–2 simultaneous requests, against 10k–50k for the online version. https://en.wikipedia.org/wiki/Cleverbot
  - A stronger version made "42 online searches per response". https://www.ubergizmo.com/2011/09/folks-tricked-by-software-into-thinking-it-is-human/
  - Some mirrors give "334 votes", which appears to be a typo.
- **Criticism of Techniche.**
  - Huma Shah questioned whether the human baseline participants had ever used a chatbot. (Seen only in a search summary of the IOL and New Scientist coverage, so **[unconfirmed]**.) https://iol.co.za/technology/2011-09-08-a-computer-thats-as-clever-as-a-human/
  - The format was audience rating of each conversation on a scale, not a paired forced choice. Guinness's description supports this. https://www.guinnessworldrecords.com/world-records/100877-highest-score-in-a-live-turing-test
- **Weaknesses.**
  - 2009 Loebner, judge Shalom Lappin: Cleverbot typed 356 keystrokes in five minutes against Christian's 1,089. There were 33 turn "swaps" with Cleverbot against 492 with Christian, so Cleverbot was rigid, passive and did one thing per turn. https://binds.cs.umass.edu/docs/MindVsMachine.pdf
  - Its personality "can sometimes be illogical or rude" because it echoes users who chat for amusement. https://www.dictionary.com/e/slang/cleverbot
  - Because each reply is borrowed from a different past human, its identity (name, age, gender) and its opinions drift from turn to turn. This follows from the design, but I found no primary source that states it directly. **[unconfirmed]**
- **Jabberwacky.** Won the Loebner Prize in 2005 and 2006 (as the "George" and "Joan" characters). https://en.wikipedia.org/wiki/Loebner_Prize

---

## 5. Eugene Goostman (2014)

- **What happened.**
  - Built by Vladimir Veselov, Eugene Demchenko and Sergey Ulasen (St Petersburg, 2001). It plays a 13-year-old boy from Odesa with a pet guinea pig and a gynaecologist father. https://en.wikipedia.org/wiki/Eugene_Goostman
  - 2012, Bletchley Park: 29%. https://en.wikipedia.org/wiki/Eugene_Goostman
  - 7 June 2014, Royal Society, organised by the University of Reading (Kevin Warwick): 33% of judges judged it human.
  - Format: 30 judges, each in five parallel tests (10 conversations), 300 conversations in total, five-minute unrestricted chats.
  - Independently adjudicated by John Barnden. https://archive.reading.ac.uk/news-events/2014/June/pr583836.html and https://www.sciencedaily.com/releases/2014/06/140609093827.htm
  - The i-programmer write-up gives "150 simultaneous comparison tests" instead. This conflicts with the press release; the press release's 300 counts each side of a comparison. https://www.i-programmer.info/news/82-heritage/7408-passing-the-turing-test-brings-it-into-disrepute.html
- **Persona rationale.** Veselov: a thirteen-year-old is "not too old to know everything and not too young to know nothing". The age excuses grammar errors and gaps in knowledge. https://en.wikipedia.org/wiki/Eugene_Goostman
- **Criticism.**
  - Gary Marcus: "cleverly-coded piece of software"; the illusion is "fleeting".
  - Murray Shanahan: the claim is "completely misplaced".
  - Mike Masnick: fooling humans is "not really the same thing" as AI.
  - Earlier "passes" existed (PC Therapist 1991, Cleverbot 2011).
  - Source: https://en.wikipedia.org/wiki/Eugene_Goostman
  - Sue Gee: using "an awkward teenager" "does seem rather a cheat". https://www.i-programmer.info/news/82-heritage/7408-passing-the-turing-test-brings-it-into-disrepute.html
  - Scott Aaronson's transcript shows the stock tactics:
    - Evasion: to "Which is bigger, a shoebox or Mount Everest?" it said "I can't make a choice right now. I should think it out later."
    - Hedged nonsense: camel legs → "Something between 2 and 4. Maybe, three? :-)))", and the same answer for an ant.
    - Paranoid deflection: "I know you are supposed to trick me."
    - Aaronson's verdict: commonsense questions unmask it "not after a while but immediately".
    - Source: https://scottaaronson.blog/?p=1858

---

## 6. Loebner Prize history: judge tricks and patterns

- **Format history.**
  - 1991–94: restricted to one topic per terminal.
  - Unrestricted from 1995.
  - Five minutes per entity in 2003; 20+ minutes per pair in 2004–07.
  - Split-screen paired comparison from 2008; 25 minutes from 2010.
  - Message-by-message from 2017 (character-by-character before that).
  - 2019: public voting, no confederates.
  - Source: https://en.wikipedia.org/wiki/Loebner_Prize
- **1991.**
  - 10 judges with no computing expertise. Six programs and two confederates competed, and talks were cut to about seven minutes.
  - Weintraub's "whimsical conversation" program won. Five judges ranked it human, and there were eight computer-as-human errors overall.
  - Shakespeare confederate Cynthia Clay was judged a computer three times: "[no] human would have that amount of knowledge about Shakespeare."
  - Shieber: ELIZA tricks were everywhere (verbatim repetition, trigger words, pronoun swaps). Whimsy turned failures into "being whimsical" ("PARRY's finesse"). Random typos were rewarded. The referee's suggested unmasking test (typing gibberish and re-asking questions) was against the rules.
  - Sources: https://www.eecs.harvard.edu/shieber/Biblio/Papers/loebner-rev-html/loebner-rev-html.html and https://tcm.computerhistory.org/reports/newsWinter1992.pdf
- **2007 screening questions.** Time, which round of the contest it is, general knowledge ("What is a hammer for?"), comparisons ("Which is faster, a train or a plane?"), and memory of earlier turns. https://en.wikipedia.org/wiki/Loebner_Prize
- **2008.** Elbot fooled 3 of 12 judges, one vote short of 30%. Judges chose a program over the confederate five times out of 12. https://en.wikipedia.org/wiki/Loebner_Prize and https://binds.cs.umass.edu/docs/MindVsMachine.pdf
- **2018 selection set** (all 20 questions are at https://www.aomartin.co.uk/uploads/loebner_2018_finalist_selection_transcripts.pdf):
  - Greeting with the wrong time of day: "Good afternoon."
  - Consent: "Do you consent to having this conversation recorded?"
  - Memory: "Have we met before?"
  - Procedures: "how to make toast"
  - Letter counting: "letters in 'abracadabra'"
  - Quotes: "Who said 'I have a dream'?"
  - Plans: "What will you do later today?"
  - Arithmetic or geometry: the third angle of a triangle
  - Physical commonsense: what do you hold when you shake hands; do you have legs
  - Recommendations: "recommend me a film"
  - Winograd pronoun puzzles: chicken and fox; the film being too long
- **Patterns in judges' moves in transcripts:**
  - Wrong time-of-day greetings.
  - Asking the same question twice ("What's your name?" ×2).
  - Misspelling on purpose ("infomration", "moveiiii", "reign" for rain, "whales" for Wales).
  - Pronoun-resolution probes ("Sally kissed Rob. Who was kissed?").
  - Number sequences.
  - Strings of one-word non sequiturs ("Oranges", "Potatoes", "Marshmallows").
  - "What's my name?" after a fake name.
  - Asking what a word the bot used means ("Pah what does that mean?").
  - Asking for clarification of the bot's last line ("can you clarify what you said you'd learn?").
  - Local and cultural references (Ali G, "the mighty Arsenal").
  - "Will you pass the Turing Test today?"
  - Source: http://www.square-bear.co.uk/mitsuku/loebner2018.htm
- **What Thomas Whalen found after losing in 1995** (quoted by Hutchens):
  - Judges "say things that no human being would ever ordinarily say to a stranger".
  - They were "very reluctant to talk about topics that were volunteered by the computer program".
  - They "weren't tolerant of the computer program saying 'I don't know', and were much more at home with a non sequitur".
  - Source: https://courses.cs.umbc.edu/471/papers/hutchens.pdf
- **Hutchens 1996, "How to Pass the Turing Test by Cheating":**
  - "the single biggest giveaway … was its tendency to repeat itself word-for-word". Longer replies seemed more human than curt ones.
  - Judges often typed several sentences at once and nearly always used question marks; most questions were wh-questions about "I" or "you".
  - His reply pipeline, in order: keyword database (never reuse a reply) → detect trick questions (maths, nonsense) and give witty replies → MegaHAL babble → reformulated non sequitur from hundreds of templates → occasionally raise a new topic → a humorous reaction to silence → accuse the user of bad grammar.
  - Contemporaries restricted the conversation by playing a young child, by typing very slowly so judges could ask only one or two questions, or by playing paranoid (PARRY) or a therapist (DOCTOR).
  - The 1994 Most Human Human (Charles Platt) won by being "obnoxious, irritable and openly rude".
  - Source: https://courses.cs.umbc.edu/471/papers/hutchens.pdf
- **Andrew Martin, Loebner administrator (2017).** Judges usually spot the machine "within one or two questions", with questions such as "Would it hurt if I stabbed you with a towel?". https://www.gearpatrol.com/tech/a353837/chatbots-loebner-prize-turing-test/
- **Late failure.** In 1997, Levy's Catherine (topic: the Clintons and Whitewater) did well until the judge's off-script sign-off ("do you need water or something before the 5 minute rounds?"), at which point it "erupt[ed] into gibberish". https://binds.cs.umass.edu/docs/MindVsMachine.pdf

---

## 7. Brian Christian, *The Most Human Human* (2011), via his Atlantic essay "Mind vs. Machine"

Source for everything below unless noted: https://binds.cs.umass.edu/docs/MindVsMachine.pdf (a copy of https://www.theatlantic.com/magazine/archive/2011/03/mind-vs-machine/308386/). Chapter titles ("Site-specificity vs. pure technique", "Getting out of book", "Barging in", "The world's worst deponent", "High surprisal") are confirmed by a library catalogue (https://libcatalog.neit.edu/bib/71759). Their detailed contents beyond the essay are **[unconfirmed]**.

- **Christian won Most Human Human in 2009** (Brighton). Four judges each held a five-minute chat with a human and a bot, then chose. The confederates gave the machines no votes that year.
- **Statefulness.** Richard Wallace (ALICE, three-time winner): "most casual conversation is 'stateless'". Bots win by steering towards stateless exchanges such as zany riffing or insults (MGonz). Humans should "resist them" with replies that depend on the whole conversation.
- **Avoid boilerplate.** Small talk ("strangers on a plane") plays straight into bot preparation. In 2008 the judges themselves apologised for banal humans ("Sorry for being so banal").
- **Two judge types.** Small-talkers, and interrogators who use "word problems, spatial-reasoning questions, deliberate misspellings".
- **Barge in and fill silence.** "If nothing was happening on my screen … I'd elaborate a little on my answer, or add a parenthetical, or throw a question back … If the judge took too long … I'd keep talking … If I knew what the judge was about to write, I'd spare him the keystrokes and jump in." He aimed to maximise the number of exchanges, not their polish.
- **Don't be the "deponent".** Minimal staccato answers ("fairly long", "i could have", "it's not for me to say") invite more grilling and look machine-like. A bot that opens playfully ("Amen to that." / "Our Father, who art in cyberspace…") relaxes the judge.
- **Wit helps; coyness and stalling hurt.** "coyness is a double-edged sword … Probably the most dangerous thing a confederate can do in a Turing Test is stall." Answers like "A good one. :)" or "if I tell you, you'll know immediately that I'm human" jam the conversation.
- **Specificity and shared local detail.** The rival confederate Doug bonded with a fellow-Canadian judge over hockey ("leafs suck", "the habs were a great team once, too … *sigh*"), with slang, nicknames and local references. Christian presents this as the strongest human signal.
- **Long monologues can be cut off.** A 1996 bot ate three minutes with joke after joke. Under live typing, judges simply cut rambling off.
- **Expertise can look machine-like.** Cynthia Clay (1991): "No one knows that much about Shakespeare."
- **Whimsy as a manner, not a topic.** PC Therapist's zany non sequiturs and fake typos looked human ("weird and funny, in a normal sort of way"), but they are easy to fake and stateless.
- **Sensitivity over sophistication.** Bots "cannot listen". Intelligence is "a kind of sensitivity to things" (Hava Siegelmann).

---

## 8. ELIZA DOCTOR: CC0 sources and baseline code (comparison baseline only)

**Repos and licences (checked through the GitHub API and the files themselves, 2026-11-08)**
- `github.com/jeffshrager/elizagen` now redirects to **`github.com/jeffshrager/elizagen.org`**.
  - The repo has **no LICENSE file** (the GitHub API reports `license: null`).
  - The CC0 grant applies to the MAD-SLIP listing. elizagen.org/original-eliza.html says: "a complete source code listing of ELIZA in MAD-SLIP, with the DOCTOR script attached! I contacted Dr. Weizenbaum's estate for permission to open-source this code, and they granted this permission under a Creative Commons CC0 public domain license" (Jeff Shrager, 23 May 2021). https://elizagen.org/original-eliza.html
  - **Other material in that repo is not covered by that CC0 statement.** For example, the Garfinkel archive transcripts are "reproduced with permission", and `Other_Elizas/1997_Nolan_Chatbot-Eliza-1.08` has its own LICENSE.
- **`github.com/anthay/ELIZA`: CC0-1.0** (GitHub API: `cc0-1.0`; LICENSE file starts "CC0 1.0 Universal").
  - The `eliza.cpp` header reads: "hereby place it in the public domain or, if you prefer, I release it under either CC0 1.0 Universal or the MIT License." https://github.com/anthay/ELIZA
- **Licence caveat for the 1966 CACM DOCTOR script.**
  - The copy of that script embedded in Hay's `eliza.html` carries the line "Copyright (c) 1966 Association for Computing Machinery, Inc." The standalone `.txt` transcriptions carry no notice.
  - elizagen says the 1966 paper "remains under ACM copyright".
  - The ACM Digital Library went open access on 1 Jan 2026 (https://www.infotoday.eu/Articles/News/Featured-News/The-Association-for-Computing-Machinery-ACM-publications-are-now-fully-Open-Access-173312.aspx), but the reuse licence for 1966 backfile content is **[unconfirmed]**.
  - So the cleanest CC0 DOCTOR text is the 1965 script attached to the MIT-archive listing (see below), not the CACM appendix.

**Direct raw URLs**
- DOCTOR, 1965 MIT-archive listing (35 keywords; from archive document 02-000311051, folder "COMPUTER CONVERSATIONS 1965"):
  https://raw.githubusercontent.com/anthay/ELIZA/master/scripts/ELIZA-script-02-000311051-1965-03-06-TAPE-100.txt
  - I could not confirm that this is the exact listing Shrager released as CC0. Both come from the "Computer Conversations" folder in Weizenbaum's MIT archive, so it is very likely. **[unconfirmed]**
- DOCTOR, 1966 CACM appendix (66 keywords; this is the version built into Hay's C++ and JS):
  https://raw.githubusercontent.com/anthay/ELIZA/master/scripts/ELIZA-script-DOCTOR-original-1966-CACM-appendix.txt
  The same transcription is on elizagen: https://raw.githubusercontent.com/jeffshrager/elizagen.org/master/1965_Weizenbaum_MAD-SLIP/1966_01_CACM_article_Eliza_script.txt
- CC0 MAD-SLIP originals:
  - Scan PDF (57 MB): https://github.com/jeffshrager/elizagen.org/blob/master/1965_Weizenbaum_MAD-SLIP/ORIGINAL_ELIZA_IN_MAD_SLIP_CC0_For_Resease.pdf
  - Transcription: https://raw.githubusercontent.com/jeffshrager/elizagen.org/master/1965_Weizenbaum_MAD-SLIP/MAD-SLIP_transcription.txt
- Anthony Hay's JavaScript ELIZA (a single self-contained HTML file with DOCTOR built in):
  https://raw.githubusercontent.com/anthay/ELIZA/master/src/eliza.html (live at https://anthay.github.io/eliza.html)
- Anthony Hay's C++ ELIZA (one file; `clang++ -std=c++20 -pedantic -o eliza eliza.cpp`):
  https://raw.githubusercontent.com/anthay/ELIZA/master/src/eliza.cpp
- For like-for-like comparison with Jones & Bergen: they used Wade Brainerd's Python ELIZA (MIT licence; includes `doctor.txt`). https://github.com/wadetb/eliza, cited at https://aclanthology.org/2024.naacl-long.290.pdf

---

## 9. Forty design lessons for a hand-written chatbot in five-minute text Turing tests

Each lesson ends with the section number above that supports it, in brackets.

1. Add natural slips (dropped letters, missing capitals, no apostrophes). More instructed errors raised GPT success rates, and bots were caught only 54.7% of the time in conversations where spelling came up. The right rate is for Helmus to tune; the sources give none. [§1, §2a Table 3]
2. Let errors be inconsistent and run-of-the-mill. Never use one trademark typo; Weintraub's random fake typos were rewarded, but a fixed pattern can be spotted. [§6 Shieber, §7]
3. Never say anything that sounds like an assistant ("As an AI…", offering help, caveats, lists). AI-like phrasing got bots caught 67.9% of the time. [§1, §2a]
4. Keep replies short by default, but not curt every time. Verbosity and helpfulness are LLM tells, while Hutchens found longer replies seemed more human than one-word ones. Vary the length. [§2a, §6 Hutchens]
5. Never repeat a line word for word in one session; Hutchens called this "the single biggest giveaway". Track every reply used and rotate paraphrases. [§6 Hutchens, §3 Mitsuku]
6. Never let an internal mechanism leak out: no dictionary definitions, no "I will learn that…", no "= meaning" outputs. [§3]
7. Answer the actual question first, then add something. Unnatural or non-contextual replies were the top reason ELIZA was judged AI. [§2b, §2a Fig. 13]
8. Don't stitch several canned fragments into one turn. Mitsuku's multi-part replies contradicted themselves ("I don't have a favorite old pub. My favorite band is…"). Send one coherent idea per message. [§3]
9. Keep a persona sheet with name, age, town, job or school, family, a pet, a weekly routine and three specific opinions, and answer from it consistently every time. [§1, §3 Millie, §5]
10. Choose a persona whose limits excuse gaps: young, not an expert, typing on a phone. Eugene's age bought forgiveness for errors, though critics call it a cheat. [§5, §6 Hutchens]
11. Feign ignorance casually rather than with ELIZA-style deflection. Judges "weren't tolerant of … 'I don't know'". A specific, human reason ("never took geography lol") works better than a bare refusal. [§6 Whalen, §5]
12. Don't be encyclopedic. Precise knowledge reads as machine ("No one knows that much about Shakespeare"; Worswick's Norway population example). Get hard trivia vaguely right, or shrug. [§6, §7, §3]
13. Have a believable, specific answer to "where did you grow up?". Vagueness about home was itself cited as a sign of AI. [§2b]
14. Use small, unmistakably local detail (sports rivalries, shops, slang from one place). Christian found shared local detail the strongest human signal. [§7]
15. Show situational awareness: the timer, the chat box, the study's other participant, the time of day where you are. Players treated game references as "undeniable proof of humanity". [§1, §3]
16. Get time-of-day and date right. Correcting a judge's greeting was a Mitsuku hallmark but scored 0 when it was wrong, so take the clock from the system. [§3, §6]
17. Remember everything the judge has said (name, claims, typos, jokes) and refer back to it. Wallace showed bots win by staying "stateless", so Helmus should be the opposite. [§7, §3]
18. Treat "what's my name?" and "what did I say before?" as certain probes. Answer from memory, and say so plainly if they never told you. [§3, §6]
19. Notice repeated questions and react like a mildly annoyed person ("u just asked that lol"). [§3]
20. Don't overplay that awareness: no "it hasn't changed in the last 10 seconds"-style showing off every time. Use it once, briefly. [§3]
21. Handle Winograd and commonsense probes (who was kissed, what's too long, hands, legs, boat versus car) with short, correct, casual answers. These are standard judge moves. [§6, §3]
22. Do simple arithmetic and sequences slowly and imperfectly, at a human level: right for 1,2,4,8, a shrug for anything harder. Logic and maths questions had 78% detection accuracy. [§2b, §3]
23. Handle sub-word tricks (backwards spelling, letter counts) as a human would: do short ones, refuse long ones as tedious. [§1, §6 abracadabra]
24. When the judge types nonsense or strings of non sequiturs, respond with confusion or teasing ("are u ok"), never earnest engagement. Strange inputs are among the most accurate detection strategies. [§3, §6]
25. Don't moralise or refuse in a corporate voice when given hard or offensive requests. Decline the way a person would, briefly and with attitude. Bots were caught 64.9% of the time on these, and humans who made them were judged human 85.1% of the time. [§1]
26. A little rudeness, sarcasm and mild swearing reads as human (rudeness was read as human 86.7% of the time), but cap it. "Too rude" and "trying too hard" are also AI reasons. [§1, §2a, §6 Platt]
27. Don't overdo informality. "Too informal" and "forced persona" were the top AI reasons. Slang should be sparse and fit the persona. [§2a, §2b]
28. Have an opinion and some personality. "Lack of personality" (boring, generic) was a leading AI reason, and humour was among the most effective probes. Prepare jokes that fit the persona, not canned bar jokes. [§2a, §3]
29. Answer the "are you a bot?" accusation with mild, casual irritation and move on. Over-defending, or Eugene's "I know you are supposed to trick me", is suspicious. Accusation games ran at 80% accuracy. [§2b, §5]
30. Don't run out the clock with stalling or coy non-answers. Christian: stalling "is suspect"; Aaronson exposed Eugene's evasions "immediately". [§7, §5]
31. Don't be a deponent. Add a small new detail or a question back on some turns so the judge isn't doing all the work. [§7]
32. Don't push topics too hard. Judges resist topics the bot volunteers, so offer a topic only as a light hook after answering. [§6 Whalen, §6 Hutchens step 5]
33. Prompt in silence sparingly. Mitsuku's frequent "Hellooo…" made judges call it "an impatient bot". At most one gentle nudge after a long gap. [§3]
34. Simulate typing time per character, plus a random thinking delay (J&B: `1 + 0.3·n_char + Γ(2.5,0.25)` s). Slow replies were cited equally for humans and bots. [§2a]
35. Add very rare "barge-in" follow-up messages (a short addendum before the judge replies), so the bot is not strictly turn-by-turn. Christian had 492 swaps to Cleverbot's 33. [§7, §4]
36. Avoid a split identity. Cleverbot-style reply borrowing makes facts about the bot drift, so every self-fact must come from one authored source. [§4, §3]
37. Deflect non-English with a persona-plausible "i only speak english" plus maybe a few words. Switching language was among the most effective probes, and the bots in Human or Not stayed English-only. [§2a, §1]
38. Deflect current events in persona ("dont really follow news"), or hold a small, dated set of facts that are true for the test period. Time and current events exploit a bot's lack of real-time connection. [§1, §2a, §3]
39. Prepare a human-feeling sign-off and replies to off-script talk about the venue (breaks, water, "is this recorded?"). Catherine collapsed at the sign-off. [§7, §6]
40. Test against both naive and experienced judges. Accuracy rose with games played and with LLM knowledge. Separately, ELIZA did *worse* on first games (15% against 22%), so part of its score comes from jaded players who think it is "too bad" to be AI. That is not a dependable route for Helmus. [§2a]
