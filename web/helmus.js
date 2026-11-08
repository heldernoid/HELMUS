// Helmus in the browser: the same engine as engine/helmus.py, line for line (tests/test_parity.py checks it).
// Every parameter comes from the edit list (model/helmus.edits); every line Helmus says comes from the phrasebook
// (model/phrasebook.json) and the persona table (model/persona.json). Nothing is trained.

const HEADS = ["react", "answer", "ask"];
const WORD = /[a-z0-9]+(?:'[a-z]+)?|[?!.,]+|[^\sa-z0-9]/giu;
const clip = v => (v < 0 ? 0 : v > 1 ? 1 : v);

// a stable hash in [0, 1): FNV-1a, 32 bits, over the UTF-8 bytes (as h() in engine/helmus.py)
export function h(...parts) {
  let x = 0x811c9dc5;
  for (const b of new TextEncoder().encode(parts.map(String).join("|"))) x = Math.imul(x ^ b, 0x01000193) >>> 0;
  return x / 2 ** 32;
}

function oneEdit(a, b) {
  if (a === b) return false;
  if (a.length === b.length) {
    const d = [];
    for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) d.push(i);
    return d.length === 1 || (d.length === 2 && d[1] === d[0] + 1 && a[d[0]] === b[d[1]] && a[d[1]] === b[d[0]]);
  }
  if (a.length > b.length) [a, b] = [b, a];
  let i = 0;
  while (i < a.length && a[i] === b[i]) i++;
  return a.slice(i) === b.slice(i + 1);
}

// Damerau-Levenshtein distance (optimal string alignment), stopping early once it passes `cap` (as _dl in Python)
function dl(a, b, cap) {
  if (Math.abs(a.length - b.length) > cap) return cap + 1;
  let prev2 = null, prev = Array.from({ length: b.length + 1 }, (_, j) => j);
  for (let i = 1; i <= a.length; i++) {
    const cur = [i, ...new Array(b.length).fill(0)];
    for (let j = 1; j <= b.length; j++) {
      const c = a[i - 1] === b[j - 1] ? 0 : 1;
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + c);
      if (prev2 && i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) cur[j] = Math.min(cur[j], prev2[j - 2] + 1);
    }
    if (Math.min(...cur) > cap) return cap + 1;
    prev2 = prev; prev = cur;
  }
  return prev[b.length];
}

const isAlpha = w => /^\p{L}+$/u.test(w);
const isDigit = w => /^\p{Nd}+$/u.test(w);

export class Net {
  constructor(editsText, book, persona, vocabText = "") {
    this.alias = {}; this.emb = {}; this.units = { D: {}, U: {}, M: {} };
    this.regs = {}; this.keys = {}; this.rates = {}; this.vocab = new Set(); this.why = {};
    for (const raw of editsText.split("\n")) {
      const cut = raw.indexOf("#"), line = cut >= 0 ? raw.slice(0, cut) : raw, reason = cut >= 0 ? raw.slice(cut + 1).trim() : "";
      const p = line.split(/\s+/).filter(Boolean);
      if (!p.length) continue;
      const op = p[0];
      let key = null;
      const U = (layer, name) => (this.units[layer][name] ??= { bias: 0, taps: [], links: [], decay: 0 });
      const K = name => (this.keys[name] ??= { bias: 0, links: [] });
      if (op === "ALIAS") { this.alias[p[1]] = p[2].split("+"); key = "ALIAS " + p[1]; }
      else if (op === "EMB") { (this.emb[p[1]] ??= {})[p[2]] = +p[3]; key = `EMB ${p[1]} ${p[2]}`; }
      else if (op === "UNIT") { U(p[1], p[2]); key = `UNIT ${p[1]} ${p[2]}`; }
      else if (op === "TAP") { this.units.D[p[1]].taps.push([+p[2], +p[3], p[4].split("|"), +p[5]]); key = `TAP ${p[1]}`; }
      else if (op === "BIAS") { if (p[1] === "K") K(p[2]).bias = +p[3]; else this.units[p[1]][p[2]].bias = +p[3]; key = `BIAS ${p[1]} ${p[2]}`; }
      else if (op === "LINK") { if (p[1] === "K") K(p[2]).links.push([p[3], +p[4]]); else this.units[p[1]][p[2]].links.push([p[3], +p[4]]); key = `LINK ${p[1]} ${p[2]} ${p[3]}`; }
      else if (op === "DECAY") { this.units.M[p[1]].decay = +p[2]; key = `DECAY ${p[1]}`; }
      else if (op === "REG") { (this.regs[p[1]] ??= []).push([p[2], p[3]]); key = `REG ${p[1]} ${p[2]}`; }
      else if (op === "VOCAB") { this.vocab.add(p[1]); key = "VOCAB " + p[1]; }
      else if (op === "RATE") { this.rates[p[1]] = +p[2]; key = `RATE ${p[1]}`; }
      else throw new Error("unknown op " + op);
      if (!(key in this.why)) this.why[key] = reason;
    }
    this.book = Object.fromEntries(book.map(e => [e.id, e]));
    const generic = ["U:topic_", "U:theme_", "U:question", "U:q_form", "U:understood", "U:strange"];
    this.gates = {};
    for (const [eid, k] of Object.entries(this.keys))
      this.gates[eid] = k.links.filter(([src, w]) => w > 0 && src.startsWith("U:") && !generic.some(g => src.startsWith(g))).map(([src]) => src);
    this.persona = persona;
    for (const ws of Object.values(this.alias)) for (const w of ws) this.vocab.add(w);
    this.known = new Set([...this.vocab, ...Object.keys(this.emb)]);
    this.real = new Set(vocabText.split("\n").filter(w => w && !w.startsWith("#")));
    this.lexiconAll = [...new Set([...this.known, ...this.real])].filter(w => w.length >= 3 && isAlpha(w)).sort();
  }

  // ---- read (fixed) ----
  read(text) {
    const raw = text.match(WORD) || [];
    const S = { "S:any": 1 };
    if (text.includes("?")) S["S:question"] = 1;
    const letters = [...text].filter(c => /\p{L}/u.test(c));
    if (letters.length >= 4 && letters.every(c => c === c.toUpperCase() && c !== c.toLowerCase())) S["S:shout"] = 1;
    if (/(.)\1\1/u.test(text.toLowerCase())) S["S:stretched"] = 1;
    if (!raw.length) S["S:empty"] = 1;
    let words = [];
    for (const tok of raw) {
      let t = tok.toLowerCase();
      if (/^[?!.,]+$/.test(t)) continue;
      t = t.replace(/([a-z])\1{2,}/g, "$1$1");
      if (/^(?:(?:ha|ah){2,}h?|(?:he){2,}h?|l(?:ol)+|(?:lo)+l)$/.test(t))
        t = "ah".includes(t[0]) ? "haha" : (t[0] === "h" || t[0] === "e") ? "hehe" : "lol";
      if (!this.known.has(t) && !(t in this.alias) && !(t in this.emb)) {
        const single = t.replace(/([a-z])\1+/g, "$1");
        if (this.known.has(single) || single in this.alias) t = single;
      }
      words.push(...(this.alias[t] || [t]));
    }
    words = words.map(w => this.near(w));
    S["S:words"] = Math.min(1, words.length / 20);
    if (words.length) S["S:unknown_share"] = words.filter(w => !this.known.has(w) && !isDigit(w)).length / words.length;
    if (words.length <= 2) S["S:short"] = 1;
    const m = Net.math(text);
    if (m) Object.assign(S, m);
    return [words, S];
  }

  near(w) {
    if (this.known.has(w) || w in this.alias || this.real.has(w) || w.length < 3 || !isAlpha(w)) return w;
    const n = w.length, budget = n >= 8 ? 2 : 1, sorted = x => [...x].sort().join("");
    let best = w, bk = [budget + 1, 1, 1];
    const less = (a, b) => a[0] !== b[0] ? a[0] < b[0] : a[1] !== b[1] ? a[1] < b[1] : a[2] < b[2];
    for (const cand of this.lexiconAll) {
      if (cand[0] !== w[0] || Math.abs(cand.length - n) > budget) continue;
      if (n <= 4 && (cand.length !== n || sorted(cand) !== sorted(w))) continue;
      const d = dl(w, cand, budget), k = [d, cand.length === n ? 0 : 1, this.known.has(cand) ? 0 : 1];
      if (d <= budget && less(k, bk)) {
        best = cand; bk = k;
        if (k[0] === 1 && k[1] === 0 && k[2] === 0) break;
      }
    }
    return best;
  }

  static math(text) {
    const m = text.toLowerCase().match(/(-?\d+(?:\.\d+)?)\s*([+\-x*/]|times|plus|minus|divided by)\s*(-?\d+(?:\.\d+)?)/);
    if (!m) return null;
    const a = +m[1], b = +m[3];
    const op = { times: "*", x: "*", plus: "+", minus: "-", "divided by": "/" }[m[2]] || m[2];
    if (op === "/" && b === 0) return { "S:math": 1, "S:math_hard": 1 };
    const v = { "+": a + b, "-": a - b, "*": a * b, "/": b ? a / b : 0 }[op];
    const easy = Math.abs(a) <= 12 && Math.abs(b) <= 12 && "+-*".includes(op) && v === Math.trunc(v);
    return { "S:math": 1, [easy ? "S:math_easy" : "S:math_hard"]: 1, _calc: v === Math.trunc(v) ? String(v) : v.toFixed(2) };
  }

  // ---- the network ----
  features(words) {
    const n = words.length;
    return words.map((w, i) => {
      const f = { ...(this.emb[w] || {}) };
      if (!("w:" + w in f)) f["w:" + w] = 1;
      if (!this.known.has(w) && !isDigit(w)) f["shape:unknown"] = 1;
      if (isDigit(w)) f["shape:number"] = 1;
      if (!("c:func" in f)) f["shape:content"] = 1;
      if (i === 0) f["pos:start"] = 1;
      if (i === n - 1) f["pos:end"] = 1;
      f["shape:any"] = 1;
      return f;
    });
  }

  detect(X) {
    const out = {}, where = {}, n = X.length;
    for (const [name, u] of Object.entries(this.units.D)) {
      let best = 0, at = -1;
      for (let t = 0; t < n; t++) {
        let s = u.bias;
        for (const [lo, hi, feats, w] of u.taps) {
          let m = 0;
          for (let o = lo; o <= hi; o++) {
            if (t + o >= 0 && t + o < n) {
              const x = X[t + o];
              for (const f of feats) { const v = x[f] || 0; if (v > m) m = v; }
            }
          }
          s += w * m;
        }
        const v = clip(s);
        if (v > best + 1e-9) { best = v; at = t; }
      }
      out["D:" + name] = best; where[name] = at;
    }
    return [out, where];
  }

  turn(state, text, now = new Date()) {
    const [words, S] = this.read(text);
    const calc = S._calc ?? null; delete S._calc;
    const norm = words.join(" ");
    if (norm && (state.history || []).some(m => this.read(m)[0].join(" ") === norm)) S["S:repeat"] = 1;
    const X = this.features(words);
    const A = { ...S };
    const feats = new Set(X.flatMap(x => Object.keys(x)));
    for (const f of feats) A["F:" + f] = Math.max(...X.map(x => x[f] || 0));
    const [D, where] = this.detect(X);
    Object.assign(A, D);
    for (const [name, u] of Object.entries(this.units.U)) {
      let s = u.bias;
      for (const [src, w] of u.links) s += w * (A[src] || 0);
      A["U:" + name] = clip(s);
    }
    const prevM = state.M || {}, prevE = state.E || {}, M = {};
    for (const [name, u] of Object.entries(this.units.M)) {
      let s = u.bias + u.decay * (prevM[name] || 0);
      for (const [src, w] of u.links) {
        if (src.startsWith("M:")) s += w * (prevM[src.slice(2)] || 0);
        else if (src.startsWith("E:")) s += w * (prevE[src.slice(2)] || 0);
        else s += w * (A[src] || 0);
      }
      M[name] = clip(s);
    }
    for (const [k, v] of Object.entries(M)) A["M:" + k] = v;
    for (const [k, v] of Object.entries(prevE)) A["E:" + k] = v;
    const regs = { ...(state.R || {}) };
    for (const [reg, slots] of Object.entries(this.regs)) {
      let best = slots[0];
      for (const sg of slots) if ((A["D:" + sg[0]] || 0) > (A["D:" + best[0]] || 0)) best = sg;
      const [slot, gate] = best;
      if ((A[gate] || 0) > 0.5 && (A["D:" + slot] || 0) > 0.5 && (where[slot] ?? -1) >= 0) regs[reg] = words[where[slot]];
    }
    const used = state.used || {}, seed = state.seed || 0, pen = this.rates.repeat_penalty ?? 0.6;
    const raw = {}, scores = {};
    for (const [eid, k] of Object.entries(this.keys)) {
      let s = k.bias;
      for (const [src, w] of k.links) s += w * (A[src] || 0);
      raw[eid] = s;
      scores[eid] = s - pen * (used[eid] || 0);
    }
    const turnNo = (state.turn || 0) + 1;
    const ctx = { calc, regs, now, words, history: state.history || [] };
    const said = new Set(state.said || []);
    // the best candidate whose lines are not all said already; if every one is spent, the best (as pick() in Python)
    const pick = (cands, key) => {
      const ranked = cands.map(e => [key(e), e]).sort((x, y) => y[0][0] - x[0][0] || y[0][1] - x[0][1]).map(x => x[1]);
      for (const e of ranked) if (this.book[e].texts.some(t => !said.has(this.fill(t, ctx)))) return e;
      return ranked[0];
    };
    const chosen = {};
    for (const head of HEADS) {
      const fit = Object.keys(scores).filter(e => {
        if (this.book[e].head !== head || !(raw[e] > 0)) return false;
        const g = this.gates[e];
        return !g.length || g.some(src => (A[src] || 0) > 0.5);
      });
      if (fit.length) chosen[head] = pick(fit, e => [scores[e], -h(seed, e)]);
    }
    if (!("answer" in chosen) && !("react" in chosen))
      chosen.answer = pick(Object.keys(scores).filter(e => this.book[e].head === "fallback"), e => [scores[e], -h(seed, e, used[e] || 0)]);

    const parts = ["react", "answer", "ask"].filter(hd => hd in chosen).map(hd => this.render(chosen[hd], state, turnNo, ctx));
    const reply = this.style(parts.filter(Boolean).join(" "), seed, turnNo);
    const newUsed = { ...used };
    for (const e of Object.values(chosen)) newUsed[e] = (newUsed[e] || 0) + 1;
    const E = {};
    for (const e of Object.values(chosen)) E[e] = 1;
    for (const [hd, e] of Object.entries(chosen)) { E["@h:" + hd] = 1; if (this.book[e].group) E["@" + this.book[e].group] = 1; }
    const newState = { seed, turn: turnNo, M, E, R: regs, used: newUsed, history: [...(state.history || []), text],
      said: [...(state.said || []), ...parts.filter(Boolean)] };
    const units = {};
    for (const [k, v] of Object.entries(A)) if (v > 0.001 && !k.startsWith("F:")) units[k] = Math.round(v * 1000) / 1000;
    const top = Object.entries(scores).map(([e, v]) => [Math.round(v * 1000) / 1000, e])
      .sort((a, b) => b[0] - a[0] || (b[1] > a[1] ? 1 : b[1] < a[1] ? -1 : 0)).slice(0, 8);
    return [reply, newState, { words, units, chosen, top }];
  }

  // ---- the table: templates and style ----
  local(now) { return new Date(now.getTime() + this.persona.utc_offset * 3600 * 1000); }

  render(eid, state, turnNo, ctx) {
    const texts = this.book[eid].texts, n = (state.used || {})[eid] || 0;
    const start = Math.floor(h(state.seed || 0, eid, n) * texts.length), said = new Set(state.said || []);
    for (let k = 0; k < texts.length; k++) {
      const out = this.fill(texts[(start + k) % texts.length], ctx);
      if (!said.has(out)) return out;
    }
    return this.fill(texts[start], ctx);
  }

  fill(text, ctx) {
    const P = this.persona;
    return text.replace(/\{([a-z0-9_:]+)\}/g, (_, key) => {
      if (key.startsWith("p:")) return String(P.facts[key.slice(2)] ?? "");
      if (key === "calc") return ctx.calc || "";
      if (key in ctx.regs) return ctx.regs[key];
      const L = this.local(ctx.now);
      if (key === "time") return `${L.getUTCHours() % 12 || 12}:${String(L.getUTCMinutes()).padStart(2, "0")}`;
      if (key === "first_msg" || key === "last_msg") {
        const hist = ctx.history;
        if (!hist.length) return "";
        const m = (key === "first_msg" ? hist[0] : hist[hist.length - 1]).trim().toLowerCase().replace(/[?!.]+$/, "");
        return m.length <= 40 ? m : m.slice(0, 37).replace(/ [^ ]*$/, "") + "...";
      }
      if (key === "weekday") return ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"][L.getUTCDay()];
      if (key === "daypart") { const hr = L.getUTCHours(); return hr >= 5 && hr < 12 ? "morning" : hr >= 12 && hr < 17 ? "afternoon" : hr >= 17 && hr < 22 ? "evening" : "night"; }
      return "";
    }).trim();
  }

  style(text, seed, turnNo) {
    if (this.persona.lowercase ?? true) text = text.toLowerCase();
    text = text.replace(/\.\s*$/, "").trim();
    const rate = this.rates.typo || 0, words = text.split(" ");
    if (rate && words.length >= 2 && h(seed, turnNo, "typo") < rate) {
      const i = Math.floor(h(seed, turnNo, "typo-at") * words.length), w = words[i];
      if (w.length >= 4 && isAlpha(w)) {
        const j = 1 + Math.floor(h(seed, turnNo, "typo-j") * (w.length - 2));
        words[i] = w.slice(0, j) + w[j + 1] + w[j] + w.slice(j + 2);
      }
    }
    return words.join(" ");
  }
}

// seconds before the reply is shown: the 2025 study's typing delay (a minimum, typing, reading, a skewed pause)
export function delay(reply, prev, seed, turnNo) {
  const g = -Math.log(Math.max(1e-9, 1 - h(seed, turnNo, "think"))) * 0.6;
  return 1 + 0.3 * reply.length + 0.03 * prev.length + g;
}
