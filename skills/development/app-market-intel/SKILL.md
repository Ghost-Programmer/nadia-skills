---
name: app-market-intel
description: Searches mobile and desktop app store rankings, user ratings, version release notes, pricing, and competitor teardowns using AppGoat and Apple App Store Search APIs.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
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

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/development/app-market-intel/scripts/app_market.py`.
- **Configuration Properties (`nadia.prop.*`)**:
  - Requires `nadia.prop.appgoat.apiKey` in `~/.nadia/nadia.properties` (configure via **Settings ➔ Properties** or `setNadiaProperty`).

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

