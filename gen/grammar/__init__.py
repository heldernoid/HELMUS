"""The grammar: word tags and a weighted context-free grammar of chat English, written by hand and shared by every
persona. gen/generate.py builds the tags (words.build, after the vocabulary) and imports the rule modules."""
RULES = ["gen.grammar.phrases", "gen.grammar.verbs", "gen.grammar.clauses", "gen.grammar.more", "gen.grammar.chat"]
