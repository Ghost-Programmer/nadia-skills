---
name: app-market-intel
description: Searches mobile and desktop app store rankings, user ratings, version release notes, pricing, and competitor teardowns using AppGoat and Apple App Store Search APIs.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: development
  display-name: AppMarketIntelSkill
allowed-tools: startProject createKanbanCard storeBriefEntry executeSessionCommand searchMemory saveMemory getNadiaProperty setNadiaProperty
tools: [startProject, createKanbanCard, storeBriefEntry, executeSessionCommand, searchMemory, saveMemory, getNadiaProperty, setNadiaProperty]
properties: [nadia.prop.appgoat.apiKey]
---

# App Store & Product Market Intelligence Skill (`AppGoat` & `iTunes Search`)

This skill powers `@Product Manager` in discovering trending mobile/desktop applications and games, analyzing user ratings and feature sets, conducting competitive product teardowns, and drafting Product Requirement Documents (PRDs) in `doc/spec/`.

---

## Setup Instructions

### External App & Integration Setup

- **Python 3.10+ Runtime**:
  - Install Python 3.10+ and ensure `python` is on system `PATH`:
    - **Windows**: `winget install Python.Python.3.12` (enable *"Add python.exe to PATH"*)
    - **macOS**: `brew install python`
    - **Linux**: `sudo apt install python3`
  - Uses Python's built-in standard library only (no `pip install` packages required).
- **AppGoat API Key (`nadia.prop.appgoat.apiKey`)**:
  - Apple App Store Search queries work keyless out-of-the-box.
  - For extended AppGoat market intelligence and rankings, generate an API key from your AppGoat developer dashboard and configure `nadia.prop.appgoat.apiKey` in **⚙️ System Settings ➔ Properties** (`~/.nadia/nadia.properties`) or via `setNadiaProperty`.
- **Bundled Script**: `~/.nadia/skills/development/app-market-intel/scripts/app_market.py`.

---

## 1. Core Operational Workflows

### 1.1 Searching Mobile Apps & Games (`search`)
Search apps or games by category or keyword to retrieve ratings, review counts, bundle IDs, release notes, and pricing:

```bash
python ~/.nadia/skills/development/app-market-intel/scripts/app_market.py search --query "productivity habit tracker" --limit 10
```

### 1.2 Inspecting a Specific App by ID (`lookup`)
Fetch detailed metadata, supported devices, genres, and version history for an app ID:

```bash
python ~/.nadia/skills/development/app-market-intel/scripts/app_market.py lookup --app-id "284882215"
```
