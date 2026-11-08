// Run the browser engine (web/helmus.js) on chats from a JSON file and print each reply and its chosen entries.
// Used by tests/test_parity.py: node tests/parity.mjs cases.json <model folder>
import { readFileSync } from "node:fs";
import { Net } from "../web/helmus.js";

const [cases, model] = [JSON.parse(readFileSync(process.argv[2], "utf8")), process.argv[3]];
const net = new Net(readFileSync(model + "/helmus.edits", "utf8"), JSON.parse(readFileSync(model + "/phrasebook.json", "utf8")),
  JSON.parse(readFileSync(model + "/persona.json", "utf8")), readFileSync(model + "/vocab.txt", "utf8"));
const out = cases.map(c => {
  let st = { seed: c.seed };
  return c.messages.map((m, i) => {
    const [r, s, tr] = net.turn(st, m, new Date(c.now + i * 60000));
    st = s;
    return { reply: r, chosen: tr.chosen, units: tr.units };
  });
});
console.log(JSON.stringify(out));
