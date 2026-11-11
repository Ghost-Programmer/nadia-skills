---
name: design-assets
description: Searches 200+ open-source SVG icon libraries (Iconify), generates harmonious AI color palettes (Colormind), and builds placeholder graphics (DummyImage) for Android, JavaFX, and Angular UI development.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
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

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/development/design-assets/scripts/design_assets.py`.
- **Configuration Properties (`nadia.prop.*`)**: Keyless (`properties: []`).

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

