---
name: create-a-skill
description: Guidelines, template, and procedural instructions for authoring, packaging, importing, and sharing procedural skills compliant with the open agentskills.io standard in the Nadia cognitive agent system.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: development
  display-name: CreateSkillSkill
allowed-tools: executeSessionCommand
tools: [executeSessionCommand]
---

# Procedural Skill Creation Guide (`agentskills.io` Open Standard)

This skill guides the agent in authoring, structuring, validating, and packaging procedural skills (`SKILL.md`) compliant with the open **[agentskills.io](https://agentskills.io)** standard for the Nadia cognitive architecture.

## Setup Instructions

- **Prerequisites**: Target skills directory `~/.nadia/skills/` exists and has write permissions.
- **Official Base Template**: A starter template is maintained at [`skills/TEMPLATE.md`](file:///c:/Users/jeff/Source/nadia-skills/skills/TEMPLATE.md) (and `~/.nadia/skills/TEMPLATE.md`).
- **Open Standard Compliance**: Every skill authored or exported by Nadia follows the [agentskills.io](https://agentskills.io) specification so community-built skills can be imported directly and agent-generated skills can be shared across compatible platforms.
- **Skill Reloading**: After writing or modifying a `SKILL.md`, call `SkillRegistry.reloadSkills()` or save in the Skill Editor to re-index active skills.

---

## 1. Skill Directory Architecture & Progressive Disclosure (`agentskills.io`)

Skills are stored in self-contained directories under `~/.nadia/skills/<category>/<skill-name>/` (or flat `<skill-name>/` when packaged as a `.zip` for sharing):

```text
<skill-name>/
├── SKILL.md       # Required: YAML frontmatter + procedural Markdown instructions
├── scripts/       # Optional: Deterministic executable scripts (Python, Bash, JS)
├── references/    # Optional: Deep-dive reference docs loaded on demand
└── assets/        # Optional: Static templates, schemas, or boilerplate files
```

- **Directory & `name` Matching**: The directory name and the frontmatter `name` field MUST use lowercase alphanumeric characters and single hyphens (`^[a-z0-9]+(-[a-z0-9]+)*$`), 1–64 characters, with no leading, trailing, or consecutive hyphens (e.g. `create-a-skill`, `clean-writing`, `web-research`, `flight-tracker`).

---

## 2. `SKILL.md` Frontmatter Specification (`agentskills.io` Standard)

Every `SKILL.md` file begins with YAML frontmatter enclosed in triple hyphens (`---`):

| Field | Required | Specification |
| :--- | :--- | :--- |
| **`name`** | **Yes** | Lowercase kebab-case (`a-z`, `0-9`, `-`), max 64 chars, matching the skill folder name (e.g. `pdf-processing`). |
| **`description`** | **Yes** | Non-empty summary (max 1024 chars) explaining **what** the skill does and **when** the agent should trigger it. |
| **`license`** | Optional | License identifier (e.g., `Apache-2.0`, `MIT`). |
| **`compatibility`** | Optional | Environment or tool requirements (max 500 chars, e.g., required CLI tools, Python packages, or network access). |
| **`metadata`** | Optional | String key-value map for custom attributes (`author`, `version`, `category`, `display-name`). |
| **`allowed-tools`** | Optional | Space-delimited list of pre-approved tools per `agentskills.io` (e.g., `executeSessionCommand storeBriefEntry`). |
| **`tools`** | Optional | YAML array of bound Nadia tool names (e.g., `[executeSessionCommand, storeBriefEntry]`). |

---

## 3. Standard `agentskills.io` Skill Template (`skills/TEMPLATE.md`)

```markdown
---
name: example-skill
description: Concise, actionable summary of what this skill does and the specific trigger conditions when the agent should use it (1-1024 characters).
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: general
  display-name: ExampleSkill
allowed-tools: toolName1 toolName2 executeSessionCommand storeBriefEntry searchMemory saveMemory
tools: [toolName1, toolName2, executeSessionCommand, storeBriefEntry, searchMemory, saveMemory]
---

# Example Skill Title

Provide a concise overview of this procedural skill's purpose, domain scope, and when the cognitive agent or staff specialist should activate it.

---

## 1. Prerequisites & Progressive Disclosure Resources (`agentskills.io`)

- **Required Environment / Tools**: List any required Spring AI `@NadiaTool` bindings, CLI utilities, or environment variables.
- **Bundled Skill Resources (Optional)**:
  - `scripts/`: Deterministic helper scripts (e.g., Python, Bash) executed via `executeSessionCommand`.
  - `references/`: Detailed API schemas or reference documentation loaded on demand.
  - `assets/`: Static templates, configuration files, or boilerplate payloads.

---

## 2. Core Operational Workflows

### 2.1 Primary Execution Workflow

1. **Step 1 - Context & Parameter Validation**:
   - Validate input parameters and query `<episodic_memory>` via `searchMemory` for relevant user preferences or prior state.
2. **Step 2 - Tool / Script Invocation**:
   - Invoke the appropriate registered tool(s) (`toolName1`, `toolName2`) or execute bundled scripts under `scripts/`.
3. **Step 3 - Verification & Persistence**:
   - Verify tool outputs, persist durable facts with `saveMemory` or brief summaries with `storeBriefEntry` when applicable, and present structured Markdown results.

### 2.2 Secondary / Fallback Workflow

1. **Error & Edge-Case Handling**:
   - Detail fallback actions if an external API, hardware device, or network resource is unavailable or unapproved under Zero-Trust policy.

---

## 3. Tool & Script Reference

| Tool / Script | Parameters | Operational Purpose |
| :--- | :--- | :--- |
| `toolName1` | `paramA` (`String`), `paramB` (`int`) | Primary domain operation and expected JSON output. |
| `toolName2` | `id` (`String`) | Secondary inspection or state update action. |
| `scripts/helper.py` | `--input <path> --format json` | Optional bundled CLI helper script invoked via `executeSessionCommand`. |

---

## 4. Safety, Guardrails & Completion Criteria

1. **Tool-Driven Execution**: Always invoke registered tools or bundled scripts rather than fabricating outputs.
2. **Zero-Trust & Sandbox Compliance**: Respect workspace boundaries and zero-trust network authorization checks.
3. **Definition of Done**: The workflow completes once all requested actions are verified and a clean Markdown summary is returned.
```

---

## 4. Chat Presentation & Community Sharing Protocol

When the user asks to create, draft, or design a new skill:

1. **Display Complete Markdown in Chat**: Always present the full, production-ready `SKILL.md` content inside a formatted markdown code block (` ```markdown ... ``` `) directly in your chat response.
2. **Enforce `agentskills.io` Compliance**: Ensure `name` is lowercase kebab-case (`^[a-z0-9]+(-[a-z0-9]+)*$`), `description` clearly states what and when, and `license`, `compatibility`, `metadata`, and `allowed-tools` / `tools` are properly populated.
3. **Interactive Save & Export**: Inform the user they can save the skill to `~/.nadia/skills/<category>/<skill-name>/SKILL.md` or click **📦 Share / Export (.zip)** in the Nadia Skill Editor to package the skill (including any `scripts/`, `references/`, and `assets/`) as a standard `agentskills.io` archive.
