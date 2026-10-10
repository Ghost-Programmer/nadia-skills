---
name: CreateSkillSkill
description: Guidelines, template, and procedural instructions for authoring and adding new procedural skills to the Nadia cognitive agent system.
tools: []
---

# Procedural Skill Creation Guide

This skill guides the agent in authoring, structuring, and formatting new procedural skills (`SKILL.md`) for the Nadia cognitive architecture.

## Setup Instructions

- **Prerequisites**: Target skills directory `./skills/` (or `~/.nadia/skills/`) exists and has write permissions.
- **Skill Reloading**: After writing or modifying a `SKILL.md`, call `SkillRegistry.reloadSkills()` or restart the session to register newly created procedural skills.
- **Validation**: Ensure YAML frontmatter is valid and separated by triple hyphens (`---`).

---

## 1. Skill Architecture & File Layout

All procedural skills are stored under the `./skills/` root directory:

```
./skills/
  └── <skill-name-kebab-case>/
        └── SKILL.md
```

- **Folder Naming**: Use lowercase kebab-case naming (e.g. `data-sync`, `cloud-deploy`, `code-review`).
- **File Name**: `SKILL.md` (or `skill.md`).

---

## 2. Skill Document Structure

Every `SKILL.md` file consists of two mandatory sections separated by standard YAML frontmatter delimiters:

### Section A: YAML Frontmatter
Delimited by triple hyphens (`---`):

- **`name`**: PascalCase identifier for the skill (e.g. `CodeReviewSkill`, `DatabaseMigrationSkill`).
- **`description`**: A concise, descriptive summary explaining what the skill does and when the agent orchestrator should load/activate it. Include relevant trigger keywords.
- **`tools`**: A JSON/YAML list of tool function names that this skill utilizes (e.g. `[storeBriefEntry, executeSessionCommand]`, or `[]` if purely instruction-based).

### Section B: Markdown Body
The system prompt instructions loaded by the Prologue handler when the skill is active:

- **# Title & Objective**: High-level purpose of the capability.
- **## Execution Guidelines & Workflow**: Ordered phases, decision trees, or step-by-step operational steps.
- **## Tool Usage & Parameter Reference**: Exact tool invocation examples and required arguments.
- **## Safety, Error Handling & Completion Rules**: Guardrails, redaction, and success criteria.

---

## 3. Skill Template

```markdown
---
name: ExampleSkill
description: Clear, actionable description of capabilities and specific trigger conditions.
tools: [toolName1, toolName2]
---

# Example Skill Title

Overview of the cognitive skill's purpose and scope.

---

## 1. Workflow & Execution Steps

1. **Step 1 Name**: Detailed instructions on what to analyze or evaluate.
2. **Step 2 Name**: Guidelines on calling tools and inspecting output.
3. **Step 3 Name**: How to formulate the final result or update state.

---

## 2. Tool Reference & Usage Guidelines

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

## 4. Chat Presentation Protocol

When the user asks to create, draft, or design a new skill:

1. **Display Complete Markdown in Chat**: Always present the full, production-ready `SKILL.md` content inside a formatted markdown code block (` ```markdown ... ``` `) directly in your chat response.
2. **Interactive Save Capability**: Inform the user they can copy the content, double-click the message bubble to open the detail viewer and click **Save As**, or instruct you to write it directly into `./skills/<skill-name>/SKILL.md`.
3. **Verify Compliance**: Ensure the generated skill contains valid YAML frontmatter, non-empty name/description, and structured markdown instructions.
