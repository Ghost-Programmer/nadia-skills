---
name: design-assets
description: Searches 200+ open-source SVG icon libraries (Iconify), generates harmonious AI color palettes (Colormind), and builds placeholder graphics (DummyImage) for Android, JavaFX, and Angular UI development.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: development
  display-name: DesignAssetsSkill
allowed-tools: executeSessionCommand generateDiagram renderMermaidDiagram storeBriefEntry searchMemory saveMemory
tools: [executeSessionCommand, generateDiagram, renderMermaidDiagram, storeBriefEntry, searchMemory, saveMemory]
properties: []
---

# UI Design Assets, Icons & Color Palettes Skill (`Iconify`, `Colormind` & `DummyImage`)

This skill equips `@UI Designer` and `@Software Engineer` with instant access to over 200,000 open-source vector SVG icons via **[Iconify](https://iconify.design/docs/api/)**, deep-learning 5-color UI palettes via **[Colormind](http://colormind.io/api-access/)**, and responsive placeholder image URLs via **[DummyImage](https://dummyimage.com/)** without requiring any API keys.

---

## Setup Instructions

### External App & Integration Setup

- **Python 3.10+ Runtime**:
  - Install Python 3.10+ and ensure `python` is on system `PATH`:
    - **Windows**: `winget install Python.Python.3.12` (enable *"Add python.exe to PATH"*)
    - **macOS**: `brew install python`
    - **Linux**: `sudo apt install python3`
  - Uses Python's built-in standard library only (no `pip install` packages required).
- **External Design APIs (Keyless)**:
  - Requires outbound HTTP/HTTPS access to [Iconify API](https://api.iconify.design) (200k+ open-source SVG icons), [Colormind API](http://colormind.io/api/) (AI 5-color palettes), and [DummyImage](https://dummyimage.com). No API keys or accounts are required (`properties: []`).
- **Bundled Script**: `~/.nadia/skills/development/design-assets/scripts/design_assets.py`.

---

## 1. Core Operational Workflows

### 1.1 Searching Open-Source SVG Icons (`icons`)
Search across Material Design Icons (`mdi`), Lucide (`lucide`), Heroicons (`heroicons`), Tabler (`tabler`), and Phosphor (`ph`):

```bash
python ~/.nadia/skills/development/design-assets/scripts/design_assets.py icons --query "dashboard" --limit 15
```

### 1.2 Downloading Raw SVG Markup for an Icon (`svg`)
Retrieve the raw `<svg>...</svg>` vector markup for any `prefix:name` icon (e.g., `mdi:shield-check`, `lucide:sparkles`):

```bash
python ~/.nadia/skills/development/design-assets/scripts/design_assets.py svg --icon "mdi:rocket-launch"
```

### 1.3 Generating Harmonious 5-Color UI Palettes (`palette`)
Generate a 5-color UI theme palette (`background`, `surface`, `primary`, `accent`, `text`) with HEX and RGB tokens:

```bash
python ~/.nadia/skills/development/design-assets/scripts/design_assets.py palette
```

### 1.4 Generating Placeholder Image URLs (`placeholder`)
Create custom-sized placeholder graphic URLs for wireframes and mockups:

```bash
python ~/.nadia/skills/development/design-assets/scripts/design_assets.py placeholder --width 800 --height 450 --bg "1e293b" --fg "f8fafc" --text "Miller Software Solutions LLC"
```
