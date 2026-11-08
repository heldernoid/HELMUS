// ELIZA (Weizenbaum, 1966) with the DOCTOR script: a line-for-line JavaScript port of Wade Brainerd's Python ELIZA
// (github.com/wadetb/eliza, MIT licence, copyright (c) 2019 Wade Brainerd; see baselines/eliza/LICENSE), the version
// the 2025 three-party Turing test used as its baseline. It is here only to compare against: Helmus uses none of it.

export class Eliza {
  constructor(script) {
    this.initials = []; this.finals = []; this.quits = []; this.pres = {}; this.posts = {}; this.synons = {};
    this.keys = {}; this.memory = [];
    let key = null, decomp = null;
    for (const line of script.split("\n")) {
      if (!line.trim()) continue;
      const i = line.indexOf(":");
      const tag = line.slice(0, i).trim(), content = line.slice(i + 1).trim();
      const parts = content.split(" ");
      if (tag === "initial") this.initials.push(content);
      else if (tag === "final") this.finals.push(content);
      else if (tag === "quit") this.quits.push(content);
      else if (tag === "pre") this.pres[parts[0]] = parts.slice(1);
      else if (tag === "post") this.posts[parts[0]] = parts.slice(1);
      else if (tag === "synon") this.synons[parts[0]] = parts;
      else if (tag === "key") { key = { word: parts[0], weight: parts.length > 1 ? +parts[1] : 1, decomps: [] }; this.keys[parts[0]] = key; }
      else if (tag === "decomp") {
        let p = parts, save = false;
        if (p[0] === "$") { save = true; p = p.slice(1); }
        decomp = { parts: p, save, reasmbs: [], next: 0 };
        key.decomps.push(decomp);
      } else if (tag === "reasmb") decomp.reasmbs.push(parts);
    }
  }

  matchR(parts, words, results) {
    if (!parts.length && !words.length) return true;
    if (!parts.length || (!words.length && !(parts.length === 1 && parts[0] === "*"))) return false;
    if (parts[0] === "*") {
      for (let i = words.length; i >= 0; i--) {
        results.push(words.slice(0, i));
        if (this.matchR(parts.slice(1), words.slice(i), results)) return true;
        results.pop();
      }
      return false;
    }
    if (parts[0].startsWith("@")) {
      const root = parts[0].slice(1);
      if (!this.synons[root] || !this.synons[root].includes(words[0].toLowerCase())) return false;
      results.push([words[0]]);
      return this.matchR(parts.slice(1), words.slice(1), results);
    }
    if (parts[0].toLowerCase() !== words[0].toLowerCase()) return false;
    return this.matchR(parts.slice(1), words.slice(1), results);
  }

  next(decomp) { const r = decomp.reasmbs[decomp.next % decomp.reasmbs.length]; decomp.next++; return r; }

  reassemble(reasmb, results) {
    const out = [];
    for (const w of reasmb) {
      if (!w) continue;
      if (w[0] === "(" && w[w.length - 1] === ")") {
        let insert = results[+w.slice(1, -1) - 1] || [];
        for (const p of [",", ".", ";"]) { const k = insert.indexOf(p); if (k >= 0) insert = insert.slice(0, k); }
        out.push(...insert);
      } else out.push(w);
    }
    return out;
  }

  sub(words, table) { return words.flatMap(w => table[w.toLowerCase()] || [w]); }

  matchKey(words, key) {
    for (const decomp of key.decomps) {
      const results = [];
      if (!this.matchR(decomp.parts, words, results)) continue;
      const res = results.map(r => this.sub(r, this.posts));
      const reasmb = this.next(decomp);
      if (reasmb[0] === "goto") return this.matchKey(words, this.keys[reasmb[1]]);
      const out = this.reassemble(reasmb, res);
      if (decomp.save) { this.memory.push(out); continue; }
      return out;
    }
    return null;
  }

  respond(text) {
    if (this.quits.includes(text.toLowerCase())) return this.finals[0];
    text = text.replace(/\s*\.+\s*/g, " . ").replace(/\s*,+\s*/g, " , ").replace(/\s*;+\s*/g, " ; ");
    let words = this.sub(text.split(" ").filter(Boolean), this.pres);
    const keys = words.filter(w => this.keys[w.toLowerCase()]).map(w => this.keys[w.toLowerCase()]).sort((a, b) => b.weight - a.weight);
    let out = null;
    for (const k of keys) { out = this.matchKey(words, k); if (out && out.length) break; }
    if (!out || !out.length) {
      if (this.memory.length) out = this.memory.splice(Math.floor(Math.random() * this.memory.length), 1)[0];
      else out = this.next(this.keys.xnone.decomps[0]);
    }
    return out.join(" ");
  }
}
