# Nadia Skills Repository

Official public repository of procedural agent skills and operational directives for the **Nadia AI** assistant platform.

---

## 📋 Overview

Skills in Nadia are modular, procedural capability definitions that instruct cognitive AI agents and specialized staff personas on how to execute domain tasks, invoke specific tools, interface with Python scripts, and coordinate workflows.

This repository serves as the central distribution registry for procedural skills that can be browsed, searched, downloaded, and synchronized directly inside Nadia's **Procedural Skills** panel UI.

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
    │   ├── create-a-skill/SKILL.md     # Procedural skill authoring and packaging guidelines
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
    ├── geo/
    │   ├── alltrails/SKILL.md          # Trailhead routing, elevation profiles, and hiking logistics
    │   ├── aviation/SKILL.md           # Flightradar24 live flight tracking and telemetry
    │   ├── location/SKILL.md           # Coordinates and geocoding resolution
    │   ├── map/SKILL.md                # Map markers, route plotting, and geospatial visualization
    │   ├── satellite/SKILL.md          # N2YO satellite passes and orbit predictions
    │   └── weather/SKILL.md            # Real-time weather telemetry and storm warnings
    ├── hardware/
    │   ├── bambu/SKILL.md              # Bambu 3D printer MQTT monitoring and HMS error analysis
    │   ├── hue/SKILL.md                # Philips Hue smart lighting control
    │   └── plaud/SKILL.md              # Plaud Note audio transcription and AI summaries
    ├── location/
    │   └── location/SKILL.md           # Geospatial coordinate mapping
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
    ├── wordpress/
    │   └── wordpress/SKILL.md          # WordPress content management
    └── writing/
        └── clean-writing/SKILL.md      # AP-style prose, tone constraints, and technical editing
```

---

## 🛠️ SKILL.md Format Specification

Every skill directory MUST contain a `SKILL.md` file featuring a YAML frontmatter header followed by structured markdown instructions.

```yaml
---
name: NameOfSkill
description: Summary description of the skill's purpose and guidelines.
tools: [toolName1, toolName2, toolName3]
---

# Skill Title

Overview and high-level directives explaining when and how the agent should utilize this capability.

## Operational Workflow

1. **Step 1**: First action step...
2. **Step 2**: Tool execution step...

```

---

## 📥 Installing Skills into Nadia

In the **Nadia** desktop client:
1. Open the **Procedural Skills** panel on the left sidebar.
2. Click **📥 Install Skills from GitHub**.
3. Point to this repository (`https://github.com/Ghost-Programmer/nadia-skills`) or any compatible fork.
4. Filter by category or search term, select the desired skills, and click **Install Selected**.
5. Nadia will download the markdown directives and companion scripts into `./skills/<category>/<skill-name>/` and dynamically recompile the active cognitive agents without requiring a restart.

---

## 📄 License & Credits

Copyright (c) 2026 Miller Software Solutions LLC. All rights reserved.
