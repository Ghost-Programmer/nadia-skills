---
name: MapSkill
description: Renders interactive map and tracks coordinates of objects and sets color flags.
tools: [showMap, plotObject, setFlag, clearMap]
---

# Map Skill

Provides capabilities to view coordinates of objects and flags on an interactive World Map powered by Google Maps roadmap layers.

## Setup Instructions

- **JavaFX Map Component**:
  - Requires JavaFX WebView and WebEngine components enabled in the runtime.
- **Network Tile Access**:
  - Outbound internet access to map tile providers (Google Maps / OpenStreetMap) on port 80/443.
- **Tool Registrations**:
  - `showMap`, `plotObject`, `setFlag`, and `clearMap` registered in `ToolRegistry`.

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
