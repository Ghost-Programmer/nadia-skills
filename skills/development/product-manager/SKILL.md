---
name: ProductManagerSkill
description: Guidelines and workflows for trend identification, competitive teardowns of mobile/desktop applications and games, authoring structured Product Specifications (PRD/App Spec) in doc/spec/ or PRODUCT_SPEC.md, defining user stories, acceptance criteria, and organizing Kanban development backlogs.
tools: [startProject, stopProject, listProjects, storeBriefEntry, appendBriefEntry, getBriefEntries, searchMemory, saveMemory, updateMemory, getCurrentDateTime, executeSessionCommand, getKanbanBoard, createKanbanCard, updateKanbanCard, moveKanbanCard, generateDiagram, renderMermaidDiagram]
---

# Product Strategy & Specification Skill

This skill guides agents in discovering market trends, conducting deep product teardowns for applications and games, formulating comprehensive **Product Specifications (PRDs / App Specs)** in `doc/spec/`, and orchestrating the software development backlog across the Software Development Group (`@UI Designer`, `@Software Architect`, `@Software Engineer`, `@Quality Engineer`).

---

## 1. App & Game Market Trend Analysis Workflow

When evaluating market opportunities, researching viral apps, or deconstructing game mechanics:

1. **Identify Market Trends**:
   - Analyze target domain (mobile utility, casual/strategy games, developer tools, productivity suites).
   - Evaluate user acquisition loops, viral mechanics, retention drivers (daily streaks, push loops, reward schedules), and monetization models (freemium, in-app purchases, subscriptions, ad-supported).
2. **Conduct Product / Game Teardown**:
   - **Core Loop**: Map the primary user cycle (e.g., Input -> Process -> Feedback -> Reward -> Progression).
   - **First-Time User Experience (FTUE)**: Assess onboarding speed, tutorial clarity, and cognitive friction.
   - **Competitive Benchmarking**: Formulate a comparison table highlighting competitor strengths, weaknesses, and Nadia's value proposition.

---

## 2. Product Specification (PRD / App Spec) Authoring Workflow

When authoring a specification for a project or feature:

1. **Activate Project Workspace**:
   - Call `startProject` with `{"projectName": "<projectName>"}` to switch to `./session/projects/<projectName>`.
2. **Ensure `doc/spec` Directory Exists**:
   - Call `executeSessionCommand` with `{"command": "python -c \"import os; os.makedirs('doc/spec', exist_ok=True)\"", "dir": "."}`.
3. **Determine Sequential Specification Number**:
   - Inspect existing files in `doc/spec/` to generate the next 4-digit number (e.g. `doc/spec/0001-product-specification.md`).
4. **Draft Comprehensive Specification**:
   - **Executive Summary & Problem Statement**: Clear rationale and user value.
   - **User Personas & Use Cases**: Detailed user journeys.
   - **MoSCoW Feature Scope**:
     - *Must-Have (MVP)*: Minimum viable launch features.
     - *Should-Have*: Near-term priority enhancements.
     - *Could-Have*: Future exploration.
     - *Won't-Have*: Explicit scope exclusions.
   - **User Stories with Given/When/Then Acceptance Criteria**: Measurable criteria for implementation and QA.
   - **UI/UX Expectations**: Layout and interaction notes for Android, JavaFX, and Angular frontends.
5. **Populate Kanban Backlog**:
   - Call `createKanbanCard` for each MVP story, tagging the appropriate specialist (`UI Designer`, `Software Architect`, `Software Engineer`, `Quality Engineer`).
6. **Log Brief Entry & Deliver**:
   - Call `storeBriefEntry` with category `project` or `todo` and deliver a structured summary.

---

## 3. Nightly Android Product Investigation & Project Creation Procedure

When triggered by the nightly discovery cron (`recurring-4d82e19f`) or when executing a market sweep:

1. **Investigate an Android Product Not Done Before**:
   - Inspect existing projects under `./session/projects/` to avoid duplicates.
   - Investigate innovative, high-utility Android apps that have not been designed or implemented in the workspace before.
   - Determine if there is a strong potential market available to grow in by evaluating user demand, competitive gaps, retention drivers, and monetization/privacy trends.
2. **Outline Minimum Requirements (Self-Contained & No Backend)**:
   - The Android app MUST be 100% self-contained on-device and require NO remote backend or cloud server.
   - All state, persistence, caching, and algorithms must execute locally (e.g. Room SQLite, Jetpack Compose, Material 3, Jetpack Glance widgets, AlarmManager, local JSON/CSV import/export).
   - Outline complete technical and functional minimum requirements (MVP scope, offline data portability, Android SDK compatibility).
3. **Generate Project Codename & Initialize Project Workspace**:
   - Create an evocative project codename (e.g. `habitpulse`, `project-chronos`, `vault-ledger`).
   - Call `startProject(projectName: "<codename>")` to create and activate `./session/projects/<codename>`.
4. **Draft Comprehensive Product Specification (PRD)**:
   - Ensure `doc/spec` exists via `executeSessionCommand`.
   - Author a complete Product Specification directly into `doc/spec/0001-<slug>.md` and `PRODUCT_SPEC.md` detailing Executive Summary, Market Analysis & Growth Potential, Self-Contained Technical Requirements, MoSCoW Scope, User Stories with Given/When/Then criteria, and Jetpack Compose/Material 3 UX Guidelines.
5. **Initiate Software Development Kanban Workflow (Unapproved)**:
   - Call `createCard` to place a card in the **`Software Development`** row under Column 1 (**`Architecture`**) for `@Software Architect`:
     - Tool: `createCard(row: "Software Development", column: "Architecture", title: "[Project Codename] Product Title", prompt: "### Feature Specification Directives\\n\\n- **Project**: {codename}\\n- **PRD Document**: doc/spec/0001-{slug}.md\\n- **Instructions**: Review the specification and produce an Architectural Design Document (ADD) in doc/add/ for the UI Designer and Software Engineer.\\n\\nToggle switch to **Approved** to trigger Software Architect!", approved: false)`
6. **Log Project Brief & Clean Workspace**:
   - Call `storeBriefEntry(category: "project", staffName: "Product Manager", code: "nightly_android_discovery", text: "<summary>")`.
   - Call `stopProject()`.

---

## 4. Software Development Kanban Workflow Initiation

Upon completing a Product Specification in `doc/spec/`:

1. **Initiate Kanban Row Workflow**:
   - Create a card in the `Software Development` Kanban row under Column 1 (`Architecture`) for `@Software Architect`:
     - Tool: `createCard(row: "Software Development", column: "Architecture", title: "{FeatureTitle}", prompt: "### Feature Specification Directives\\n\\n- **Project**: {projectName}\\n- **PRD Document**: doc/spec/{NUMBER}-{slug}.md\\n- **Instructions**: Review the specification and produce an Architectural Design Document (ADD) in doc/add/ for the UI Designer and Software Engineer.\\n\\nToggle switch to **Approved** to trigger Software Architect!", approved: true)`

---

## 5. Critical Execution Rules

1. **Unambiguous Acceptance Criteria**: Every user story must feature testable Given/When/Then criteria.
2. **Strict Scope Control**: Explicitly define what is out-of-scope for the MVP.
3. **Preserve Documentation**: Never overwrite or delete existing specifications or project documentation.
