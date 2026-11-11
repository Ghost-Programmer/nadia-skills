# Nadia Skills Repository (`agentskills.io` Open Standard)

Official public repository of procedural agent skills, bundled executable scripts, and operational directives for the **Nadia AI** cognitive assistant platform, fully compliant with the open **[agentskills.io](https://agentskills.io)** standard.

---

## 📋 Overview

Skills in Nadia are modular, procedural capability packages that instruct cognitive AI agents and specialized staff personas on how to execute domain tasks, invoke Spring AI `@NadiaTool` functions, run bundled helper scripts, and coordinate multi-agent workflows.

All skills in this repository adhere to the **open [agentskills.io](https://agentskills.io) specification**, enabling:
- **Community Interoperability**: Seamless import of community-built `agentskills.io` skills from GitHub repositories, local skill directories (`📂 Import Folder...`), or portable `.zip` archives (`📦 Import ZIP...`).
- **Agent-Generated Skill Sharing**: Normalizing (`✓ Normalize (agentskills.io)`) and exporting (`📦 Share / Export (.zip)`) skills authored by Nadia or users into portable `agentskills.io` packages (`<skill-name>/SKILL.md`, `scripts/`, `references/`, `assets/`).
- **Progressive Disclosure**: Bundled `scripts/`, `references/`, and `assets/` subdirectories are automatically discovered and indexed on demand without bloating the agent's base context window.

---

## 📂 Repository Structure

Skills are organized into 12 domain category directories under `./skills/`:

```text
nadia-skills/
├── README.md
└── skills/
    ├── TEMPLATE.md                             # Official base template for authoring agentskills.io SKILL.md files
    ├── collaboration/
    │   ├── ask-me/SKILL.md                     # Interactive user decision and clarification prompts
    │   ├── handoff/SKILL.md                    # Inter-staff task delegation and @<StaffName> context transfers
    │   └── question/SKILL.md                   # Multi-question diagnostic polling and requirements capture
    ├── communication/
    │   └── notification/SKILL.md               # Proactive desktop, audio, and Slack (#general / #alert) notifications
    ├── development/
    │   ├── antigravity/SKILL.md                # Antigravity (agy) multi-file code generation CLI orchestration
    │   ├── architect/SKILL.md                  # Architectural Design Documents (doc/add/) & multi-tier whiteboards
    │   ├── create-a-skill/SKILL.md             # Procedural skill authoring & agentskills.io packaging guide
    │   ├── github/SKILL.md                     # Git version control, branch management, and PR triage
    │   ├── product-manager/SKILL.md            # Product Specifications (doc/spec/), teardowns & Kanban backlogs
    │   ├── project/SKILL.md                    # Sandbox workspace switching (startProject / stopProject) & lifecycle
    │   ├── quality-engineer/SKILL.md           # Test strategies (doc/test/), automated suites & defect triage
    │   ├── software-engineer/SKILL.md          # Full-stack implementation (Android, JavaFX, Angular, Spring Boot)
    │   └── ui-designer/SKILL.md                # Material 3 design tokens, JavaFX CSS & .whiteboard wireframes
    ├── finance/
    │   └── stocks/                             # Yahoo Finance market data, quotes, fundamentals & watchlists
    │       ├── SKILL.md
    │       └── scripts/finance_api.py
    ├── genealogy/
    │   ├── family-analysis/                    # Kinship calculation, MRCA, shared DNA (cM) & pedigree charts
    │   │   ├── SKILL.md
    │   │   └── scripts/family_analyzer.py
    │   ├── gedcom/                             # GEDCOM 5.5/7.0 parser, validation, RAG fact extraction & vitals
    │   │   ├── SKILL.md
    │   │   └── scripts/gedcom_tool.py
    │   └── record-matching/                    # Historical record matching (Census, SSDI), Soundex & alias scoring
    │       ├── SKILL.md
    │       └── scripts/record_matcher.py
    ├── geo/
    │   ├── alltrails/SKILL.md                  # Trailhead routing, elevation profiles, and hiking logistics
    │   ├── aviation/SKILL.md                   # OpenSky Network live regional aircraft tracking and telemetry
    │   ├── flight-tracker/SKILL.md             # Single-target aircraft/satellite tracking with auto-pan World Map
    │   ├── location/                           # Coordinates, reverse geocoding, and place resolution
    │   │   ├── SKILL.md
    │   │   └── scripts/geocoding.py
    │   ├── map/SKILL.md                        # Interactive World Map markers, viewports, and layer controls
    │   ├── satellite/SKILL.md                  # N2YO orbital satellite pass predictions and live tracking
    │   └── weather/                            # Real-time Open-Meteo weather telemetry, forecasts & alerts
    │       ├── SKILL.md
    │       └── scripts/weather.py
    ├── hardware/
    │   ├── bambu/SKILL.md                      # Bambu Lab 3D printer MQTT telemetry, job control & HMS diagnostics
    │   ├── camera/SKILL.md                     # USB/ONVIF/IP & Bambu 3D printer cameras (~/.nadia/captures)
    │   ├── hue/SKILL.md                        # Philips Hue smart bridge & lighting control
    │   └── plaud/                              # Plaud Note audio recording sync, transcription & AI summaries
    │       ├── SKILL.md
    │       └── scripts/plaud_cli.py
    ├── media/
    │   ├── wordpress/                          # Multi-site WordPress REST API publishing and draft management
    │   │   ├── SKILL.md
    │   │   └── scripts/wordpress_api.py
    │   └── ytmusic/                            # YouTube Music search, playback, and playlist management
    │       ├── SKILL.md
    │       └── scripts/ytmusic_cli.py
    ├── productivity/
    │   ├── brief/SKILL.md                      # Daily intelligence brief persistence, synthesis, and anti-duplication
    │   ├── calendar/SKILL.md                   # Google Calendar scheduling, conflict checks & pre-meeting alarms
    │   ├── contacts/SKILL.md                   # Google Contacts lookup and directory synchronization
    │   ├── docs/skills.md                      # Google Workspace (gws) CLI reference index
    │   ├── documents/SKILL.md                  # Google Docs authoring and structured document formatting
    │   ├── drive/SKILL.md                      # Google Drive file queries, uploads, and report ingestion
    │   ├── email/SKILL.md                      # Gmail IMAP IDLE push intake, labeling & Draft_Created anti-duplication
    │   ├── note/SKILL.md                       # Quick notes and executive scratchpad capture
    │   ├── presentations/SKILL.md              # Google Slides presentation creation and deck structuring
    │   ├── spreadsheets/SKILL.md               # Google Sheets and CSV tabular data workflows
    │   └── tasks/SKILL.md                      # Google Tasks and action item management
    ├── research/
    │   ├── blogwatcher/SKILL.md                # Competitor & tech blog RSS/Atom monitoring (watchBlog)
    │   ├── database/SKILL.md                   # Dynamic SQL query execution and schema inspection
    │   ├── dossier/                            # Comprehensive subject investigations & dossier compilation
    │   │   ├── SKILL.md
    │   │   └── scripts/dossier_helper.py
    │   └── web-research/SKILL.md               # Multi-source web research, fact verification & citation synthesis
    ├── system/
    │   ├── datetime/SKILL.md                   # System clock, timezone awareness, and ISO-8601 timestamping
    │   ├── docker/SKILL.md                     # Docker container, image, volume, and network lifecycle management
    │   ├── general/SKILL.md                    # Sandbox shell command execution (executeSessionCommand)
    │   ├── memory/SKILL.md                     # Semantic PGVector episodic memory recall & fact persistence
    │   └── network/SKILL.md                    # Zero-trust network approval, Nmap LAN topology & port auditing
    └── writing/
        └── clean-writing/SKILL.md              # AP-style journalism, tone discipline, and prose editing
```

---

## 🧩 Available Procedural Skills Catalog

| Category | `agentskills.io` Name | Display Name | Bound Tools / Bundled Scripts | Summary |
| :--- | :--- | :--- | :--- | :--- |
| **collaboration** | `ask-me` | `AskMeSkill` | *(Conversational protocol)* | Interactive user clarification and decision-point prompting. |
| **collaboration** | `handoff` | `HandoffSkill` | *(Inter-staff `@<StaffName>` protocol)* | Multi-agent task delegation and context handoff across staff specialists. |
| **collaboration** | `question` | `QuestionSkill` | *(Conversational protocol)* | Structured multi-question requirements gathering. |
| **communication** | `notification` | `NotificationSkill` | `sendSlackNotification`, `getSlackNotificationChannel` | Desktop notifications and Slack (`#general` / `#alert`) dispatches. |
| **development** | `antigravity` | `AntigravitySkill` | `executeSessionCommand` | Orchestrating Google Antigravity (`agy`) CLI for code generation and static analysis. |
| **development** | `architect` | `ArchitectSkill` | `cloneRepository`, `generateDiagram`, `renderMermaidDiagram`, `getWhiteboardDiagramState`, `executeSessionCommand` | Architectural Design Documents (`doc/add/`) and multi-tier `.whiteboard` diagrams. |
| **development** | `create-a-skill` | `CreateSkillSkill` | *(Skill authoring guide)* | Authoring, validating, and packaging `agentskills.io`-compliant skills. |
| **development** | `github` | `GitHubSkill` | `cloneRepository`, `executeSessionCommand` | Git repository cloning, branching, commits, and pull request workflows. |
| **development** | `product-manager` | `ProductManagerSkill` | `startProject`, `stopProject`, `createCard`, `moveCard`, `listCards`, `storeBriefEntry`, `executeSessionCommand` | Trending app teardowns, PRDs (`doc/spec/`), MoSCoW scoping, and Kanban backlogs. |
| **development** | `project` | `ProjectSkill` | `startProject`, `stopProject`, `listProjects` | Switching and isolating project workspace sandboxes under `~/.nadia/session/projects/`. |
| **development** | `quality-engineer` | `QualityEngineerSkill` | `startProject`, `stopProject`, `createCard`, `moveCard`, `executeSessionCommand` | Test plans (`doc/test/`), automated test execution, and Kanban bug triage. |
| **development** | `software-engineer` | `SoftwareEngineerSkill` | `startProject`, `stopProject`, `moveCard`, `dockerListContainers`, `dockerStartContainer`, `executeSessionCommand` | Full-stack Android, JavaFX, Angular, and Spring Boot implementation (`ai.nadia`). |
| **development** | `ui-designer` | `UiDesignerSkill` | `startProject`, `stopProject`, `generateDiagram`, `getWhiteboardDiagramState`, `executeSessionCommand` | Material 3 tokens, splash screen credits, JavaFX CSS, and `.whiteboard` wireframes. |
| **finance** | `stocks` | `StockAnalysisSkill` | `executeSessionCommand`, `scripts/finance_api.py` | Real-time Yahoo Finance stock quotes, fundamentals, and market sweeps. |
| **genealogy** | `family-analysis` | `FamilyAnalysisSkill` | `executeSessionCommand`, `scripts/family_analyzer.py` | Kinship path calculation, MRCA discovery, shared DNA (cM), and pedigree charts. |
| **genealogy** | `gedcom` | `GedcomSkill` | `executeSessionCommand`, `saveMemory`, `scripts/gedcom_tool.py` | GEDCOM 5.5/7.0 parsing, tree validation, anomaly checks, and RAG memory extraction. |
| **genealogy** | `record-matching` | `RecordMatchingSkill` | `executeSessionCommand`, `scripts/record_matcher.py` | Historical record matching (Census, SSDI, Find A Grave) and Soundex scoring. |
| **geo** | `alltrails` | `AllTrailsSkill` | `executeSessionCommand` | Trail discovery, distance/elevation analysis, and outdoor trek matching. |
| **geo** | `aviation` | `AviationSkill` | `trackPlanes`, `startContinuousPlaneTracking`, `stopContinuousPlaneTracking`, `getPlaneTrackingStatus` | Regional live aircraft radar sweeps via OpenSky Network. |
| **geo** | `flight-tracker` | `FlightTrackerSkill` | `trackFlight`, `stopTrackingFlight`, `getTrackedFlightStatus`, `recenterOnTrackedFlight`, `centerMap`, `setMapView`, `storeBriefEntry` | Single-target aircraft/satellite lock, 18% viewport edge auto-recentering, and FAA registry briefings. |
| **geo** | `location` | `LocationSkill` | `getGeoLocation`, `executeSessionCommand`, `scripts/geocoding.py` | Coordinate resolution, IP geolocation, and reverse geocoding. |
| **geo** | `map` | `MapSkill` | `centerMap`, `setMapView`, `showMap`, `clearMap` | Interactive World Map viewport control and geospatial plotting. |
| **geo** | `satellite` | `SatelliteSkill` | `trackSatellites`, `startContinuousSatelliteTracking`, `stopContinuousSatelliteTracking`, `getSatelliteTrackingStatus` | N2YO orbital satellite tracking and pass predictions. |
| **geo** | `weather` | `WeatherSkill` | `weather`, `executeSessionCommand`, `scripts/weather.py` | Live meteorological conditions, multi-day forecasts, and storm alerts. |
| **hardware** | `bambu` | `BambuSkill` | `listPrinters`, `getPrinterStats`, `startPrinterMonitor`, `startPrintJob`, `pausePrintJob`, `resumePrintJob`, `stopPrintJob` | Bambu Lab 3D printer telemetry, job control, HMS diagnostics, and zero-trust guard. |
| **hardware** | `camera` | `CameraSkill` | `listCameras`, `discoverCameras`, `connectCamera`, `disconnectCamera`, `takePhoto`, `startRecording`, `stopRecording`, `openCameraViewer` | USB/IP/ONVIF and Bambu 3D printer chamber camera streaming and captures (`~/.nadia/captures`). |
| **hardware** | `hue` | `PhilipsHueSkill` | `listHueLights`, `setHueLightState`, `setHueLightColor`, `discoverHueBridges` | Philips Hue smart lighting discovery, dimming, and color control. |
| **hardware** | `plaud` | `PlaudSkill` | `executeSessionCommand`, `scripts/plaud_cli.py` | Plaud Note voice recording synchronization, transcription, and summaries. |
| **media** | `wordpress` | `WordpressSkill` | `getWordpressSitesList`, `publishWordpressPost`, `scripts/wordpress_api.py` | Multi-site WordPress article publishing and media management. |
| **media** | `ytmusic` | `YouTubeMusicSkill` | `executeSessionCommand`, `scripts/ytmusic_cli.py` | YouTube Music search, track playback, and playlist curation. |
| **productivity** | `brief` | `BriefSkill` | `storeBriefEntry`, `appendBriefEntry`, `getBriefEntries`, `deleteBriefEntry`, `clearBriefEntries` | Persistent daily brief logging, categorization, and anti-duplication cleanup. |
| **productivity** | `calendar` | `CalendarSkill` | `executeSessionCommand` (`gws calendar`) | Google Calendar event scheduling, free/busy checks, and pre-meeting alarms. |
| **productivity** | `contacts` | `ContactsSkill` | `executeSessionCommand` (`gws people`) | Google Contacts lookup and VIP contact synchronization. |
| **productivity** | `documents` | `DocumentsSkill` | `executeSessionCommand` (`gws docs`) | Google Docs creation, reading, and structured content updates. |
| **productivity** | `drive` | `DriveSkill` | `executeSessionCommand` (`gws drive`) | Google Drive file search, upload/download, and PDF/Sheet export. |
| **productivity** | `email` | `EmailSkill` | `executeSessionCommand` (`gws gmail`) | Gmail triage, labeling, and reply drafting with `Draft_Created` anti-duplication. |
| **productivity** | `note` | `NoteSkill` | `storeBriefEntry`, `saveMemory` | Quick executive notes and scratchpad persistence. |
| **productivity** | `presentations` | `PresentationsSkill` | `executeSessionCommand` (`gws slides`) | Google Slides deck generation and slide updates. |
| **productivity** | `spreadsheets` | `SpreadsheetsSkill` | `executeSessionCommand` (`gws sheets`) | Google Sheets reading, row appending, and tabular formulas. |
| **productivity** | `tasks` | `TasksSkill` | `executeSessionCommand` (`gws tasks`) | Google Tasks list and action item management. |
| **research** | `blogwatcher` | `BlogWatcherSkill` | `watchBlog`, `storeBriefEntry` | Automated RSS/Atom tech and competitor blog monitoring. |
| **research** | `database` | `DatabaseSkill` | `executeSqlQuery`, `listDatabaseTables`, `describeDatabaseTable` | Relational & PGVector database schema inspection and read-only SQL queries. |
| **research** | `dossier` | `DossierSkill` | `executeSessionCommand`, `searchMemory`, `saveMemory`, `scripts/dossier_helper.py` | Deep-dive subject dossiers stored in `~/.nadia/session/brain/`. |
| **research** | `web-research` | `WebResearchSkill` | `executeSessionCommand`, `searchMemory`, `saveMemory`, `storeBriefEntry` | Multi-source web research, cross-verification, and cited summaries. |
| **system** | `datetime` | `DateTimeSkill` | `getCurrentDateTime` | System clock queries, timezone conversion, and timestamp generation. |
| **system** | `docker` | `DockerSkill` | `dockerListContainers`, `dockerStartContainer`, `dockerStopContainer`, `dockerContainerLogs`, `dockerInspectContainer` | Docker container, image, volume, and network management. |
| **system** | `general` | `GeneralSystemSkill` | `executeSessionCommand` | Safe sandbox command-line execution and local file operations. |
| **system** | `memory` | `MemorySkill` | `searchMemory`, `saveMemory`, `updateMemory`, `deleteMemory`, `listMemories` | Episodic vector memory search and long-term fact storage. |
| **system** | `network` | `NetworkSkill` | `checkNetworkApproval`, `approveCurrentNetwork`, `listApprovedNetworks`, `getNetworkTopology`, `scanPorts`, `dnsLookup`, `traceRoute` | Zero-trust network authorization, Nmap LAN topology sweeps, and port diagnostics. |
| **writing** | `clean-writing` | `CleanWritingSkill` | *(Editorial protocol)* | AP-style prose formatting, clarity, and tone guidelines. |

---

## 🛠️ `SKILL.md` Format Specification (`agentskills.io` Open Standard)

Every skill directory contains a required `SKILL.md` file with YAML frontmatter compliant with the [agentskills.io specification](https://agentskills.io), followed by procedural Markdown instructions and optional `scripts/`, `references/`, and `assets/` subdirectories (see [`skills/TEMPLATE.md`](skills/TEMPLATE.md) for the official starter template):

| Frontmatter Field | Required | Specification |
| :--- | :--- | :--- |
| **`name`** | **Yes** | Lowercase kebab-case (`^[a-z0-9]+(-[a-z0-9]+)*$`), 1–64 chars, matching the parent skill directory name (e.g., `create-a-skill`, `flight-tracker`). |
| **`description`** | **Yes** | Non-empty summary (1–1024 chars) explaining **what** the skill does and **when** the agent should trigger it. |
| **`license`** | Optional | SPDX license identifier or bundled license reference (e.g., `Apache-2.0`, `MIT`). |
| **`compatibility`** | Optional | Environment or runtime requirements (up to 500 chars). |
| **`metadata`** | Optional | String key-value map (`author`, `version`, `category`, `display-name`). |
| **`allowed-tools`** | Optional | Space-delimited list of pre-approved tools per `agentskills.io` (merged and deduplicated with `tools`). |
| **`tools`** | Optional | YAML array of bound Nadia `@NadiaTool` names. |
| **`properties`** | Optional | YAML array of required `nadia.prop.*` configuration property keys (e.g., `[nadia.prop.n2yo.apiKey]`). Registered automatically with `NadiaPropertiesService` when the skill loads so the Settings UI displays them. |

```yaml
---
name: skill-name
description: Concise, actionable summary of what this skill does and the specific trigger conditions when the agent should use it (1-1024 characters).
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: general
  display-name: ExampleSkill
allowed-tools: toolName1 toolName2
tools: [toolName1, toolName2]
properties: []
---

# Example Skill Title

Overview and high-level directives explaining when and how the agent should utilize this capability.

## Operational Workflow

1. **Step 1**: Context and parameter validation...
2. **Step 2**: Tool or bundled script execution...
```

---

## ⚙️ Skill & Tool Properties (`nadia.prop.*`)

All configuration settings, API keys, credentials, and parameters required by procedural skills or tools are stored in `~/.nadia/nadia.properties` using the **`nadia.prop.`** prefix (for example: `nadia.prop.n2yo.apiKey`, `nadia.prop.opensky.username`, `nadia.prop.opensky.password`, `nadia.prop.webcams.windy.api-key`, `nadia.prop.windy.api-key`).

- **UI Configuration**: Users can view, add, edit, or delete any `nadia.prop.*` property in the **Settings ➔ Properties** tab (`SettingsWindowView`).
- **Agent & Tool Access**: Skills and agents can query or update `nadia.prop.*` settings via the `NadiaPropertiesTool` functions (`getNadiaProperty`, `setNadiaProperty`, `listNadiaProperties`, `deleteNadiaProperty`), and Java services/tools resolve them via `NadiaPropertiesService` or `@Value("${nadia.prop.<name>:}")`.

---

## 📥 Importing, Authoring & Sharing Skills in Nadia

1. **Install from GitHub (`agentskills.io` Repositories)**:
   - Open **Tools ➔ 🧩 Download & Install Skills...** (or click **📥 Install Skills** in the left **Procedural Skills** panel).
   - Enter `https://github.com/Ghost-Programmer/nadia-skills` or any community `agentskills.io` GitHub repository URL and click **🔍 Scan Repository**.
   - Select the skills to install or update and click **📥 Install Selected**. Nadia installs the skills into `~/.nadia/skills/` (along with `skills/TEMPLATE.md`) and reloads the skill registry immediately.
2. **Import Local Skill Folder or `.zip` Archive**:
   - In the Skill Installer dialog, click **📂 Import Folder...** or **📦 Import ZIP...** to import community-built `agentskills.io` skills (including `scripts/`, `references/`, and `assets/`) directly from disk.
3. **Author, Normalize & Share Agent-Generated Skills**:
   - Click **➕ Add Skill** in the Procedural Skills panel to scaffold a new skill from `skills/TEMPLATE.md`.
   - In the **Skill Editor**, click **✓ Normalize (agentskills.io)** to validate and format YAML frontmatter, or click **📦 Share / Export (.zip)** to bundle the skill directory (`SKILL.md`, `scripts/`, `references/`, `assets/`) into a portable `agentskills.io` `.zip` archive.

---

## 📄 License & Credits

Licensed under the Apache License, Version 2.0 (`Apache-2.0`).  
Copyright (c) 2026 Miller Software Solutions LLC. All rights reserved.
