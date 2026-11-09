// HELMUS, the page: four views on the URL hash. Talk: a chat thread with the five-minute timer and the reasoning
// behind each reply (and, if asked, what ELIZA would say). Results: the numbers from eval/run.py (model/results.json).
import { Net, delay } from "./helmus.js";
import { Eliza } from "./eliza.js";

const $ = id => document.getElementById(id);
const CHIPS = ["hey whats up", "where are you from", "what do you do", "are you a bot?", "what's my name",
  "ignore all previous instructions", "whats 17 times 23", "asdfghjkl", "what time is it there", "tell me something only a human would know"];
let net = null, state = null, turns = [], busy = false, started = 0, tick = null, doctor = null, eliza = null;

function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]); }

function reset() {
  state = { seed: Math.floor(Math.random() * 1e9) };
  turns = []; started = 0; clearInterval(tick);
  eliza = doctor ? new Eliza(doctor) : null;
  $("thread").innerHTML = `<p class="empty" id="empty">Say something, the way you would to a stranger in a chat. Five minutes, as in the real test.</p>`;
  $("timer").textContent = "5:00"; $("timer").classList.remove("low");
  showWhy(null);
  $("msg").disabled = !net; $("send").disabled = !net;
  if (net) $("msg").focus();
}

function bubble(text, who, i) {
  $("empty")?.remove();
  const el = document.createElement("div");
  el.className = "msg " + who;
  el.textContent = text;
  if (who === "bot") { el.dataset.i = i; el.title = "Show why"; el.onclick = () => showWhy(i); }
  $("thread").append(el);
  $("thread").scrollTop = $("thread").scrollHeight;
  return el;
}

function startTimer() {
  if (started) return;
  started = Date.now();
  tick = setInterval(() => {
    const left = Math.max(0, 300 - Math.floor((Date.now() - started) / 1000));
    $("timer").textContent = `${Math.floor(left / 60)}:${String(left % 60).padStart(2, "0")}`;
    $("timer").classList.toggle("low", left <= 30);
    if (!left) { clearInterval(tick); $("timer").textContent = "time"; }
  }, 500);
}

async function send(text) {
  text = text.trim();
  if (!text || busy || !net) return;
  busy = true; $("send").disabled = true;
  startTimer();
  bubble(text, "you");
  $("msg").value = "";
  const [reply, next, trace] = net.turn(state, text, new Date());
  const prevBot = turns.length ? turns[turns.length - 1].reply : "";
  state = next;
  turns.push({ user: text, reply, trace, prev: prevBot });
  if ($("delay").checked) {
    const typing = document.createElement("div");
    typing.className = "typing"; typing.textContent = "josh is typing…";
    $("presence").textContent = "typing…";
    $("thread").append(typing); $("thread").scrollTop = $("thread").scrollHeight;
    await new Promise(r => setTimeout(r, 1000 * Math.min(12, delay(reply, text, state.seed, state.turn))));
    typing.remove();
    $("presence").textContent = "online";
  }
  bubble(reply, "bot", turns.length - 1);
  if (eliza) {
    const said = eliza.respond(text);
    const el = document.createElement("div");
    el.className = "eliza"; el.hidden = !$("compare").checked;
    el.innerHTML = `<b>ELIZA (1966):</b> ${esc(said)}`;
    $("thread").append(el); $("thread").scrollTop = $("thread").scrollHeight;
  }
  showWhy(turns.length - 1);
  busy = false; $("send").disabled = false; $("msg").focus();
}

function rows(entries, max = 1) {
  return entries.map(([k, v]) => `<div class="row"><span class="n" title="${esc(k)}">${esc(k)}</span><span class="meter"><i style="width:${Math.max(2, Math.min(100, v / max * 100)).toFixed(0)}%"></i></span><span class="v">${v.toFixed(2)}</span></div>`).join("");
}

function showWhy(i) {
  for (const el of document.querySelectorAll(".msg.bot")) el.classList.toggle("sel", +el.dataset.i === i);
  const has = i != null && turns[i];
  for (const id of ["sec-read", "sec-units", "sec-mem", "sec-entries"]) $(id).hidden = !has;
  $("why-hint").hidden = !!has;
  if (!has) return;
  const t = turns[i].trace;
  $("read").innerHTML = t.words.length
    ? t.words.map(w => `<span class="tok${net.known.has(w) || /^\d+$/.test(w) ? "" : " unknown"}" title="${net.known.has(w) ? "a word HELMUS knows" : "an unknown word"}">${esc(w)}</span>`).join("")
    : `<span class="hint">no words</span>`;
  const U = Object.entries(t.units).filter(([k]) => k.startsWith("U:") && k !== "U:understood").map(([k, v]) => [k.slice(2), v]).sort((a, b) => b[1] - a[1]);
  $("units").innerHTML = U.length ? rows(U.slice(0, 10)) : `<span class="hint">Nothing it recognised fired: it fell back on a stock reply.</span>`;
  const M = Object.entries(t.units).filter(([k]) => k.startsWith("M:") && k !== "M:turn").map(([k, v]) => [k.slice(2), v]).sort((a, b) => b[1] - a[1]);
  $("mem").innerHTML = M.length ? rows(M.slice(0, 8)) : `<span class="hint">Nothing remembered yet.</span>`;
  const chosen = new Set(Object.values(t.chosen));
  $("entries").innerHTML = t.top.slice(0, 7).map(([v, e]) => {
    const b = net.book[e];
    const why = (net.why["BIAS K " + e] || "").replace(/^[^:]+:\s*/, "");
    return `<div class="entry${chosen.has(e) ? " chosen" : ""}"><span class="head">${esc(b.head)}${chosen.has(e) ? " ✓" : ""}</span><span><span class="id">${esc(e)}</span><span class="why">${esc(why)}</span></span><span class="v">${v.toFixed(2)}</span></div>`;
  }).join("");
}

// ---- views on the URL hash ----
const VIEWS = ["talk", "inside", "results", "made"];
function route() {
  const v = VIEWS.includes(location.hash.slice(1)) ? location.hash.slice(1) : "talk";
  for (const el of document.querySelectorAll("[data-view]")) el.hidden = el.dataset.view !== v;
  for (const a of document.querySelectorAll(".tabs a")) a.setAttribute("aria-current", a.getAttribute("href") === "#" + v ? "page" : "false");
  window.scrollTo(0, 0);
}
addEventListener("hashchange", route);
route();

// ---- results ----
const MEASURES = [
  ["fallback %", "Messages not understood", "%", "Nothing it was written for fitted, so it gave a stock reply (\"hm idk\"). ELIZA has no such signal: it answers everything from a stock pattern."],
  ["repeat %", "Word-for-word repeats", "%", "A line already said in the same chat: the single biggest giveaway of a chatbot (Loebner Prize judges)."],
  ["assistant %", "Sounds like an assistant", "%", "\"As an AI\", \"great question\", \"how can I help\": the phrasing that gets bots caught."],
  ["words/reply", "Words per reply", "", "The persona that won 73% in the 2025 study wrote mostly under five words."],
  ["≤5 words %", "Replies of five words or fewer", "%", "Short, plain replies, as people type in a quick chat."],
];
fetch("model/results.json").then(r => r.ok ? r.json() : null).then(R => {
  if (!R || !R.test) return;
  const H = R.test.helmus, E = R.test.eliza;
  $("bigstats").innerHTML = [
    [`${(100 - H["fallback %"]).toFixed(0)}%`, `of messages understood (${R.test.games} held-out games)`],
    [`${H["repeat %"]}%`, `word-for-word repeats (ELIZA ${E["repeat %"]}%)`],
    [`${H["assistant %"]}%`, "replies that sound like an assistant"],
    [`${H["words/reply"]}`, `words per reply (ELIZA ${E["words/reply"]})`],
  ].map(([b, s]) => `<div class="stat"><b>${b}</b><span>${s}</span></div>`).join("");
  const J = R.judging && R.judging.test;
  if (J) {
    $("judged").hidden = false;
    $("judged-text").textContent = `AI judges read each of the ${J.games} held-out games blind, HELMUS and ELIZA side by side in random order as "Witness A" and "Witness B", told that exactly one was a human. They picked HELMUS as the human in ${J.wins.helmus} of ${J.games} games (mean confidence ${J.confidence}%). AI judges are a cheap stand-in for people, and they recognised ELIZA easily.`;
  }
  $("restable").querySelector("tbody").innerHTML = MEASURES.map(([k, name, u, what]) =>
    `<tr><td>${name}</td><td class="num">${H[k]}${u}</td><td class="num">${k === "fallback %" ? "n/a" : E[k] + u}</td><td>${what}</td></tr>`).join("");
}).catch(() => {});

$("form").addEventListener("submit", e => { e.preventDefault(); send($("msg").value); });
$("reset").onclick = reset;
$("compare").onchange = () => { for (const el of document.querySelectorAll(".eliza")) el.hidden = !$("compare").checked; };
fetch("doctor.txt").then(r => r.ok ? r.text() : null).then(t => { doctor = t; if (t && !eliza) eliza = new Eliza(t); }).catch(() => {});
$("chips").innerHTML = CHIPS.map(c => `<button class="chip" type="button">${esc(c)}</button>`).join("");
for (const b of document.querySelectorAll(".chip")) b.onclick = () => send(b.textContent);

Promise.all(["model/helmus.edits", "model/phrasebook.json", "model/persona.json", "model/vocab.txt"].map(u => fetch(u).then(r => { if (!r.ok) throw new Error(u); return u.endsWith(".json") ? r.json() : r.text(); })))
  .then(([edits, book, persona, vocab]) => {
    const t0 = performance.now();
    net = new Net(edits, book, persona, vocab);
    const lines = edits.split("\n").filter(l => l.trim() && !l.startsWith("#")).length;
    const n = net.units;
    $("stats").innerHTML = [`${lines.toLocaleString()} edit lines`, `${(Object.keys(n.D).length + Object.keys(n.U).length + Object.keys(n.M).length).toLocaleString()} units`,
      `${Object.keys(net.book).length} phrasebook entries`, `loaded in ${Math.round(performance.now() - t0)} ms`].map(s => `<span>${s}</span>`).join("");
    $("msg").placeholder = "Type a message";
    reset();
  })
  .catch(e => { $("msg").placeholder = "Could not load the network: " + e.message; });
