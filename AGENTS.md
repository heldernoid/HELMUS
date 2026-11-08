# AGENTS.md

Guidance for AI agents (and people) working on Helmus. Read `docs/design.md` for what it is, `docs/personas.md` for
who it plays, and `LOG.md` for what was decided and why.

## What this project is

Helmus is a chatbot meant to be judged human in 5-minute text chats more often than ELIZA, and to hold its own against
Cleverbot. Its network is **written by hand**: a lexicon, phrase detectors, utterance units, memory and phrasebook
keys, all as lines of a plain-text edit list (`weights/helmus.edits`) with a reason on every line. What it says comes
from a hand-written phrasebook (`weights/phrasebook.json`) and persona table (`weights/persona.json`). The engine
(`engine/helmus.py`, mirrored in `web/helmus.js`) starts from nothing and applies them. Sister project of WP-CharNet
and WP-Ductus, same method.

## House rules

1. **No training, ever.** No gradient descent, no fitting, no automatic search over weights or thresholds. Values are
   typed by hand, each with a reason.
2. **Everything is written by the author model.** No outside corpus, chat log, dataset, word list or model at chat
   time. ELIZA (the CC0 1966 DOCTOR script) appears only as a baseline to compare against, in `baselines/`.
3. **Every weight has a reason.** The DSL refuses a weight without one.
4. **Every intent has test sentences.** `yes=` sentences must fire it, `no=` sentences must not. Add both kinds,
   including near misses ("how are you a bot" is not a "how are you").
5. **The persona is one table.** Facts about the person Helmus plays live only in `gen/persona/<name>.py`; the
   phrasebook refers to them as `{p:key}`. Never write a persona fact into a phrasebook line.
6. **The voice of the persona:** follow `docs/personas.md`. For Josh: mostly 1–5 words, lowercase, no final full
   stop, no apostrophes, slang now and then, never an assistant's tone.
7. **Never an assistant.** No lists, no "great question", no help at length, no knowledge a person of the persona
   would not have. A person refuses tasks, pretends ignorance and changes the subject.
8. **Log everything** in `LOG.md`: what changed, the numbers before and after, and what did not work.
9. **One set of weights.** No version names in files or docs.
10. **Privacy.** No personal names, emails or local paths in files or commits.
11. **No assistant-specific files.** This file is the shared guide; no `CLAUDE.md` or similar.

## The authoring language (gen/dsl.py)

- **`cls(name, words, why)`:** a word class; words get the feature `c:<name>`.
- **`alias(raw, words, why)`:** an informal spelling read as words (`u` → `you`).
- **`intent(name, patterns, why, yes=[...], no=[...], unless=[...])`:** an utterance unit that fires when any
  pattern does.
  - Pattern syntax: words; `a|b`; `@class`; `[optional]`; `*` (up to 3 words); `!x` (not after x); `^` and `$`;
    `{slot}` or `{slot:unknown}`.
  - `unless` blocks the intent when another intent (or an `F:` feature) fires.
- **`register(name, intent, slot, why)`:** copies a slot's word into a register for `{name}` in templates.
- **`topic(name, classes, why)`, `unit(name, links, why)`:** units from features or other units.
- **`mem(name, links, why, decay, bias)`:** a memory unit carried between turns.
  - Sources: `U:`, `S:` (this message); `M:` (last turn's memory); `E:<entry>`, `E:@<group>`, `E:@h:<head>`
    (what Helmus said last turn).
- **`say(id, head, when, texts, why, bias=None, group=None)`:** a phrasebook entry.
  - Heads: `react`, `answer`, `ask`, `fallback`.
  - The key is `when` ({source: weight}). The default bias makes it score 0.5 when all its positive sources are on.
  - Texts are its variants, with slots: `{p:key}`, `{user_name}`, `{user_like}`, `{user_place}`, `{calc}`,
    `{time}`, `{weekday}`, `{daypart}`, `{first_msg}`, `{last_msg}`.
- **`rate(name, value, why)`:** a style rate (typos, the repeat penalty).

## How a reply is made

Each head takes its best entry whose key scores above zero; a used entry ranks lower (repeat penalty) but is not
ruled out. If neither react nor answer fits, a fallback answers. The reply is react + answer + ask, joined, then
lowercased with no final full stop, with a typo now and then.

## Commands

```bash
python3 gen/generate.py [persona]             # weights/ and web/model/ (persona default: josh)
python3 -m pytest -q tests                     # intent tests and conversation checks
python3 engine/helmus.py [seed]                # chat in the terminal (TRACE=1 shows the chosen entries)
```

## Definition of done for a change

`gen/generate.py` runs without unknown sources, every test passes, the scripted conversations read as the persona,
`LOG.md` is updated, no version names.
