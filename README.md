# Nadia Skills Repository (`agentskills.io` Open Standard)

Official public repository of procedural agent skills and operational directives for the **Nadia AI** assistant platform, fully compliant with the open **[agentskills.io](https://agentskills.io)** standard.

---

## 📋 Overview

Skills in Nadia are modular, procedural capability definitions that instruct cognitive AI agents and specialized staff personas on how to execute domain tasks, invoke specific tools, interface with bundled scripts, and coordinate workflows.

All skills in this repository adhere to the **open `agentskills.io` specification**, enabling:
- **Community Interoperability**: Seamless import of community-built `agentskills.io` skills from GitHub repositories, local directories, or `.zip` packages.
- **Agent-Generated Skill Sharing**: Exporting skills authored by Nadia or users into portable `agentskills.io` packages (`<skill-name>/SKILL.md`, `scripts/`, `references/`, `assets/`).
- **Progressive Disclosure**: Bundled `scripts/`, `references/`, and `assets/` are discovered and exposed on demand without bloating the agent's base context window.

---

## 📂 Repository Structure

Skills are categorized into logical domain directories under the `./skills/` hierarchy:

```
nadia-skills/
├── README.md
└── skills/
    ├── collaboration/
    │   ├── ask-me/SKILL.md             # Interactive user decision and clarification prompts
    │   ├── handoff/SKILL.md            # Inter-staff task delegation and context transfers
    │   └── question/SKILL.md           # Multi-question diagnostic polling and requirements capture
    ├── communication/
    │   └── notification/SKILL.md       # Proactive desktop, audio, and Slack notifications
    ├── development/
    │   ├── antigravity/SKILL.md        # Antigravity (agy) multi-file code generation CLI
    │   ├── architect/SKILL.md          # Architectural Design Documents (ADD) & whiteboards
    │   ├── create-a-skill/SKILL.md     # Procedural skill authoring and agentskills.io packaging guide
    │   ├── github/SKILL.md             # Git version control, branch management, and PR triage
    │   ├── product-manager/SKILL.md    # Product Specifications (PRDs) and user stories
    │   ├── project/SKILL.md            # Sandbox workspace switching and build lifecycle
    │   ├── quality-engineer/SKILL.md   # Test strategies, automated execution, and defect logging
    │   ├── software-engineer/SKILL.md  # Full-stack implementation (Android, JavaFX, Angular, Spring Boot)
    │   └── ui-designer/SKILL.md        # Material 3 design tokens, wireframing, and JavaFX CSS
    ├── finance/
    │   └── stocks/                     # Yahoo Finance market data, quotes, and equity resolution
    │       ├── SKILL.md
    │       └── scripts/finance_api.py
    ├── genealogy/
    │   ├── family-analysis/            # Kinship calculation, MRCA, shared DNA (cM), and pedigree charts
    │   │   ├── SKILL.md
    │   │   └── scripts/family_analyzer.py
    │   ├── gedcom/                     # GEDCOM 5.5/7.0 tree parser, validation, vitals, and anomaly detection
    │   │   ├── SKILL.md
    │   │   └── scripts/gedcom_tool.py
    │   └── record-matching/            # Historical record matching (Census, SSDI), Soundex, and alias scoring
    │       ├── SKILL.md
    │       └── scripts/record_matcher.py
    ├── geo/
    │   ├── alltrails/SKILL.md          # Trailhead routing, elevation profiles, and hiking logistics
    │   ├── aviation/SKILL.md           # OpenSky live flight tracking and telemetry
    │   ├── location/SKILL.md           # Coordinates and geocoding resolution
    │   ├── map/SKILL.md                # Map markers, route plotting, and geospatial visualization
    │   ├── satellite/SKILL.md          # N2YO satellite passes and orbit predictions
    │   └── weather/SKILL.md            # Real-time weather telemetry and storm warnings
    ├── hardware/
    │   ├── bambu/SKILL.md              # Bambu 3D printer MQTT monitoring and HMS error analysis
    │   ├── hue/SKILL.md                # Philips Hue smart lighting control
    │   └── plaud/SKILL.md              # Plaud Note audio transcription and AI summaries
    ├── media/
    │   ├── wordpress/SKILL.md          # Multi-site WordPress publishing and REST API
    │   └── ytmusic/SKILL.md            # YouTube Music playback and playlist management
    ├── productivity/
    │   ├── brief/SKILL.md              # Daily intelligence briefs persistence and recall
    │   ├── calendar/SKILL.md           # Google Calendar scheduling and pre-meeting alarms
    │   ├── contacts/SKILL.md           # Google Contacts synchronization
    │   ├── documents/SKILL.md          # Google Docs authoring and document formatting
    │   ├── drive/SKILL.md              # Google Drive file storage and SAF exports
    │   ├── email/SKILL.md              # Gmail intake, IMAP IDLE push, and outbound drafts
    │   ├── note/SKILL.md               # Quick notes and scratchpad capture
    │   ├── presentations/SKILL.md      # Slide presentation generation
    │   ├── spreadsheets/SKILL.md       # Google Sheets and CSV calculation tables
    │   └── tasks/SKILL.md              # Google Tasks and Kanban task orchestration
    ├── research/
    │   ├── blogwatcher/SKILL.md        # Competitor blog monitoring and RSS feeds
    │   ├── database/SKILL.md           # Dynamic SQL query execution and schema inspection
    │   ├── dossier/                    # Subject background investigations and dossier authoring
    │   │   ├── SKILL.md
    │   │   └── scripts/dossier_helper.py
    │   └── web-research/SKILL.md       # Deep web research, synthesis, and citation formatting
    ├── system/
    │   ├── datetime/SKILL.md           # Temporal awareness and timestamp parsing
    │   ├── docker/SKILL.md             # Container lifecycle management and inspections
    │   ├── general/SKILL.md            # General system directives and shell execution
    │   ├── memory/SKILL.md             # Semantic RAG memory recall and episodic facts
    │   └── network/SKILL.md            # Nmap LAN sweeps, MAC vendor resolution, and IoT topology
    └── writing/
        └── clean-writing/SKILL.md      # AP-style prose, tone constraints, and technical editing
```

---

## 🛠️ `SKILL.md` Format Specification (`agentskills.io` Open Standard)

Every skill directory contains a required `SKILL.md` file with YAML frontmatter compliant with the [agentskills.io specification](https://agentskills.io), followed by procedural Markdown instructions and optional `scripts/`, `references/`, and `assets/` subdirectories:

```yaml
---
name: skill-name
description: Concise summary of what the skill does and when the agent should use it (max 1024 chars).
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: development
  display-name: SkillNameSkill
allowed-tools: toolName1 toolName2
tools: [toolName1, toolName2]
---

# Skill Title

Overview and high-level directives explaining when and how the agent should utilize this capability.

## Operational Workflow

1. **Step 1**: First action step...
2. **Step 2**: Tool execution step...
```

---

## 📥 Importing & Sharing Skills in Nadia

1. **Install from GitHub (`agentskills.io` Repositories)**:
   - Open **Tools ➔ 🧩 Download & Install Skills...** (or click **📥 Install Skills** in the left **Procedural Skills** panel).
   - Enter `https://github.com/Ghost-Programmer/nadia-skills` or any community `agentskills.io` GitHub repository URL and click **🔍 Scan Repository**.
2. **Import Local Folder or `.zip` Package**:
   - In the Skill Installer dialog, click **📂 Import Folder...** or **📦 Import ZIP...** to import community-built `agentskills.io` skills directly from disk.
3. **Share / Export Agent-Generated Skills**:
   - Open any skill in the **Skill Editor** and click **📦 Share / Export (.zip)** (or **✓ Normalize (agentskills.io)**) to bundle `SKILL.md` along with `scripts/`, `references/`, and `assets/` into a standard `agentskills.io` `.zip` package.

---

## 📄 License & Credits

Licensed under the Apache License, Version 2.0 (`Apache-2.0`).  
Copyright (c) 2026 Miller Software Solutions LLC. All rights reserved.
