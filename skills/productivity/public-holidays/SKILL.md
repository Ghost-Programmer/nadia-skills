---
name: public-holidays
description: Queries official public, bank, and federal holidays across 100+ countries, checks whether today is a public holiday, and retrieves long weekends using the Nager.Date API.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: productivity
  display-name: PublicHolidaysSkill
allowed-tools: executeSessionCommand getCurrentDateTime storeBriefEntry searchMemory saveMemory
tools: [executeSessionCommand, getCurrentDateTime, storeBriefEntry, searchMemory, saveMemory]
properties: []
---

# Worldwide Public & Bank Holidays Skill (`Nager.Date`)

This skill equips `@Personal Assistant` and `@Stock Broker` to query official public, bank, and federal holidays across 100+ countries via the open **[Nager.Date API](https://date.nager.at/Api)**—ideal for scheduling meetings, travel planning, and checking stock market holiday closures.

---

## Setup Instructions

### External App & Integration Setup

- **Python 3.10+ Runtime**:
  - Install Python 3.10+ and ensure `python` is on system `PATH`:
    - **Windows**: `winget install Python.Python.3.12` (enable *"Add python.exe to PATH"*)
    - **macOS**: `brew install python`
    - **Linux**: `sudo apt install python3`
  - Uses Python's built-in standard library only (no `pip install` packages required).
- **Nager.Date Public Holidays API (Keyless)**:
  - Requires outbound HTTPS access to `https://date.nager.at/api/v3`. Works out-of-the-box across 100+ countries with no account or API key (`properties: []`).
- **Bundled Script**: `~/.nadia/skills/productivity/public-holidays/scripts/public_holidays.py`.

---

## 1. Core Operational Workflows

### 1.1 Fetching Upcoming Public Holidays (`upcoming`)
Retrieve the next upcoming public holidays for a country (ISO-3166 alpha-2 code, e.g., `US`, `GB`, `CA`, `DE`, `JP`):

```bash
python ~/.nadia/skills/productivity/public-holidays/scripts/public_holidays.py upcoming --country "US"
```

### 1.2 Listing All Holidays for a Year (`year`)
Retrieve the complete calendar of public holidays for a specific year and country:

```bash
python ~/.nadia/skills/productivity/public-holidays/scripts/public_holidays.py year --country "US" --year 2026
```

### 1.3 Finding Long Weekends (`weekends`)
Identify 3-day and 4-day holiday weekends for travel or sprint planning:

```bash
python ~/.nadia/skills/productivity/public-holidays/scripts/public_holidays.py weekends --country "US" --year 2026
```
