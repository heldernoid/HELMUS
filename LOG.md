# How Helmus was written

## Decisions

**1. The target.** The 2025 three-party Turing test (Jones & Bergen, arXiv 2503.23674; PNAS 2026):
- ELIZA was judged human 23% of the time;
- GPT-4.5 with a persona prompt 73%;
- GPT-4o without one 21%.

Games had a median of 8 messages over 4.2 minutes, so Helmus answers about 4 times a game.

What interrogators do:
- small talk 61%;
- social and emotional probing 50%;
- asking if the witness is human 19%;
- situational awareness 13%;
- knowledge 12%.

Strange inputs and jailbreaks were the most accurate tests, though rare. The winning persona was a 19-year-old
introverted gamer:
- mostly under 5 words;
- no full stops, no apostrophes;
- slang sparingly;
- asks back sometimes;
- feigns ignorance.

**2. Everything hand-written.** The user's rule: all data, dialogue and persona facts come from the author model.
There is no corpus, no infini-gram and no model at chat time. ELIZA's CC0 DOCTOR script is only a baseline.

**3. The architecture** (docs/design.md):
- a lexicon;
- phrase detectors (a convolution over word positions with windowed taps, the AND idiom of the sister projects);
- pooled utterance units;
- recurrent memory;
- a phrasebook read through hand-written keys by three heads (react, answer, ask).

A hand-written transformer generating word by word (the WPLM way) was set aside: for open small talk every word choice
would need its own circuit, and a reply composed from hand-written parts is both natural and traceable.

**4. Patterns are compiled, not trained.**
- A detector is written as a short pattern ("where [are] you from").
- `gen/dsl.py` turns it into taps: each required word +1 at its window of offsets, an AND bias of −(k−1), and −1
  for a `!x` block.
- Every tap carries the pattern as its reason.

**5. Repeat penalty: rank lower, don't rule out.** At first a used entry's score dropped below zero, and a repeated
question ("wyd" after "sup") fell through to a fallback ("good question lol"). Now an entry fits by its key alone, and
the penalty only orders the entries that fit.

**6. Typos.**
- A word of five letters or more, one edit from a known word, reads as that word.
- Words a detector reads (VOCAB) count as known, so "name" is no longer read as "game".
- An inflection is not a typo: "ignored" is not read as "ignore".

**7. Blocking (`unless`).** Near misses are blocked by competing intents:
- "how are you a bot" is an accusation;
- "what do you do for fun" is not a job question;
- "i like you" is a compliment, not a taste.

**8. Understanding, by domain.** Four writers added about 470 intents, each with test sentences that must and must not
fire it:
- small talk;
- feelings and opinions;
- bot tests and strange inputs;
- knowledge and the situation.

They exposed DSL flaws, now fixed:
- an optional word `[x]` used to match any word (it now expands into the variants with and without it);
- multi-word alternatives (`a|b_c`);
- slots limited to a kind (`{x:content}`, `{x:#num}`, `{x:@class}`);
- an `unless` block that an intent with many patterns could outvote (blocks now scale with the intent's size).

**9. Josh's phrasebook, by domain.** Four writers gave every intent replies in Josh's voice:
- about 2,500 entries at first, about 3,000 (10,800 lines) by the end;
- each with 3–8 variants;
- facts only through the persona table, plus `facts()` declared beside the lines that use them;
- memory for "asked twice" and for follow-ups on the last topic.

A coverage check (`tests/coverage.py`) asks whether every recognised test sentence gets a real reply, not a fallback.
Every domain is at 100%.

**10. No word-for-word repeats.** The research's "single biggest giveaway". Four rules:
- a used line is skipped while its entry has another;
- an entry whose lines are all spent gives way to the next fitting entry;
- a message the user repeats word for word is noticed (`S:repeat`), lightly the first time ("u just asked that lol")
  and more firmly after;
- repeats on the held-out games went from 20% to 0%.

**11. An entry fits only when its question was asked.** Phrasebook keys are sums. Two incidental words could add up and
fire an entry whose intent never fired (175 entries could). The engine now gates each entry on its intent sources
(its positive `U:` links other than topics and message shapes). Keys still rank the entries that fit.

**12. Reading misspellings against a hand-written vocabulary.**
- The user chose a hand-written English vocabulary over a public word list: about 10,000 base words, 30,000 forms by
  fixed spelling rules (`gen/vocab.py`, `gen/vocabulary/`).
- A word in it is real and stays as it is, so "worry" is no longer read as "sorry".
- Any other word is read as the nearest real word by Damerau distance:
  - a swap for 3–4 letters;
  - one edit for 5–7;
  - two edits for 8 or more.
- The first letter must match. On a tie, the same length wins ("wehre" is "where", not "were").
- Stretched words are squeezed ("whaaaats"), and long laughs read as laughter.

**13. Dev and test.**
- The 160 held-out interrogations were written blind and split by hash: 60 dev games, read to find failures, and 100
  test games, never read.
- Round 2 fixed the dev failures by kind. Dev fallbacks fell from 37% to 1%, but test fallbacks only from 41% to 40%.
  Adding patterns family by family overfits.
- The split made this visible.

**14. Themes and question types: understanding that generalises.**
- The vocabulary's themed blocks are mapped by hand to 22 themes (`gen/topics.py`), so any word of a theme marks the
  message (`U:theme_food` on "soup"). Words that usually mean something else in chat are excluded ("can", "watch",
  "plans").
- Question-type units (`gen/intents/qtypes.py`): do you like, do you have, have you ever, what's your, do/can/would you.
- Last-resort replies are keyed on theme × question type, scoring 0.2–0.35, under every specific entry
  (`josh_themes_a.py`, `josh_themes_b.py`). Below them sit hedged answers by question type alone.
- Test fallbacks went from 40% to 31% with the themes, and to 26% with the question types.

**15. One life for Josh.** A consistency pass resolved contradictions between domains:
- Thanksgiving at Grandma's;
- one Florida trip, at 14;
- the second round of the study;
- a chill boss;
- job pay against study pay;
- one nightmare;
- one crying story;
- lying on his bed now;
- a single day timeline.

The canonical life is in `docs/personas.md`, "Josh's life, as written".

## What did not work

- A repeat penalty that ruled entries out (decision 5).
- The typo rule at four letters, with only the lexicon as known words: "name" became "game", "ignored" became "ignore"
  (decision 6).
- Counting a word as unknown when it had no class: "the" counted as unknown, so "i am from the future" captured
  "future" as a place.

## Numbers

Held-out test games (100, never read), against ELIZA (`eval/results.json`):

| | First version | After phrasebook | After round 2 | After themes and question types |
|---|---|---|---|---|
| not understood (fallback) | 58% | 41% | 40% | 26% |
| word-for-word repeats | 20% | 0% | 0% | 0% |
| sounds like an assistant | 0% | 0% | 0% | 0% |

ELIZA: 2.3% repeats, 6.5 words a reply. HELMUS: 3.6 words a reply, 80% of replies 5 words or fewer.

Size:
- 87,756 edit lines;
- 8,053 units (7,161 detectors, 692 utterance units, 200 memory units);
- 3,037 phrasebook entries (10,847 lines);
- 6,619 intent tests;
- a hand-written vocabulary of 29,990 forms.
