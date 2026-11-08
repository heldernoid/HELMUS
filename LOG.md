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

## What did not work

- A repeat penalty that ruled entries out (decision 5).
- The typo rule at four letters, with only the lexicon as known words: "name" became "game", "ignored" became "ignore"
  (decision 6).
- Counting a word as unknown when it had no class: "the" counted as unknown, so "i am from the future" captured
  "future" as a place.

## Numbers

First working version, persona Josh:
- 379 units (305 detectors, 57 utterance units, 17 memory units);
- 3,179 edit lines;
- 77 phrasebook entries (236 lines);
- 200 intent tests, all passing.
