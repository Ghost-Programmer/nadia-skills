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
tools: []
---

# Procedural Skill Creation Guide (agentskills.io Open Standard)

This skill guides the agent in authoring, structuring, validating, and packaging procedural skills (`SKILL.md`) compliant with the open **agentskills.io** standard for the Nadia cognitive architecture.

## Setup Instructions

- **Prerequisites**: Target skills directory `./skills/` (or `~/.nadia/skills/`) exists and has write permissions.
- **Open Standard Compliance**: Every skill authored or exported by Nadia follows the [agentskills.io](https://agentskills.io) specification so community-built skills can be imported directly and agent-generated skills can be shared across compatible platforms.
- **Skill Reloading**: After writing or modifying a `SKILL.md`, call `SkillRegistry.reloadSkills()` or save in the Skill Editor to re-index active skills.

---

## 1. Skill Directory Architecture & Progressive Disclosure (`agentskills.io`)

Skills are stored in self-contained directories under `~/.nadia/skills/<category>/<skill-name>/` (or flat `<skill-name>/` when packaged for sharing):

```text
<skill-name>/
├── SKILL.md       # Required: YAML frontmatter + procedural Markdown instructions
├── scripts/       # Optional: Deterministic executable scripts (Python, Bash, JS)
├── references/    # Optional: Deep-dive reference docs loaded on demand
└── assets/        # Optional: Static templates, schemas, or boilerplate files
```

- **Directory & `name` Matching**: The directory name and the frontmatter `name` field MUST use lowercase alphanumeric characters and single hyphens (`a-z`, `0-9`, `-`), 1–64 characters, with no leading, trailing, or consecutive hyphens (e.g. `create-a-skill`, `clean-writing`, `web-research`).

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

## 3. Standard `agentskills.io` Skill Template

```markdown
---
name: example-skill
description: Clear, actionable description of what this skill does and specific trigger conditions when the agent should use it.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: general
  display-name: ExampleSkill
allowed-tools: toolName1 toolName2
tools: [toolName1, toolName2]
---

# Example Skill Title

Overview of the cognitive skill's purpose and scope.

---

## 1. Workflow & Execution Steps

1. **Step 1 Name**: Detailed instructions on what to analyze or evaluate.
2. **Step 2 Name**: Guidelines on calling tools or executing bundled scripts in `scripts/`.
3. **Step 3 Name**: How to formulate the final result or update state.

---

## 2. Tool & Script Reference

- **`toolName1`**: When and how to call this tool.
  - Parameters: `param1`, `param2`
  - Example payload:
    ```json
    {
      "param1": "value",
      "param2": 123
    }
    ```

---

## 3. Safety, Edge Cases & Completion Criteria

- Guardrails and redaction rules.
- What to do on failure or missing prerequisites.
- Definition of done: when the workflow terminates.
```

---

## 4. Chat Presentation & Community Sharing Protocol

When the user asks to create, draft, or design a new skill:

1. **Display Complete Markdown in Chat**: Always present the full, production-ready `SKILL.md` content inside a formatted markdown code block (` ```markdown ... ``` `) directly in your chat response.
2. **Enforce `agentskills.io` Compliance**: Ensure `name` is lowercase kebab-case (`^[a-z0-9]+(-[a-z0-9]+)*$`), `description` clearly states what and when, and `license`, `compatibility`, `metadata`, and `allowed-tools` / `tools` are properly populated.
3. **Interactive Save & Export**: Inform the user they can save the skill to `~/.nadia/skills/<category>/<skill-name>/SKILL.md` or click **📦 Share / Export (.zip)** in the Nadia Skill Editor to package the skill (including any `scripts/`, `references/`, and `assets/`) as a standard `agentskills.io` archive.
