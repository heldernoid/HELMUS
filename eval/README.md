# Helmus held-out interrogation set

`interrogations.json` holds 160 interrogator scripts (704 messages) for testing Helmus in
5-minute, three-party text Turing tests (Jones & Bergen 2025, arXiv 2503.23674).

## How it was written

- A separate agent wrote it, playing the interrogators, before the bot's phrasebook existed.
- The writer was blind to the bot: it did not read `gen/`, `weights/` or `web/`. Its only
  source was `docs/research.md`, which describes what real interrogators do.
- Each script is the messages one interrogator sends to one witness, in order: 3 to 7
  messages, mostly 4 to 5, none longer than 300 characters. The follow-ups make sense
  whatever the bot replies. Some react to a generic reply ("lol ok", "that's what a bot
  would say").
- The style mix follows roughly the study's proportions: small talk is the most common,
  many games are mixed, and strange inputs and jailbreaks are included. The 25 "sharp"
  games are written by a skilled, adversarial interrogator. They use memory checks,
  repeated or reworded questions, commonsense riddles, questions about local detail,
  questions about the other witness, and speed or counting traps.
- The writing is casual on purpose: lowercase, typos, slang, emoji, some Spanish, some
  rudeness. No wording is reused across scripts.

## Format

A list of objects: `{"id", "style", "persona_of_interrogator", "messages": [...]}`.
Each id is the style plus a number, e.g. `sharp-07`.

## Style counts

| style       | count |
|-------------|------:|
| mixed       | 34 |
| sharp       | 25 |
| smalltalk   | 22 |
| emotional   | 14 |
| accusation  | 12 |
| situational | 10 |
| strange     | 10 |
| knowledge   |  9 |
| jailbreak   |  9 |
| memory      |  8 |
| rude        |  7 |
| **total**   | **160** |

## Rule: this is a held-out test

Do not use this set to write, tune or extend the bot's patterns, phrasebook or weights.
Do not copy its wording into `gen/`, `weights/` or `web/`, and do not use it as a list of
cases to cover. Use it only to evaluate the bot. Once the bot has been fitted to it, the set
no longer measures anything. If that happens, write a new blind set.

## Dev and test splits

`eval/run.py` splits the set once, by a hash of each game's id: 60 games are the **dev** split, which may be read to
find where Helmus fails, and 100 are the **test** split, whose transcripts are never read while writing Helmus. Only
the test split's numbers are reported as results.
