# Helmus: design

Helmus is a chatbot meant to be judged human in 5-minute text chats more often than ELIZA (23% in the 2025
three-party Turing test of Jones & Bergen) and to hold its own against Cleverbot. Every weight, every rule, every
line it can say and every fact about the person it plays is written by hand, by a frontier model. There is no
training, no corpus, no outside chat log and no model running at chat time.

## What the target looks like (from Jones & Bergen 2025)

A game: an interrogator chats with a human and with Helmus at the same time for 5 minutes, then says which is human.
- **Length:** median 8 messages over 4.2 minutes, so Helmus answers about 4 times per game. Messages are at most
  300 characters and cannot be pasted.
- **What interrogators do:**
  - small talk, about daily life and personal details: 61%;
  - social and emotional probing, about opinions, feelings, humour and experiences: 50%;
  - asking outright "are you human?": 19%;
  - situational awareness, such as the time, the weather or the game itself: 13%;
  - knowledge and reasoning: 12%.
- **What catches bots best:** strange inputs and jailbreaks ("ignore all previous instructions"). Both are rare,
  but they are the most accurate tests.
- **Why judges decide:**
  - linguistic style (spelling, formality, phrasing): 27%;
  - the flow of the conversation (how questions are handled): 23%;
  - gut feeling.

  Knowledge is rarely the reason. The most accurate reasons are how questions were handled, and a lack of
  knowledge: a human does not know everything.
- **The persona that won 73% for GPT-4.5:**
  - a 19-year-old into internet culture and games;
  - introverted, chill, not trying hard to convince;
  - no wide world knowledge;
  - mostly under 5 words and under 30 characters, no full stops, no apostrophes;
  - slang like "fr" and "ngl", but not every message;
  - asks questions back, but not every time;
  - dry and a bit funny.
- **Typing delay:** messages arrive after about 1 s + 0.3 s per character of the reply + 0.03 s per character of the
  question + a skewed "thinking" pause.

This is good news for a hand-written bot. Short, plain, slightly evasive replies are exactly what a hand-written
phrasebook does well, and the things that expose LLMs (jailbreaks, being too helpful, knowing too much) are things a
hand-written bot does not do.

## The network

A sparse network with named units, run on one message at a time, with a memory carried from turn to turn. Every
parameter is a line of a plain-text edit list with its reason, as in WP-CharNet and WP-Ductus. The words Helmus can
say live in a separate hand-written table, the **phrasebook**, which the network reads like a key–value memory:
the weights decide, the table speaks.

```
message ──read──▶ tokens ──E──▶ features ──G──▶ parse ──D──▶ phrase detectors ──U──▶ intents, topics, slots
                                                                          │
                                         memory M (from earlier turns) ◀──┤
                                                                          ▼
                                    phrasebook keys K ──▶ react / answer / ask-back heads ──▶ reply ──▶ style, delay
```

1. **Read** (fixed, no weights): split the message into words, numbers, emoji and punctuation; record its shape
   (question mark, all capitals, length, stretched letters as in "sooo", laughter).
2. **E: lexicon** (weights). Each known word maps to named features:
   - `w:<word>`, its own identity;
   - `c:<class>`, the classes it belongs to: `c:you`, `c:where`, `c:food`, `c:sad`, `c:negation`, `c:ai_word` and so
     on;
   - informal spellings mapped to their word (`u` → you, `r` → are, `ngl` → not gonna lie).

   An unknown word gets shape features, and a word one typo away from a known word of four letters or more reads as
   that word (a fixed rule, stated).
3. **G: grammar** (weights; `gen/grammar/`, shared by every persona). A weighted context-free grammar of chat
   English finds the best analysis of the whole message by CKY:
   - **Tags.** Every word's possible tags come from the vocabulary: the spelling rules that make "walked" also say
     it is a past or a participle. The closed classes and the costs of rarer readings ("like" as a filler) are
     written by hand.
   - **Rules.** About 1,300 rules, with costs in thousandths, never above zero; the parser keeps the highest total.
     They cover noun phrases, the five verb forms and their complements, the verb group (auxiliaries, negation,
     tense, modals), statements and questions, the same phrases with a gap for wh-questions ("what do you like _"),
     subordinate, relative and wh-clauses, commands, polite and formal English, and chat's fragments, dropped
     subjects and fillers.
   - **Roles.** A rule marks each part's role: subj, obj, neg, past, fut, wh...
   - **What the network gets.** From the best parse:
     - for each word, its tag (`t:V`), the phrases starting there (`g:NP`) and the role of the phrase it heads
       (`r:obj`);
     - for the message, its main clauses' features: `G:S`, `G:Sq`, `G:Sw`, `G:Simp`, `G:neg`, `G:past`,
       `G:subj_2`, `G:verb_<base>`, `G:wh_<word>`;
     - for registers, phrases rather than words: "doing laundry" (main word "laundry"), said from the other side
       ("my job" → "your job").

   Scores are whole numbers, so Python and the browser find the same parse, tie for tie. Messages are short, so a
   parse takes a few milliseconds.
4. **D: phrase detectors** (weights), a convolution over word positions. A detector fires at a position when its
   words stand at the right offsets. A tap can look over a small window of offsets ("where *(are)* *(you)* from"),
   so optional words and small gaps are allowed. An inhibitory tap blocks it (no "not" before "sad"). Firing uses
   the AND of the earlier projects: `clip(Σ − (k − 1))`.
5. **U: utterance units** (weights), pooled over the message:
   - **intents:** asks where you're from, tells their name, accuses you of being a bot, a jailbreak, a greeting…;
   - **topics:** food, games, music, school, work, weather…;
   - **acts:** question, statement, laugh, insult, compliment;
   - **slot pointers:** detectors whose strongest position marks a word to copy, such as the name after "my name is".
6. **M: memory** (weights), units that carry over from turn to turn:
   - `m(t) = clip(a·m(t−1) + Σ links)`: the user's name known, where they are from, their mood, how often they have
     accused Helmus, whether Helmus already asked them something, the turn number;
   - registers that hold copied words (the user's name, a thing they said they like);
   - a record of which phrasebook entries and which persona facts Helmus has already used.
7. **K: phrasebook keys** (weights). Every phrasebook entry has a key: weights over intents, topics, acts and memory,
   and a bias. The entry's score is its key times the current units, minus a penalty if it has been used. Three
   heads each pick their best entry above a threshold:
   - **react:** "lol", "oh nice", "damn";
   - **answer:** the content;
   - **ask back:** "wbu", "u?", gated so it does not happen every time.

   The reply is their joined text. Composing a reply from parts is what gives a hand-written phrasebook its variety.
8. **Templates.** Entry texts have slots:
   - `{name}`, the user's name;
   - `{echo}`, a copied word;
   - `{reflect}`, the user's phrase with pronouns swapped, as ELIZA does;
   - `{persona:city}`, a fact from the persona table;
   - `{time}`, the local time in the persona's time zone.

   An entry has several variants, picked by a seeded hash so that a chat is reproducible.
9. **Style** (weights and a fixed pass):
   - lowercase, no final full stop;
   - occasional typos, at a rate set by a weight and placed by a seeded hash;
   - laughter mirrored when the user laughs.
10. **Delay.** The paper's typing delay formula, so a reply never arrives too fast.

## Why this design

- **A hand-written transformer generating word by word** would be the WPLM way. For open small talk it is
  fragile: every word choice would need its own circuit.
- **Composing replies from hand-written parts**, chosen by a network whose every unit has a name, keeps each reply
  natural (a person wrote it) and each decision traceable:
  - which detector fired;
  - which intent won;
  - which memory unit was set;
  - which entry scored highest, and which entries lost and by how much.
- **The pieces are classic,** each a network operation with written weights:
  - pattern matching (convolution with windowed taps);
  - pooling to the message;
  - recurrent memory;
  - a table read by dot-product keys, which is attention over a hand-written table.
- **Patterns are compiled, not trained.** Phrase detectors are written as short patterns ("where `[are]` `[you]`
  from") and turned into taps by a generator that writes each tap with its reason. That is a compiler from a
  hand-written spec, as Tracr is; nothing is fitted.

## What is fixed code and what is weights

- **Fixed code (stated on the page):**
  - the tokenizer and the one-typo lookup;
  - pooling, clipping and argmax;
  - template filling;
  - the clock: the persona's local time, US summer time by rule, and its week turned into `T:` inputs
    (`T:work_tonight`, `T:class_ahead`...) that keys read like any other unit;
  - arithmetic on numbers the user typed: a "calculator" layer. Helmus decides through weights whether a person
    would bother to answer.
  - the delay formula;
  - the claim check: a copied phrase agrees with the persona when one of its words is in the named facts.
- **Weights (the edit list):**
  - the lexicon;
  - every detector tap;
  - every link;
  - every memory rule;
  - every phrasebook key and bias;
  - the style rates.
- **Table:** the phrasebook texts and the persona facts, with the persona's week and its lines for each day.

## How Helmus is judged

1. **Unit tests.** Each intent has sentences that must fire it and sentences that must not; each memory rule has a
   scripted case.
2. **Interrogations.** Test conversations are written before freezing, covering the paper's strategy mix. Part of
   them is written by an agent that never sees Helmus's phrasebook. Each reply is checked for:
   - **sense:** does it answer what was asked?
   - **consistency:** never contradicting the persona or an earlier reply;
   - **no repeats.**
3. **Judges.** Transcripts of Helmus, of ELIZA (the 1966 DOCTOR script, run as a baseline only) and of a human
   writer are read blind by AI judges, who say which is human. This is a cheap stand-in, labelled as one.
4. **The page.** Chat with Helmus beside ELIZA, a blind "human or bot?" game, and the trace behind every reply.
5. **The real test.** If the stand-in looks good, a three-party study with people, run like the paper's.

## Honest limits, stated up front

- **Helmus is a bot.** The page says so to every visitor. In the game it plays a person, as the paper's systems did.
- **It cannot understand everything.** When it does not, it replies as a person who did not follow ("wait what"),
  and the page counts how often that happens.
- **Every line was written by a trained model** (the author). That is the experiment: what a frontier model can
  hand-write, not what a network can learn.
