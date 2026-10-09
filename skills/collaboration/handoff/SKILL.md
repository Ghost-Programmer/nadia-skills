---
name: HandoffSkill
description: Compact the current conversation into a structured handoff document for another agent or session to pick up seamlessly, and open a new chat window with the handoff file attached. Use when transitioning tasks, preserving context across sessions, or when requested to hand off or summarize ongoing work.
tools: [openHandoffChatWindow]
---

# Agent Session Handoff Skill

This skill provides instructions for compacting and summarizing an ongoing conversation or task into a structured handoff document and opening a new chat window with the document attached for a subsequent agent session to continue without loss of context.

---

## 1. Storage Location

- **Save to OS Temporary Directory**: Write the generated handoff document to the user's operating system temporary directory (e.g., `%TEMP%` on Windows, `/tmp` on Linux/macOS or Java `java.io.tmpdir`), **not** directly into the project workspace root.
- **Naming Pattern**: Use `nadia_handoff_<timestamp>.md` (e.g. `nadia_handoff_20260909_123000.md`).

---

## 2. Document Structure

A handoff document must include the following sections:

### 1. Goal & Session Objective

- Clear summary of the user's primary goal and any specific focus area specified for the next session.

### 2. Current State & Completed Work

- High-level overview of decisions made, files modified, and features or tests implemented.
- **Reference existing artifacts**: Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them directly by filepath or URL (e.g., `ADR-0012`, `APP_SPEC.md`, `walkthrough.md`).

### 3. Open Items & Immediate Next Steps

- Exact tasks or decisions pending for the next agent to tackle immediately.
- Known issues, blockers, or edge cases to watch out for.

### 4. Key References & Modified Files

- List of core files, entry points, and test classes relevant to the task.

### 5. Suggested Skills

- Explicit list of procedural skills (from `./skills`) that the incoming agent should activate or review to complete the work (e.g., `AntigravitySkill`, `AskMeSkill`, `ArchitectSkill`, `NetworkSkill`).

---

## 3. Opening the New Chat Window

Once the handoff document is written to the temporary directory:

1. Call the `openHandoffChatWindow` tool:
   - `handoffFilePath`: The path to the newly written handoff markdown file in the temporary directory.
   - `initialPrompt`: A concise orientation message for the next agent session (e.g., `"Attached is the handoff summary from the previous session. Please review the attached document and continue with the next immediate open items."`).
2. The UI will dynamically open a fresh, independent chat window with its own isolated Spring AI session and chat memory, with the handoff document automatically attached and ready for execution.

---

## 4. Redaction & Security Guidelines

- **Zero Credential Leaks**: Never include raw API keys, passwords, secrets, bearer tokens, or sensitive personally identifiable information (PII) in the handoff document.
- Redact or reference environment variables instead (e.g., `${OPENAI_API_KEY}`, `${DB_PASSWORD}`).

---

## 5. Tailoring to User Arguments

If the user passed a specific argument or instruction (e.g., "What will the next session be used for?"), prioritize and tailor the "Immediate Next Steps" and "Suggested Skills" specifically toward that designated objective.
