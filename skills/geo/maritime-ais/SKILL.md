---
name: maritime-ais
description: Tracks marine vessels, MMSI positions, speed over ground (SOG), course over ground (COG), and port arrivals using AIS Trail and Digitraffic Marine AIS APIs, plotting vessel trajectories on the Nadia World Map.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: geo
  display-name: MaritimeAisSkill
allowed-tools: showMap setMapNauticalView plotObject setFlag clearMap executeSessionCommand storeBriefEntry searchMemory saveMemory getNadiaProperty setNadiaProperty
tools: [showMap, setMapNauticalView, plotObject, setFlag, clearMap, executeSessionCommand, storeBriefEntry, searchMemory, saveMemory, getNadiaProperty, setNadiaProperty]
properties: [nadia.prop.aistrail.apiKey]
---

# Maritime AIS & Vessel Tracking Skill (`AIS Trail` & `Digitraffic`)

This skill extends Nadia's aviation and satellite tracking capabilities to maritime vessels, enabling `@Network Engineer`, `@Researcher`, and `@Scoutmaster` to look up live ship positions by MMSI, bounding box, or vessel metadata and plot marine trajectories on the Nadia World Map with the OpenSeaMap nautical layer (`setMapNauticalView`).

---

## Setup Instructions

### External App & Integration Setup

1. **World Map Viewer PF4J Plugin (`world-map-viewer`)**:
   - In Nadia, open **⚙️ System Settings ➔ Plugins**.
   - Click **Install from URL...** and enter `https://github.com/Ghost-Programmer/nadia-plugins` (or click **Install from Disk...** to select `world-map-viewer-<version>.jar`, or place the JAR directly in `~/.nadia/plugins/`).
   - Verify `world-map-viewer` shows **STARTED / Enabled**, then open **View ➔ 🗺️ World Map** (or invoke `showMap()`).
2. **Python 3.10+ Runtime**:
   - Install Python 3.10+ on system `PATH` (uses standard library only; script at `~/.nadia/skills/geo/maritime-ais/scripts/maritime_ais.py`).
3. **AIS Trail API Key (`nadia.prop.aistrail.apiKey`)**:
   - Digitraffic Baltic/Nordic Marine AIS feeds work keyless out-of-the-box.
   - For global AIS Trail vessel tracking, generate an API key from your AIS Trail account and save `nadia.prop.aistrail.apiKey` in **⚙️ System Settings ➔ Properties** (`~/.nadia/nadia.properties`).

---

## 1. Core Operational Workflows

### 1.1 Looking Up a Vessel by MMSI (`vessel`)
Retrieve position, speed over ground (`sog`), course over ground (`cog`), heading, and navigation status for a specific 9-digit MMSI:

```bash
python ~/.nadia/skills/geo/maritime-ais/scripts/maritime_ais.py vessel --mmsi "230992680"
```

### 1.2 Scanning Active Vessels in a Bounding Box (`bbox`)
Retrieve active vessels reporting AIS telemetry inside a geographic bounding box (`min-lat`, `max-lat`, `min-lon`, `max-lon`):

```bash
python ~/.nadia/skills/geo/maritime-ais/scripts/maritime_ais.py bbox --min-lat 59.5 --max-lat 60.5 --min-lon 24.0 --max-lon 26.0 --limit 15
```

---

## 2. World Map Integration

1. Call `showMap()` and `setMapNauticalView(true)` to enable the OpenSeaMap nautical seamarks overlay.
2. Call `plotObject(name, latitude, longitude)` for each vessel to render its position and track on the map.
