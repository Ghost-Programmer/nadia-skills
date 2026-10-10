---
name: ArchitectSkill
description: Guidelines and instructions for sending ideas and architectural proposals to the Software Architect, creating Architectural Design Documents (ADDs) with status Proposed in doc/add/ via Antigravity (agy), fully designing technical architectures, preserving project documentation, and managing Git/GitHub private repository synchronization.
tools: [startProject, stopProject, listProjects, cloneRepository, generateDiagram, renderMermaidDiagram, getWhiteboardDiagramState, executeSessionCommand, storeBriefEntry, getBriefEntries, getCurrentDateTime, searchMemory, saveMemory, dockerListContainers, dockerContainerLogs, dockerStartContainer, dockerStopContainer, dockerRestartContainer, dockerRemoveContainer, dockerListImages, dockerInspectContainer, dockerRunContainer, dockerCheckContainers]
---

# Software Architecture & ADD Design Skill

This skill guides agents in translating technical ideas, system requirements, and feature proposals into formal, fully designed **Architectural Design Documents (ADDs)** stored in `doc/add/` with status `Proposed`, onboarding remote GitHub repositories into isolated project workspaces, and generating rich, interactive Nadia `.whiteboard` architectural diagrams via **Antigravity (`agy`)**, strictly preserving all existing project files and directories.

## Setup Instructions

- **Git & GitHub CLI**:
  - Git installed and on system `PATH`.
  - GitHub CLI (`gh`) installed and authenticated (`gh auth status` / `GH_TOKEN`) for private repository creation.
- **Antigravity CLI**:
  - Antigravity CLI (`agy`) installed and accessible on `PATH`.
- **Project Sandbox & Permissions**:
  - Project sandbox directory `./session/projects/` writable.
  - Sub-process execution permissions enabled for `executeSessionCommand`.
- **Whiteboard & Kanban Tools**:
  - `startProject`, `cloneRepository`, `storeBriefEntry`, and Whiteboard tools registered in `ToolRegistry`.

---

## 1. Triggering the Architectural Design Document (ADD) Workflow

When a user provides an architectural idea, design proposal, or system requirement, execute the following 7 steps in sequence:

1. **Activate Project Context**:
   - Determine the target project name from the user's prompt (or use the currently active project).
   - Call `startProject` with parameters `{"projectName": "<projectName>"}` to switch the sandbox execution root to `./session/projects/<projectName>`.
   - **DO NOT delete or reset the project folder or any existing project files.**

2. **Verify Git & Private GitHub Repository**:
   - Verify if Git is initialized in the project directory using `executeSessionCommand`:
     - Tool: `executeSessionCommand`
     - Parameters: `{"command": "git status", "dir": "."}`
     - *(If not inside a git repository, run `{"command": "git init -b main", "dir": "."}`)*

   - Check if a remote GitHub origin exists:
     - Tool: `executeSessionCommand`
     - Parameters: `{"command": "git remote -v", "dir": "."}`

   - If no remote repository exists, create a **private** GitHub repository for the project and link it:
     - Tool: `executeSessionCommand`
     - Parameters: `{"command": "gh repo create <projectName> --private --source=. --remote=origin", "dir": "."}`

   - **DO NOT run `git clean` or `git reset --hard` which could destroy local untracked files or directories.**

3. **Ensure `doc/add` Directory Exists**:
   - Verify and create `doc/add` using Windows CMD / cross-platform Python without deleting existing contents:
     - Tool: `executeSessionCommand`
     - Parameters: `{"command": "if not exist doc\\add mkdir doc\\add", "dir": "."}`
     - *or:* `{"command": "python -c \"import os; os.makedirs('doc/add', exist_ok=True)\"", "dir": "."}`
   - **STRICT RULE**: Never delete, wipe, or recreate the `doc/add` directory.

4. **Determine Next ADD Number**:
   - Inspect existing files in `doc/add/` to find the next sequential 4-digit number:
     - Tool: `executeSessionCommand`
     - Parameters: `{"command": "python -c \"import os, glob; files = sorted(glob.glob('doc/add/[0-9]*.md')); print(f'{len(files)+1:04d}')\"", "dir": "."}`
   - Always preserve all existing ADD files.

5. **Generate ADD File Using Antigravity (`agy`) — MANDATORY TOOL CALL**:
   - **Delegate the architectural reasoning, design elaboration, and file creation to Antigravity (`agy`)** via `executeSessionCommand`:
     - Tool: `executeSessionCommand`
     - Parameters:
       ```json
       {
         "command": "agy --add-dir . --dangerously-skip-permissions --mode accept-edits --effort high -p \"Generate a comprehensive Architectural Design Document (ADD) file for the following proposal: '<IDEA_OR_REQUIREMENTS>'. 1. Check existing ADDs in doc/add/ to ensure consecutive 4-digit numbering (e.g., doc/add/0001-..., doc/add/0002-...). Do NOT overwrite or delete existing ADD files. 2. The ADD Status MUST be 'Proposed'. 3. Follow standard ADD sections: # ADD <NUMBER>: <Title>, ## Status, ## Context, ## Design. 4. Fully flesh out the technical design, system components, API/interface contracts, data models, communication patterns, security considerations, and trade-offs without placeholders. All Java, Kotlin, Android, and Spring package structures must use 'ai.nadia' as the root/starting package path (e.g., ai.nadia.<projectName>.<module>). 5. Write the final markdown file directly into doc/add/<NUMBER>-<kebab-case-title>.md in the current project directory using write_to_file. Do NOT delete or modify existing files in doc/add/.\"",
         "dir": "."
       }
       ```
   - **STRICT REQUIREMENT**: Do NOT generate or write the ADD file yourself. You **MUST** call `executeSessionCommand` with the `agy` CLI command. Antigravity will analyze the codebase, check existing ADDs in `doc/add/`, formulate the full technical architecture with `Status: Proposed`, and write the markdown file to `doc/add/<NUMBER>-<slug>.md` directly in the project directory.

6. **Verify, Commit, and Push to GitHub**:
   - Stage the newly created ADD document in git:
     - Tool: `executeSessionCommand`
     - Parameters: `{"command": "git add doc/add/", "dir": "."}`
   - Commit with a descriptive conventional commit message:
     - Tool: `executeSessionCommand`
     - Parameters: `{"command": "git commit -m \"docs(add): propose ADD <NUMBER> - <Title>\"", "dir": "."}`
   - Push the commit to the private remote repository:
     - Tool: `executeSessionCommand`
     - Parameters: `{"command": "git push -u origin main", "dir": "."}`

7. **Store TODO Brief & Present**:
   - Call `storeBriefEntry` to record an actionable TODO entry in the system brief store:
     - Tool: `storeBriefEntry`
     - Parameters:
       ```json
       {
         "category": "todo",
         "text": "- [ ] **Review and approve ADD `[NUMBER]`: `[Title]`** (Project: `[projectName]`, File: `doc/add/[NUMBER]-[slug].md`, Status: `Proposed`)",
         "staffName": "Software Architect",
         "code": "add_todo_[NUMBER]"
       }
       ```
   - Deliver the full ADD text and Git push confirmation to the user.

---

## 2. GitHub Repository Ingestion & Whiteboard Generation Workflow

This workflow automatically triggers whenever the user provides a Git or GitHub repository URL (e.g. `@Software Architect analyze https://github.com/owner/my-repo` or even `@Software Architect https://github.com/owner/my-repo`):

1. **Pull Codebase into Project Sandbox**:

   - Call `cloneRepository` with parameters `{"repoUrl": "<url>", "projectName": null}`.
   - The system parses the project name, creates `./session/projects/<projectName>`, clones the repo into `./session/projects/<projectName>/code`, and activates the project sandbox.

2. **Delegate Architecture & Whiteboard Synthesis to Antigravity (`agy`)**:
   - Run `executeSessionCommand`:
     ```json
     {
       "command": "agy --add-dir . --dangerously-skip-permissions --mode accept-edits --effort high -p \"Analyze the codebase located in './code'. 1. Identify architectural tiers (Client/UI, API Gateway, Application/Domain Services, Persistence/Database, External Integrations). 2. Construct a Nadia whiteboard JSON model containing Frames for layers, Cards for services/controllers, Shapes for datastores, and labeled orthogonal Connectors showing relationships. 3. Save the whiteboard model to '<projectName>-architecture.whiteboard' in the project root.\"",
       "dir": "."
     }
     ```

3. **Store Architecture Brief**:
   - Call `storeBriefEntry` with category `architecture` documenting the generated whiteboard file.

4. **Present Results**:
   - Present a structured summary of the architectural layers, primary components, technologies detected, and confirm the whiteboard file is ready on the Whiteboard canvas.

---

## 3. Software Development Kanban Workflow (Column 1: Architecture)

When executing an approved card in the `Software Development` Kanban row under `Architecture`:

1. **Ingest Specification**: Read the requirement specification detailed in the card prompt.
2. **Author ADD**: Run the 7-step ADD generation workflow (Section 1) using Antigravity (`agy`) to produce `doc/add/<NUMBER>-<slug>.md` with `Status: Proposed`.
3. **Route Downstream**:
   - **If UI Design needed**: Call `createCard(row: "Software Development", column: "UI Design", title: "UI Design: <FeatureTitle>", prompt: "### UI Design Directives\n\n- **Project**: `<projectName>`\n- **ADD Reference**: `doc/add/<NUMBER>-<slug>.md`\n- **Requirements**: Outline screens, layouts, design tokens, and interaction flows in `<projectName>-ui-design.whiteboard`, including a mandatory Splash Screen crediting Miller Software Solutions LLC with an official copyright notice.\n\nToggle switch to **Approved** to trigger UI Designer!", approved: true)`.
   - **If Backend/Logic only**: Call `createCard(row: "Software Development", column: "Software Development", title: "Develop: <FeatureTitle>", prompt: "### Implementation Directives\n\n- **Project**: `<projectName>`\n- **ADD Reference**: `doc/add/<NUMBER>-<slug>.md`\n- **Package Standard**: Use `ai.nadia` as root package path (e.g. `ai.nadia.<projectName>.<module>`)\n- **Requirements**: Implement full-stack services and models adhering to the ADD specification.\n\nToggle switch to **Approved** to trigger Software Engineer!", approved: true)`.

---

## 4. Critical Execution Rules

1. **MANDATORY ANTIGRAVITY DELEGATION**: Creation of ADD specifications and `.whiteboard` models MUST always be delegated to Antigravity (`agy`) via `executeSessionCommand`.
2. **NO Conversational Filler**: Immediately execute the required tool calls without asking for permission or explaining what you are about to do.
3. **STRICT PRESERVATION OF `doc/add`**: Under NO circumstances should you delete, remove, clean, or wipe `doc/add` or existing `.md` files.
4. **Status Always Proposed**: When creating new architectural ideas/proposals, the status must strictly be `Proposed`.
5. **Private Repositories**: Always use `--private` when creating GitHub repositories.
6. **Package Naming Standard**: All Java, Kotlin, Android, and Spring Boot package namespaces and module structures must use `ai.nadia` as the starting package path (e.g., `ai.nadia.<projectName>.*`).


