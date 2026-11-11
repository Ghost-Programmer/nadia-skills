---
name: wikipedia-wikidata
description: Queries Wikipedia articles, summaries, historical "On This Day" events, and structured Wikidata knowledge-graph entities without requiring API keys.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: research
  display-name: WikipediaWikidataSkill
allowed-tools: executeSessionCommand storeBriefEntry searchMemory saveMemory
tools: [executeSessionCommand, storeBriefEntry, searchMemory, saveMemory]
properties: []
---

# Wikipedia & Wikidata Knowledge Graph Skill

This skill enables `@Researcher`, `@Journalist`, and `@Genealogist` to retrieve encyclopedic summaries, full article extracts, historical "On This Day" milestones, and structured knowledge-graph entities from **[Wikipedia](https://www.mediawiki.org/wiki/API:REST_API)** and **[Wikidata](https://www.wikidata.org/w/api.php)** with zero API keys required.

---

## Setup Instructions

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/research/wikipedia-wikidata/scripts/wiki_lookup.py`.
- **Configuration Properties (`nadia.prop.*`)**: Keyless (`properties: []`).

---

## 1. Core Operational Workflows

### 1.1 Fetching a Wikipedia Article Summary (`summary`)
Retrieve the canonical extract, coordinates (if geo-tagged), Wikidata Q-ID, and URL for a topic:

```bash
python ~/.nadia/skills/research/wikipedia-wikidata/scripts/wiki_lookup.py summary --title "Ada Lovelace"
```

### 1.2 Searching Wikipedia Articles (`search`)
Find matching Wikipedia article titles and snippets:

```bash
python ~/.nadia/skills/research/wikipedia-wikidata/scripts/wiki_lookup.py search --query "Quantum computing" --limit 10
```

### 1.3 Searching Structured Wikidata Entities (`wikidata`)
Resolve people, places, organizations, or concepts to their Wikidata Q-IDs and descriptions:

```bash
python ~/.nadia/skills/research/wikipedia-wikidata/scripts/wiki_lookup.py wikidata --query "Alan Turing" --limit 5
```

### 1.4 Historical "On This Day" Events (`onthisday`)
Retrieve historical events, births, or deaths for a specific month and day:

```bash
python ~/.nadia/skills/research/wikipedia-wikidata/scripts/wiki_lookup.py onthisday --month 11 --day 11 --limit 10
```

