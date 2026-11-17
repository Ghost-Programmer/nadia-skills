---
name: map
description: Renders interactive map and tracks coordinates of objects and sets color flags.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: geo
  display-name: MapSkill
allowed-tools: showMap plotObject setFlag clearMap
tools: [showMap, plotObject, setFlag, clearMap]
properties: [nadia.prop.windy.api-key, nadia.prop.webcams.windy.api-key]
---

# Map Skill

Provides capabilities to view coordinates of objects and flags on an interactive World Map powered by Google Maps roadmap layers.

---

## Setup Instructions

### External App & Integration Setup

1. **World Map Viewer PF4J Plugin (`world-map-viewer`)**:
   - In Nadia, open **⚙️ System Settings ➔ Plugins**.
   - Click **Install from URL...** and enter `https://github.com/Ghost-Programmer/nadia-plugins` (or click **Install from Disk...** to select `world-map-viewer-<version>.jar`, or place the JAR directly in `~/.nadia/plugins/`).
   - Verify `world-map-viewer` shows **STARTED / Enabled**, then open **View ➔ 🗺️ World Map** (or invoke `showMap()`).
2. **Map Tile Access (Keyless Base Layers)**:
   - Standard roadmap, satellite, terrain, day/night terminator, and OpenSeaMap nautical layers work out-of-the-box with outbound HTTPS access (ports `80`/`443`).
3. **Windy Weather Overlay & Webcams API Keys (Optional)**:
   - To enable interactive Windy meteorological wind overlays or live webcam markers:
     1. Visit [Windy API Keys Portal](https://api.windy.com/keys) and generate keys for **Map Forecast API** and/or **Webcams API**.
     2. In Nadia, open **⚙️ System Settings ➔ Properties** (or call `setNadiaProperty`) and configure:
        ```properties
        nadia.prop.windy.api-key=your_windy_map_forecast_key
        nadia.prop.webcams.windy.api-key=your_windy_webcams_key
        ```

---

## Guidelines

1. **Viewing the Map**:
   - When the user asks to "open the map", "view map", or similar requests, call `showMap()`.

2. **Plotting Objects**:
   - To map or track moving objects (such as aircraft, flights, satellites, ships, or land vehicles) with names and coordinates, use `plotObject(name, latitude, longitude)`.
   - Plotting the same object name multiple times dynamically creates a path connecting previous locations in chronological sequence.
   - Example: Plotting a flight trajectory or tracking ISS.

3. **Placing Flags**:
   - To mark specific single coordinate points (cities, coordinate points, ports, waypoints) with colored flags, use `setFlag(latitude, longitude, color)`.
   - Available colors: `red`, `green`, `blue`, `yellow`, `orange`, `purple`, `white`, `cyan`, `pink`.

4. **Clearing map**:
   - Use `clearMap()` if the user requests to reset or wipe all coordinates from the viewer.
