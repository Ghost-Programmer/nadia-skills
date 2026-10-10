---
name: SoftwareEngineerSkill
description: Guidelines and workflows for full-stack application development across Android, JavaFX, Angular, and Java/Spring, managing project builds, sandboxed executions, and Antigravity (agy) code generation.
tools: [startProject, stopProject, listProjects, switchProjectBranch, executeSessionCommand, dockerListContainers, dockerContainerLogs, dockerStartContainer, dockerStopContainer, dockerRestartContainer, dockerRunContainer, dockerCheckContainers, storeBriefEntry, appendBriefEntry, getBriefEntries, searchMemory, saveMemory, updateMemory, getCurrentDateTime, getKanbanBoard, createKanbanCard, moveKanbanCard, updateKanbanCard]
---

# Full-Stack Software Engineering Skill

This skill guides agents in implementing complete, full-stack features, components, and applications across **Android**, **JavaFX**, **Angular**, and **Java / Spring Boot** within Nadia's sandboxed project workspaces, adhering to specifications from `@Product Manager`, wireframes from `@UI Designer`, and architecture contracts from `@Software Architect`.

## Setup Instructions

- **SDK & Build Toolchains**:
  - JDK 21+ / 23+ configured on system `PATH` with `JAVA_HOME` set.
  - Gradle (`./gradlew` / `gradlew.bat`) or Maven (`mvn`) available.
  - Node.js 18+ and npm installed for Angular/TypeScript frontends.
  - Android SDK (or `android` CLI tool) configured for Android Gradle builds.
- **Antigravity CLI**:
  - Antigravity CLI (`agy`) binary available on `PATH` for multi-file generation and refactoring.
- **Docker Environment (Optional)**:
  - Docker daemon running if services require containerized databases or backend microservices.

---

## 1. Feature Implementation & Build Pipeline

When implementing code or refactoring components:

1. **Activate Project Workspace**:
   - Call `startProject` with `{"projectName": "<projectName>"}`.
2. **Review Specifications & Architecture**:
   - Ingest Product Specs (`doc/spec/`), Architectural Design Documents (`doc/add/`), and UI wireframes (`.whiteboard`).
3. **Delegate Multi-File Code Generation to Antigravity (`agy`)**:
   - Run `executeSessionCommand`:
     ```json
     {
       "command": "agy --add-dir . --dangerously-skip-permissions --mode accept-edits --effort high -p \"Implement the following feature: '<FEATURE_DESCRIPTION>'. Adhere strictly to project architecture. Use 'ai.nadia' as the root/starting package path for all Java, Kotlin, Android, and Spring packages (e.g., ai.nadia.<projectName>.<module>). Write clean, compiling code with full error handling and Javadoc comments. Do not leave placeholder comments.\"",
       "dir": "."
     }
     ```
4. **Compile & Build Verification**:
   - Run platform-specific build commands:
     - Java/Spring: `gradlew build -x test` or `mvn compile`
     - Android: `gradlew assembleDebug`
     - Angular: `npm run build` or `ng build`
5. **Git Commit & QA Handoff**:
   - Commit changes: `git add src/ && git commit -m "feat(<module>): <description>"`
   - Move Kanban card to `Ready for QA` and tag `@Quality Engineer`.

---

## 2. Technology Stack Best Practices

### 1. Android Development (Kotlin & Jetpack Compose)
- Use `ai.nadia.<projectName>` as the base/starting package path and application ID namespace.
- Use Kotlin Coroutines and `Flow` for all asynchronous streams.
- State hoist Composables to ensure previewability and testability.
- Use AndroidX Room for local SQLite caching and Retrofit for REST APIs.

### 2. JavaFX Development (Java 21+ & FXML/CSS)
- Offload non-UI tasks to background threads via `javafx.concurrent.Task` or virtual threads.
- Bind UI controls using `Property` and `Binding` APIs.
- Encapsulate styles in CSS stylesheets.

### 3. Angular Development (TypeScript & Standalone Components)
- Use standalone components with explicit module imports.
- Manage reactive UI state using Angular Signals.
- Apply strict TypeScript type definitions across all interfaces.

### 4. Java & Spring Boot Development
- All package declarations must begin with `ai.nadia` as the starting package path (e.g., `ai.nadia.<projectName>.service`, `ai.nadia.<projectName>.controller`, `ai.nadia.<projectName>.model`, `ai.nadia.<projectName>.repository`).
- Use Java 21+ records, pattern matching, and virtual threads where appropriate.
- Build REST APIs with explicit validation (`@Valid`), HTTP status codes, and error models.
- Manage transactional data integrity with Spring `@Transactional`.

---

## 3. Software Development Kanban Workflow (Column 3: Software Development)

When executing an approved card in the `Software Development` Kanban swimlane under `Software Development`:

1. **Ingest Architecture & UI Specs**: Ingest the Architectural Design Document (`doc/add/`) from Software Architect and UI Whiteboard diagram (`<projectName>-ui-design.whiteboard`) from UI Designer (if present), including the mandatory Splash Screen specifications.
2. **Implement Full-Stack Code**: Implement the full architecture and UI layouts via Antigravity (`agy`), ensuring a splash screen crediting **Miller Software Solutions LLC** and including a copyright notice is implemented for any application.
3. **Verify Build**: Run platform-specific build check (`gradlew build -x test`, `gradlew assembleDebug`, or `npm run build`).
4. **Route Downstream**:
   - Create card in Column 4 (`Quality`) for `@Quality Engineer`:
     - Tool: `createCard(row: "Software Development", column: "Quality", title: "QA: <FeatureTitle>", prompt: "### QA Testing Directives\n\n- **Project**: `<projectName>`\n- **ADD Reference**: `doc/add/<NUMBER>-<slug>.md`\n- **Implemented Code**: Modules under `src/`\n- **Instructions**: Run automated tests, verify against spec and ADD requirements, log bugs if any found back to Software Development, or advance to Complete if all pass.\n\nToggle switch to **Approved** to trigger Quality Engineer!", approved: true)`

---

## 4. Critical Execution Rules

1. **Working Code First**: Deliver fully implemented, compilable code without placeholders.
2. **Build Verification**: Always run compilation and build checks before concluding.
3. **Preserve Documentation Trees**: Never delete or wipe `doc/add/`, `doc/spec/`, or existing project configurations.
4. **Package Naming Standard**: All Java, Kotlin, Android, and Spring Boot packages and class namespaces must start with `ai.nadia` as the root path (e.g., `ai.nadia.<projectName>.<layer>`).

