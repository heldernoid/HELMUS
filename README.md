<p align="center">
  <img src="web/apple-touch-icon.png" width="96" height="96" alt="HELMUS logo">
</p>
<h1 align="center">HELMUS</h1>
<p align="center"><em>Hand-Engineered Language Machine, Untrained &amp; Self-explaining</em><br><a href="https://heldernoid.github.io/HELMUS/">heldernoid.github.io/HELMUS</a></p>

HELMUS is a chatbot built to pass as a person in a five-minute text Turing test. Here it plays **Josh**, 19, from
Columbus, Ohio. Every weight, every rule, every line it can say and every fact about Josh was **written by hand**, by a
frontier model (Claude). There is no training, no dataset, no corpus, and no other model at chat time. It runs in the
browser and shows, for every reply, what it read, which units fired, what it remembered and which lines competed.

The name comes from its maker's name, given a classical ending; read as letters, it is what the subtitle says.

## Try it

**[heldernoid.github.io/HELMUS](https://heldernoid.github.io/HELMUS/)**: chat with Josh for five minutes, click any reply
to see why he said it, and tick *Show what ELIZA would say* to see the 1966 baseline answer the same message.

## How it works

HELMUS is not a language model: it predicts no words. It is a network of named units, and every number in it is a
line of a plain-text edit list (`weights/helmus.edits`) with the reason for it.

1. **Read** (fixed code).
   - Words, numbers and punctuation; informal spellings expanded (u → you, ngl → not going to lie).
   - Stretched words squeezed (whaaaats → whats).
   - Misspellings fixed to the nearest real word of a hand-written vocabulary of about 30,000 word forms; real words
     are never "corrected".
2. **Lexicon.** Words get named features: their identity and their classes.
3. **Phrase detectors.** About 7,000 of them, a convolution over word positions. They are written as short patterns
   ("where [are] you from") and compiled into weights.
4. **Intents and topics.** About 600 units that pool the detectors into what the message means.
5. **Memory.** About 200 units carried from turn to turn: your name, what you said, how often you have called Josh a
   bot, what he already said.
6. **Phrasebook.**
   - About 2,800 hand-written entries (about 9,500 lines), each with a key of weights saying when it fits.
   - Three heads pick a reaction, an answer and, now and then, a question back. An entry fits only when the question
     it answers was asked.
7. **Reply.**
   - Slots are filled from Josh's life table and from memory.
   - Then his voice is applied: lowercase, no full stop, the odd typo.
   - The reply never repeats a line already said, and it arrives after a human typing delay.

`docs/design.md` has the details; `docs/research.md` the studies the design follows (the 2025 three-party Turing test
of Jones & Bergen, Human or Not, the Loebner Prize, Mitsuku, Cleverbot, ELIZA).

## Results

Measured on 100 interrogations written in advance by a separate writer, before Josh's phrasebook existed, and never
read while writing HELMUS. The same messages were sent to ELIZA, the baseline of the 2025 study, where it was judged
human 23% of the time. The numbers are in `eval/results.json` and on the page's *Results* view. Judging by people is
the next step.

## Run it

```bash
python3 gen/generate.py                          # weights/ and web/model/ from the hand-written spec in gen/
python3 -m pytest -q tests                       # intent tests, coverage, browser/Python parity (needs node)
python3 tests/coverage.py                        # does every recognised message get a real reply?
python3 eval/run.py                              # the held-out interrogations, HELMUS against ELIZA
python3 engine/helmus.py                         # chat in the terminal
cd web && python3 -m http.server                 # the page
```

## Files

| Path | What |
|---|---|
| `gen/` | the hand-written spec: lexicon, intents (`gen/intents/`), memory, Josh's life (`gen/persona/`), his phrasebook (`gen/phrasebook/`), the vocabulary (`gen/vocabulary/`), and the authoring language (`gen/dsl.py`) |
| `weights/` | the generated network (`helmus.edits`), the phrasebook, the persona table and the vocabulary |
| `engine/helmus.py`, `web/helmus.js` | the engine in Python and the same engine in the browser |
| `web/` | the page |
| `eval/` | the held-out interrogations, the runner and the blind judging tools |
| `baselines/eliza/` | ELIZA with the DOCTOR script (Wade Brainerd's MIT-licensed Python version), used only as a baseline |
| `docs/` | design, personas, research |
| `LOG.md`, `AGENTS.md` | how it was written, and how to work on it |

## Limits

- **Coverage.** It understands what it was written to understand. On held-out interrogations it still misses a large
  share of messages and answers them with a plain "idk"-style line.
- **English only, one persona.** The network is shared, so another persona is another table and phrasebook.
- **No proof it passes as human yet.** The machine-checkable measures above are not a Turing test; that needs judges.
- **Written by a trained model.** Nothing in HELMUS was trained, but the author of every line is a frontier model.
  That is the experiment: what a model can write by hand.

Sister projects, built the same way: [WP-CharNet](https://github.com/heldernoid/WP-CharNet) (reads handwriting) and
[WP-Ductus](https://github.com/heldernoid/WP-Ductus) (teaches calligraphy). MIT licence.
