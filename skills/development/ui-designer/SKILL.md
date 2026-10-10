---
name: UIDesignerSkill
description: Guidelines and workflows for synthesizing modern User Interfaces for Android, JavaFX, and Angular, creating interactive Whiteboard (.whiteboard) wireframe models, Mermaid screen transition diagrams, and establishing multi-platform design tokens.
tools: [generateDiagram, renderMermaidDiagram, getWhiteboardDiagramState, clusterWhiteboardNodes, createSpikeBranch, startProject, listProjects, executeSessionCommand, storeBriefEntry, appendBriefEntry, getBriefEntries, searchMemory, saveMemory, updateMemory, getCurrentDateTime, getKanbanBoard, createKanbanCard, updateKanbanCard]
---

# UI/UX Design & Whiteboard Wireframing Skill

This skill guides agents in translating product specifications and user requirements into state-of-the-art **User Interface designs** across **Android**, **JavaFX**, and **Angular**, using Nadia's interactive **Whiteboard** (`.whiteboard`) and diagramming tools to generate visual wireframes, component layouts, screen flow mockups, design tokens, and state transition maps.

## Setup Instructions

- **Whiteboard & Diagram Tools**:
  - `generateDiagram`, `renderMermaidDiagram`, `getWhiteboardDiagramState`, and `clusterWhiteboardNodes` registered in `ToolRegistry`.
  - JavaFX Whiteboard canvas enabled in the Nadia UI.
- **Antigravity CLI**:
  - Antigravity CLI (`agy`) binary installed on `PATH` for programmatic `.whiteboard` JSON wireframe model generation.
- **Project Sandbox**:
  - Active project sandbox directory `./session/projects/<projectName>/` writable for `<projectName>-ui-design.whiteboard` files.

---

## 1. Interactive Whiteboard Wireframing Workflow

When designing UI layouts for an application or feature:

1. **Activate Project Context**:
   - Call `startProject` with the active `projectName`.
2. **Deconstruct Screen & View Hierarchy**:
   - Identify all primary screens, starting with the **mandatory Splash Screen** (e.g. Splash Screen, Overview Dashboard, Detail View, Filter Drawer, Modal Dialog).
   - Ensure the Splash Screen is explicitly specified with prominent attribution to **Miller Software Solutions LLC** and an official **copyright notice**.
   - Identify component building blocks (cards, buttons, data tables, list views, input bars).
3. **Generate Interactive `.whiteboard` Model via Antigravity (`agy`)**:
   - Call `executeSessionCommand`:
     ```json
     {
       "command": "agy --add-dir . --dangerously-skip-permissions --mode accept-edits --effort high -p \"Construct an interactive Nadia UI Whiteboard model for '<PROJECT_OR_FEATURE>'. 1. Build a valid Whiteboard JSON object with 'id', 'name', 'createdAt', 'updatedAt', 'viewport', 'elements', and 'bookmarks'. 2. Structure screens inside visual FRAMES, ALWAYS including a 'Splash Screen' frame displaying credit to 'Miller Software Solutions LLC' with a copyright notice, followed by main app views. 3. Place CARDS for UI components, SHAPES for controls/inputs, and STICKY_NOTES for layout/theming guidelines. 4. Connect screens using ORTHOGONAL CONNECTORS with directional arrows and event labels (e.g. 'onAppLaunch', 'onItemClick', 'onSave'). 5. Save the JSON model to '<projectName>-ui-design.whiteboard' in the project root.\"",
       "dir": "."
     }
     ```
4. **Render Screen Transition Diagrams**:
   - Call `renderMermaidDiagram` or `generateDiagram` to render auxiliary state transition charts.
5. **Log Design Brief**:
   - Call `storeBriefEntry` with category `design` noting the new `.whiteboard` file.

---

## 2. Multi-Platform Design System Guidelines

### 1. Android UI (Material 3 & Jetpack Compose)
- **Splash Screen & Attribution**: Splash Screen API (`core-splashscreen`) or custom Compose splash screen featuring logo, credit to "Miller Software Solutions LLC", and copyright notice.
- **Design Tokens**: Material Theme color schemes (Primary, Secondary, Tertiary, Surface, Background, Error).
- **Layouts**: `Scaffold` with `TopAppBar`, `NavigationBar` or `NavigationRail` for tablets, `LazyColumn` for dynamic lists, `ModalBottomSheet` for secondary workflows.
- **Adaptive Ergonomics**: Support compact (<600dp), medium (600-840dp), and expanded (>840dp) screen widths.

### 2. JavaFX UI (Modern Scenic Design & CSS)
- **Splash Screen & Attribution**: Preloader stage or startup splash overlay giving credit for the app to "Miller Software Solutions LLC" with a copyright notice.
- **Theme Variables**: Define global CSS root variables (`-fx-base`, `-fx-accent`, `-fx-background`, `-fx-text-fill`, `-surface-card`).
- **Containers**: Responsive `BorderPane` shells, `GridPane` property forms, `HBox`/`VBox` toolbars with `Priority.ALWAYS` fillers.
- **Micro-Styling**: 8px rounded corners (`-fx-background-radius: 8px`), drop-shadow elevations, clean scrollbar tracks.

### 3. Angular UI (Standalone Components & Modern CSS)
- **Splash Screen & Attribution**: Dedicated splash screen component with branding, credit to "Miller Software Solutions LLC", and copyright notice.
- **Component Hierarchy**: Smart container components + reusable dumb presentational components.
- **Layout Styling**: Modern CSS Grid dashboards, responsive Flexbox alignment, CSS custom property tokens.
- **State States**: Provide clear visual designs for loading spinners, skeleton loaders, empty states, and error alerts.

---

## 3. Software Development Kanban Workflow (Column 2: UI Design)

When executing an approved card in the `Software Development` Kanban swimlane under `UI Design`:

1. **Ingest Specification**: Read the requirement specification and architecture ADD referenced in the card.
2. **Create Whiteboard UI Outline with Splash Screen**:
   - Generate `<projectName>-ui-design.whiteboard` via Antigravity (`agy`) detailing screens, layout containers, and design tokens.
   - Ensure a **Splash Screen** is always present in the layout, crediting **Miller Software Solutions LLC** and including a **copyright notice**.
3. **Route Downstream**:
   - Create card in Column 3 (`Software Development`) for `@Software Engineer`:
     - Tool: `createCard(row: "Software Development", column: "Software Development", title: "Develop: <FeatureTitle>", prompt: "### Software Implementation Directives\n\n- **Project**: `<projectName>`\n- **ADD Reference**: `doc/add/<NUMBER>-<slug>.md`\n- **UI Whiteboard Model**: `<projectName>-ui-design.whiteboard`\n- **Instructions**: Implement full-stack features including the UI wireframe layouts, design tokens, and the mandatory splash screen crediting Miller Software Solutions LLC with copyright notice defined in the Whiteboard.\n\nToggle switch to **Approved** to trigger Software Engineer!", approved: true)`

---

## 4. Critical Execution Rules

1. **Mandatory Splash Screen & Attribution**: A splash screen MUST always be present for any application across Android, JavaFX, and Angular, giving credit for the app to **Miller Software Solutions LLC** and displaying an official copyright notice.
2. **Aesthetic Excellence**: Never produce basic or dated UI mockups. Champion vibrant modern palettes, clean typography, and spacious layouts.
3. **Interactive Whiteboard Output**: Always deliver a `.whiteboard` model for visual layout requests.
4. **Preserve Workspace Files**: Never delete or overwrite existing project files or documentation.

