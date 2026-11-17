---
name: wikipedia-wikidata
description: Queries Wikipedia articles, summaries, historical "On This Day" events, and structured Wikidata knowledge-graph entities without requiring API keys.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
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

### External App & Integration Setup

- **Python 3.10+ Runtime**:
  - Install Python 3.10+ and ensure `python` is on system `PATH`:
    - **Windows**: `winget install Python.Python.3.12` (enable *"Add python.exe to PATH"*)
    - **macOS**: `brew install python`
    - **Linux**: `sudo apt install python3`
  - Uses Python's built-in standard library only (no `pip install` packages required).
- **Wikimedia REST & Wikidata APIs (Keyless)**:
  - Requires outbound HTTPS access to `https://en.wikipedia.org/api/rest_v1` and `https://www.wikidata.org/w/api.php`. No API keys are required (`properties: []`).
- **Bundled Script**: `~/.nadia/skills/research/wikipedia-wikidata/scripts/wiki_lookup.py`.

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
