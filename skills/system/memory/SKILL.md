---
name: MemorySkill
description: Guidelines and instructions for creating, retrieving, updating, and deleting structured knowledge, facts, project context, and long-term preferences in Nadia's vector RAG database.
tools: [saveMemory, searchMemory, getMemoryById, updateMemory, deleteMemory, listMemories]
---

# RAG Knowledge & Memory Management Skill

This skill guides the agent in managing enduring knowledge, project rules, user preferences, technical constraints, and domain facts stored within Nadia's vector RAG knowledge base.

---

## 1. Core Capabilities & Operations

The `MemoryTool` provides full CRUD access to the persistent vector store:

| Operation | Tool | Purpose |
| :--- | :--- | :--- |
| **Create** | `saveMemory(content, category, tags, userId)` | Stores a new fact or knowledge piece with metadata and returns a unique memory ID. |
| **Retrieve** | `searchMemory(query, topK, category, userId)` | Performs semantic vector similarity search against stored knowledge. |
| **Get by ID** | `getMemoryById(id)` | Retrieves the exact content and metadata for a specific memory ID. |
| **Update** | `updateMemory(id, content, category, tags)` | Replaces the content and updates metadata (timestamps, version) for an existing memory ID. |
| **Delete** | `deleteMemory(id)` | Permanently removes a knowledge piece from the vector store by ID. |
| **List** | `listMemories(category, limit)` | Recalls top memories, optionally filtered by a specific category. |

---

## 2. When to Store Knowledge (`saveMemory`)

Always store a new memory when:

1. **User Preferences**: The user expresses a durable preference (e.g., *"I prefer Gradle over Maven"*, *"Always write tests using JUnit 5"*).
2. **Project Architecture & Decisions**: Key technical architecture choices, port configurations, database endpoints, or coding rules are decided.
3. **Domain & Business Rules**: Workflow guidelines, API keys, credentials aliases, or operational rules.

### Standard Categories & Tags

Use lowercase category identifiers:

- `user_preference`: User-specific stylistic, build, or tooling preferences.
- `project_context`: Repository architecture, directory conventions, build commands.
- `technical_decision`: Specific framework versions, database dialects, architectural choices.
- `system_rule`: Behavioral constraints, prompt safety guidelines, scheduling rules.
- `general`: General enduring facts and domain notes.

*Example Tool Call:*

```json
{
  "function": "saveMemory",
  "parameters": {
    "content": "User prefers Gradle with Kotlin DSL and Java 23 for all new Spring Boot modules.",
    "category": "user_preference",
    "tags": "gradle, java23, spring-boot, build",
    "userId": "default"
  }
}
```

---

## 3. When to Recall Knowledge (`searchMemory`)

Before answering complex domain questions or performing modifications:

1. Formulate a targeted semantic query capturing the core concept.
2. Call `searchMemory` with `topK` (typically 3 to 10) and optional category filter.
3. Incorporate recalled facts into your reasoning and plan.

*Example Tool Call:*

```json
{
  "function": "searchMemory",
  "parameters": {
    "query": "build system preference java version",
    "category": "user_preference",
    "topK": 5
  }
}
```

---

## 4. Updating & Deleting Knowledge (`updateMemory` / `deleteMemory`)

1. **Evolving Knowledge**: When a user changes an established preference (e.g., *"We switched from SQLite to PostgreSQL"*), search for the existing memory to find its ID, then call `updateMemory` to replace the outdated fact.
2. **Obsolete or Incorrect Data**: If a fact is invalid or deleted, call `deleteMemory` using its memory ID.

> [!IMPORTANT]
> **Sequential Step Rule**: Do NOT call `searchMemory` and `deleteMemory` / `updateMemory` in the same heartbeat step. First retrieve the memory to obtain its valid ID in step 1, then execute the modification or deletion in step 2.

---

## 5. Output Presentation Template

When presenting recalled or managed memories to the user, format them clearly in Markdown:

```markdown
### 🧠 RAG Knowledge Recall: [Category / Query]

- **[mem_a1b2c3d4]** `[user_preference]` *Tags: gradle, java23*
  > User prefers Gradle with Kotlin DSL and Java 23 for all new Spring Boot modules.
  *(Updated: 2026-09-02T09:20:00Z)*
```
