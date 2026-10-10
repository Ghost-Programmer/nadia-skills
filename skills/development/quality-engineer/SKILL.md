---
name: QualityEngineerSkill
description: Guidelines and workflows for test plan authoring (doc/test/ or TEST_PLAN.md), automated test suite execution across Android, JavaFX, Angular, and Java/Spring, defect tracking, Kanban triage, and code quality verification.
tools: [startProject, listProjects, executeSessionCommand, dockerListContainers, dockerContainerLogs, dockerCheckContainers, storeBriefEntry, appendBriefEntry, getBriefEntries, searchMemory, saveMemory, updateMemory, getCurrentDateTime, getKanbanBoard, createKanbanCard, updateKanbanCard, moveKanbanCard]
---

# Quality Engineering & Test Automation Skill

This skill guides agents in creating comprehensive **Test Plans** in `doc/test/` or `TEST_PLAN.md`, generating automated test suites, running test executions across **Android**, **JavaFX**, **Angular**, and **Java / Spring Boot** within project sandboxes, diagnosing test failures, and managing bug triage.

## Setup Instructions

- **Build Tools & Runtimes**:
  - JDK 21+ / 23+ configured on system `PATH` with `JAVA_HOME` set.
  - Gradle (`./gradlew` / `gradlew.bat`) or Maven (`mvn`) available in project repositories.
  - Node.js 18+ and npm installed for Angular/web projects.
  - Android SDK (or `android` CLI plugin) configured if running Android instrumented/unit tests.
- **Docker & Testcontainers (Optional)**:
  - Docker Desktop / Engine running for Testcontainers integration tests.
- **Project Sandbox**:
  - Sandbox directory `./session/projects/` writable for test reports in `doc/test/` and `build/reports/`.

---

## 1. Test Planning & Execution Pipeline

When validating features, running regression suites, or auditing code quality:

1. **Activate Project Context**:
   - Call `startProject` with `{"projectName": "<projectName>"}`.
2. **Author Comprehensive Test Plan**:
   - Ensure `doc/test/` exists:
     - `python -c "import os; os.makedirs('doc/test', exist_ok=True)"`
   - Determine sequential test plan number (`doc/test/0001-test-plan.md` or `TEST_PLAN.md`).
   - Define: Scope, Unit Test Matrix, Integration Matrix, UI/E2E Scenarios, Edge Cases, and Quality Gates.
3. **Scaffold & Generate Automated Test Suites via Antigravity (`agy`)**:
   - Run `executeSessionCommand`:
     ```json
     {
       "command": "agy --add-dir . --dangerously-skip-permissions --mode accept-edits --effort high -p \"Generate automated tests for '<FEATURE_OR_MODULE>'. Implement unit, integration, and UI test cases with thorough assertions covering happy paths and failure edge cases.\"",
       "dir": "."
     }
     ```
4. **Execute Tests via Sandboxed CLI**:
   - Java/Spring: `gradlew test` or `mvn test`
   - Android: `gradlew testDebugUnitTest`
   - Angular: `npm test -- --watch=false --browsers=ChromeHeadless` or `npx playwright test`
5. **Analyze Results & Defect Triage**:
   - If tests fail: Capture stack traces, formulate reproduction steps, log bug cards on Kanban via `createKanbanCard`, and tag `@Software Engineer`.
   - If tests pass: Log verification brief via `storeBriefEntry` (category: `qa`) and advance Kanban cards to `Done`.

---

## 2. Multi-Platform Testing Strategies

### 1. Android Testing (JUnit, MockK, Robolectric, Espresso)
- Test ViewModels and business logic with JUnit 5 / MockK.
- Test Jetpack Compose UI with `createComposeRule()` verifying UI state assertions and click events.
- Test Room database queries using in-memory Room SQLite databases.

### 2. JavaFX Testing (TestFX, JUnit 5, Monocle)
- Automate UI interactions (click, type, drag) with TestFX `FxRobot`.
- Test controllers and property bindings with JUnit 5 assertions.
- Run headless UI tests in CI environments using TestFX Monocle.

### 3. Angular Testing (Jasmine, Jest, Playwright, Cypress)
- Write isolated component unit tests using `TestBed`.
- Mock HTTP service calls using `HttpClientTestingModule` / `HttpTestingController`.
- Execute automated end-to-end user journeys using Playwright.

### 4. Java & Spring Testing (JUnit 5, MockMvc, Testcontainers)
- Use `@WebMvcTest` and `MockMvc` for controller testing.
- Use `@SpringBootTest` with Testcontainers for real database/service integration tests.
- Verify contract and edge cases with AssertJ (`assertThat(...)`).

---

## 3. Software Development Kanban Workflow (Column 4: Quality)

When executing an approved card in the `Software Development` Kanban swimlane under `Quality`:

1. **Ingest Requirements & Source Code**: Ingest specifications, ADD documents, and source files under `src/`.
2. **Execute Automated Tests**: Run test suites via `executeSessionCommand` (`gradlew test`, `mvn test`, or `npm test`).
3. **Evaluate Test Results & Route Downstream**:
   - **If Bugs Found**: Submit a defect card back to Column 3 (`Software Development`) for `@Software Engineer`:
     - Tool: `createCard(row: "Software Development", column: "Software Development", title: "Bug: <BugTitle>", prompt: "### Defect Report\n\n- **Project**: `<projectName>`\n- **Failing Tests**: <names>\n- **Error / Stacktrace**: <trace>\n- **Reproduction**: <steps>\n\nToggle switch to **Approved** to trigger Software Engineer to fix!", approved: true)`
   - **If All Tests Pass**: Create a card in Column 5 (`Complete`):
     - Tool: `createCard(row: "Software Development", column: "Complete", title: "Complete: <FeatureTitle>", prompt: "### Feature Complete & Quality Verified\n\n- **Project**: `<projectName>`\n- **Test Status**: PASSED (All tests green)\n- **Verification Summary**: Code and software verified against all specifications.\n\nTask is fully complete!", approved: true)`

---

## 4. Critical Execution Rules

1. **Empirical Execution**: Always execute real test suites; never report test results without running them.
2. **Defect Detail**: Always include reproduction steps, input data, and stack traces when logging defects.
3. **Preserve Documentation Trees**: Never delete existing test files or documentation folders.

