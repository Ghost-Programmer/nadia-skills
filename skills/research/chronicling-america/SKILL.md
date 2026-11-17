---
name: chronicling-america
description: Searches digitized historical American newspapers (Library of Congress Chronicling America, 1770-1963) and historical genealogy/book archives (Internet Archive / Archive.org) for genealogical and historical research.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: research
  display-name: ChroniclingAmericaSkill
allowed-tools: executeSessionCommand storeBriefEntry searchMemory saveMemory
tools: [executeSessionCommand, storeBriefEntry, searchMemory, saveMemory]
properties: []
---

# Historical Newspapers & Archives Skill (`Chronicling America` & `Archive.org`)

This skill empowers `@Genealogist`, `@Researcher`, and `@Journalist` to search millions of digitized historical American newspaper pages from the **[Library of Congress Chronicling America](https://www.loc.gov/collections/chronicling-america/)** collection (1770–1963) and historical books, vital records, city directories, and snapshots from the **[Internet Archive (`Archive.org`)](https://archive.org)**.

---

## Setup Instructions

### External App & Integration Setup

- **Python 3.10+ Runtime**:
  - Install Python 3.10+ and ensure `python` is on system `PATH`:
    - **Windows**: `winget install Python.Python.3.12` (enable *"Add python.exe to PATH"*)
    - **macOS**: `brew install python`
    - **Linux**: `sudo apt install python3`
  - Uses Python's built-in standard library only (no `pip install` packages required).
- **Historical Archive APIs (Keyless)**:
  - Requires outbound HTTPS access to the [Library of Congress (`loc.gov`)](https://www.loc.gov/apis/) and [Internet Archive (`archive.org`)](https://archive.org/developers/). Works out-of-the-box with no API keys (`properties: []`).
- **Bundled Script**: `~/.nadia/skills/research/chronicling-america/scripts/historical_archive.py`.

---

## 1. Core Operational Workflows

### 1.1 Searching Historical US Newspapers (`newspapers`)
Search digitized historic newspaper pages from the Library of Congress by person name, surname, town/state, and optional year range (`--start-year` / `--end-year`):

```bash
python ~/.nadia/skills/research/chronicling-america/scripts/historical_archive.py newspapers --query "Miller" --state "Ohio" --start-year 1880 --end-year 1920 --limit 10
```

### 1.2 Searching Internet Archive Genealogy & Historical Texts (`archive`)
Search digitized genealogy books, local county histories, parish registers, and historical documents on `Archive.org`:

```bash
python ~/.nadia/skills/research/chronicling-america/scripts/historical_archive.py archive --query "Miller family genealogy Virginia" --limit 10
```

### 1.3 Checking Wayback Machine Snapshots (`wayback`)
Look up archived historical web snapshots for a URL via the Wayback Availability API:

```bash
python ~/.nadia/skills/research/chronicling-america/scripts/historical_archive.py wayback --url "https://example.com" --timestamp "20150101"
```

---

## 2. Genealogical Proof Standard (GPS) & Citation Guidelines

1. **Full Source Citations**: When `@Genealogist` or `@Researcher` cites a newspaper clipping or archive text in a dossier (`~/.nadia/session/brain/`) or response, always include:
   - Newspaper or Publication Title
   - Location (City / State) and Publication Date
   - Direct Library of Congress or `Archive.org` permalink URL
2. **Persist Key Discoveries**: Store verified ancestral or historical findings in episodic memory using `saveMemory`.
