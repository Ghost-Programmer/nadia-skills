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

