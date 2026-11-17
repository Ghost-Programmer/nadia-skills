---
name: earthquakes-hazards
description: Queries real-time global earthquakes (USGS Earthquake Hazards Program) and US river/stream water gauges (USGS Water Services) and plots seismic or hydrologic hazards on the Nadia World Map.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: geo
  display-name: EarthquakesHazardsSkill
allowed-tools: showMap plotObject setFlag clearMap executeSessionCommand storeBriefEntry searchMemory saveMemory
tools: [showMap, plotObject, setFlag, clearMap, executeSessionCommand, storeBriefEntry, searchMemory, saveMemory]
properties: []
---

# Earthquakes & Natural Hazards Skill (`USGS`)

This skill enables the cognitive agent (`@Scoutmaster`, `@Researcher`, `@Network Engineer`) to query real-time global seismic events from the **[USGS Earthquake Hazards Program](https://earthquake.usgs.gov/fdsnws/event/1/)** and real-time river/stream levels from **[USGS Water Services](https://waterservices.usgs.gov/)**, and plot significant hazards directly onto the interactive Nadia World Map.

---

## Setup Instructions

### External App & Integration Setup

1. **World Map Viewer PF4J Plugin (`world-map-viewer`)**:
   - In Nadia, open **⚙️ System Settings ➔ Plugins**.
   - Click **Install from URL...** and enter `https://github.com/Ghost-Programmer/nadia-plugins` (or click **Install from Disk...** to select `world-map-viewer-<version>.jar`, or place the JAR directly in `~/.nadia/plugins/`).
   - Verify `world-map-viewer` shows **STARTED / Enabled**, then open **View ➔ 🗺️ World Map** (or invoke `showMap()`).
   - *Note*: The `world-map-viewer` plugin also provides native live USGS earthquake tools (`trackEarthquakes`, `trackGlobalEarthquakes`, `setEarthquakeLookbackDays` for 1–7 days, and `startContinuousEarthquakeTracking`) plus a built-in toolbar day selector.
2. **Python 3.10+ Runtime (for `usgs_hazards.py` & River Gauges)**:
   - Install Python 3.10+ on system `PATH` (uses standard library only; script at `~/.nadia/skills/geo/earthquakes-hazards/scripts/usgs_hazards.py`).
3. **USGS Hazard Feeds (Keyless)**:
   - Requires outbound HTTPS access to [USGS Earthquake Hazards](https://earthquake.usgs.gov/fdsnws/event/1/) and [USGS Water Services](https://waterservices.usgs.gov/). No API keys are required (`properties: []`).

---

## 1. Core Operational Workflows

### 1.1 Querying Recent Earthquakes (`quakes`)
Fetch recent earthquakes filtered by minimum magnitude, lookback hours/days, or geographic radius:

```bash
python ~/.nadia/skills/geo/earthquakes-hazards/scripts/usgs_hazards.py quakes --min-magnitude 4.5 --days 7 --limit 15
```

- **Radius search around coordinates**:
  ```bash
  python ~/.nadia/skills/geo/earthquakes-hazards/scripts/usgs_hazards.py quakes --min-magnitude 2.5 --days 7 --lat 37.7749 --lon -122.4194 --radius-km 300
  ```

### 1.2 Plotting Earthquakes on the World Map
When the user asks to see earthquakes on the map:
1. Call `showMap()` to ensure the World Map Viewer is active.
2. Run `usgs_hazards.py quakes` to retrieve event coordinates and magnitudes.
3. For each significant earthquake, call `setFlag(latitude, longitude, color)`:
   - Magnitude `>= 6.0`: `"red"`
   - Magnitude `4.5 - 5.9`: `"orange"`
   - Magnitude `< 4.5`: `"yellow"`

### 1.3 Querying River & Stream Water Conditions (`water`)
For outdoor trail safety (`@Scoutmaster`) or flood monitoring, query real-time USGS stream discharge (`00060`, ft³/s) and gage height (`00065`, ft) by US state code or USGS site ID:

```bash
python ~/.nadia/skills/geo/earthquakes-hazards/scripts/usgs_hazards.py water --state "CO" --limit 10
```

---

## 2. Presentation Guidelines

1. Always present earthquake results in a Markdown table with columns: `Magnitude`, `Location / Place`, `Depth (km)`, `Coordinates (Lat, Lon)`, `Time (UTC)`, and `Tsunami Alert`.
2. When plotting on the World Map, confirm the number of seismic markers placed and highlight the strongest event.
