---
name: lexicon
description: Queries word definitions, phonetics, etymologies, synonyms, antonyms, and classic literary poetry using the Free Dictionary API and PoetryDB without requiring API keys.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: writing
  display-name: LexiconSkill
allowed-tools: executeSessionCommand searchMemory saveMemory
tools: [executeSessionCommand, searchMemory, saveMemory]
properties: []
---

# Lexicon, Dictionary & Literary Reference Skill (`Free Dictionary` & `PoetryDB`)

This skill empowers `@Journalist` and `@Researcher` with instant dictionary definitions, parts of speech, IPA phonetics, synonyms, antonyms, usage examples via **[Free Dictionary API](https://dictionaryapi.dev/)**, and classic literary verse lookup via **[PoetryDB](https://poetrydb.org/)**.

---

## Setup Instructions

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/writing/lexicon/scripts/lexicon_lookup.py`.
- **Configuration Properties (`nadia.prop.*`)**: Keyless (`properties: []`).

---

## 1. Core Operational Workflows

### 1.1 Looking Up Word Definitions, Synonyms & Phonetics (`define`)
Retrieve parts of speech, definitions, synonyms, antonyms, and IPA pronunciation for an English word:

```bash
python ~/.nadia/skills/writing/lexicon/scripts/lexicon_lookup.py define --word "ephemeral"
```

### 1.2 Searching Classic Literature & Poetry (`poetry`)
Search poems by author, title, or line text via PoetryDB:

```bash
python ~/.nadia/skills/writing/lexicon/scripts/lexicon_lookup.py poetry --author "Emily Dickinson" --limit 5
```

