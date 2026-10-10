---
name: AntigravitySkill
description: Guidelines and command references for delegating complex coding, refactoring, and execution tasks to the Antigravity CLI (agy) under the `./session` sandbox directory.
tools: [executeSessionCommand]
---

# Antigravity CLI Delegation Skill

This skill provides guidelines and instructions for delegating complex coding, refactoring, testing, and general workspace tasks to the Antigravity CLI (`agy`) from within the Nadia workspace context.

All `agy` commands are executed inside the `./session` sandbox directory (or active project folder under `./session/projects/...`) using the `executeSessionCommand` tool.

## Setup Instructions

- **Antigravity CLI Binary**:
  - Install the Antigravity CLI (`agy`) binary and ensure it is available on system `PATH`.
  - Typical installation paths: `~/.antigravity/bin/agy` or `C:\Users\<user>\.gemini\antigravity-ide\bin\agy.cmd`.
- **Permissions & Sandbox**:
  - Ensure execution permissions for running sub-processes via `executeSessionCommand`.
  - Target project sandbox directory `./session/` must exist and be writable.
- **Authentication**:
  - Verify AGY CLI authentication (`agy auth login` or active Google Cloud / DeepMind credentials profile).

---

## Execution Guidelines

1. **Non-Interactive Execution**: Since `executeSessionCommand` executes commands non-interactively and does not support interactive inputs, you **MUST** run the `agy` CLI with the `--add-dir .`, `--print` (or `-p`), `--dangerously-skip-permissions`, and `--mode accept-edits` flags. This ensures the inner Antigravity agent explicitly binds to the current workspace directory, operates in execution mode, auto-approves tool permissions, and writes file modifications directly to workspace project files rather than creating planning artifacts.
2. **Current Directory**: Use the `dir` argument in `executeSessionCommand` to set the active directory to the specific folder under `./session` where you want the command to run. The `agy` CLI will run in this directory context and apply changes there.
3. **Reasoning Effort**: By default, `agy` will run with standard reasoning effort. If a task is highly complex (e.g., debugging a deep logical bug or refactoring key architectural paths), you can pass the `--effort high` flag. For quick or trivial tasks, you can use `--effort low`.
4. **Artifacts & Reports in `./session/brain`**: When asking Antigravity to generate standalone documentation, research reports, or artifacts, explicitly instruct it in the prompt to write the output files into `./session/brain/` (e.g., `./session/brain/<report_name>.md`). Never save or reference `.gemini` paths.

---

## Command Reference

### 1. Basic Single-Shot Prompt Execution

To run a task non-interactively in a directory, use the following pattern (flags MUST precede the prompt argument):

```bash
agy --add-dir . --dangerously-skip-permissions --mode accept-edits -p "[Instruction details]"
```

*Long Form:*

```bash
agy --add-dir . --dangerously-skip-permissions --mode accept-edits --print "[Instruction details]"
```

### 2. Resuming or Continuing Conversations

If you need to perform follow-up tasks in the same context, you can resume the previous session by passing the conversation ID or continuing the most recent conversation:

```bash
agy --dangerously-skip-permissions --conversation "[Conversation ID]" -p "[Follow-up instructions]"
```

```bash
agy --dangerously-skip-permissions --continue -p "[Follow-up instructions]"
```

---

## Common Use Case Examples

### Example 1: Refactoring Code in a Project Subfolder

Delegate the task of refactoring a file to improve logging or clean up design patterns in a specific sub-project.

* **Tool Call**: `executeSessionCommand`
* **Arguments**:
  * `command`: `agy --dangerously-skip-permissions -p "Refactor DBConnector.java to add robust error logging and close connections properly"`
  * `dir`: `my-app/src/main/java`

### Example 2: Writing and Running Tests

Instruct the CLI agent to write automated unit tests and verify they pass using local test runners.

* **Tool Call**: `executeSessionCommand`
* **Arguments**:
  * `command`: `agy --dangerously-skip-permissions -p "Write unit tests for auth.py and verify them by running pytest"`
  * `dir`: `python-auth-service`

### Example 3: Debugging and Fixing Build Failures

Delegate the analysis and fixing of a compilation or build failure.

* **Tool Call**: `executeSessionCommand`
* **Arguments**:
  * `command`: `agy --dangerously-skip-permissions -p "Run npm run build, identify the cause of any TypeScript compilation errors, and fix them"`
  * `dir`: `frontend-dashboard`
