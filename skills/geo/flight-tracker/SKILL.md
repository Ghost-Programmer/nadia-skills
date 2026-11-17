---
name: flight-tracker
description: Tracks a single aircraft or satellite on the World Map in real time, auto-recenters the map when the target nears viewport edges, and logs rich flight intelligence briefings into the daily brief.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: geo
  display-name: FlightTrackerSkill
allowed-tools: trackFlight stopTrackingFlight getTrackedFlightStatus recenterOnTrackedFlight centerMap setMapView storeBriefEntry appendBriefEntry getBriefEntries showMap clearMap
tools: [trackFlight, stopTrackingFlight, getTrackedFlightStatus, recenterOnTrackedFlight, centerMap, setMapView, storeBriefEntry, appendBriefEntry, getBriefEntries, showMap, clearMap]
properties: [nadia.prop.opensky.username, nadia.prop.opensky.password, nadia.prop.n2yo.apiKey]
---

# Flight Tracker Skill

Provides specialized procedural guidance for tracking an individual aircraft or satellite on the Nadia World Map, automatically repositioning the viewport when the craft approaches the edge of the visible map, and generating comprehensive flight intelligence briefings in the daily brief.

---

## Setup Instructions

### External App & Integration Setup

1. **World Map Viewer PF4J Plugin (`world-map-viewer`)**:
   - In Nadia, open **⚙️ System Settings ➔ Plugins**.
   - Click **Install from URL...** and enter `https://github.com/Ghost-Programmer/nadia-plugins` (or click **Install from Disk...** to select `world-map-viewer-<version>.jar`, or place the JAR directly in `~/.nadia/plugins/`).
   - Verify `world-map-viewer` shows **STARTED / Enabled**, then open **View ➔ 🗺️ World Map** (or invoke `showMap()`).
2. **OpenSky Network Credentials (Optional — Aircraft Telemetry)**:
   - Register at [OpenSky Network](https://opensky-network.org/) and set `nadia.prop.opensky.username` and `nadia.prop.opensky.password` in **⚙️ System Settings ➔ Properties** (`~/.nadia/nadia.properties`) for higher ADS-B polling quotas (anonymous mode is used if unset).
3. **N2YO API Key (Required for Orbital Satellite Target Tracking)**:
   - Create a free account at [N2YO.com](https://www.n2yo.com/login/), open **Your Profile** to generate a REST API Key, and set `nadia.prop.n2yo.apiKey` in **⚙️ System Settings ➔ Properties**.
4. **FAA Aircraft Registry Enrichment**:
   - Handled automatically by `FaaRegistryService` inside `world-map-viewer`—no external FAA credentials required.

---

## 1. Single-Target Tracking Constraint

> [!IMPORTANT]
> The Flight Tracker strictly monitors **only 1 plane or satellite at a time**.
> When a new aircraft or satellite is selected for tracking, any prior tracking loop is immediately and automatically superseded and halted.

---

## 2. Core Capabilities & Tool Directives

### 2.1 Initiating Active Target Tracking
- Call `trackFlight(targetIdentifier, targetType)`:
  - `targetIdentifier`: The aircraft callsign, 24-bit Mode S ICAO hex address, FAA N-number (e.g., `"UAL456"`, `"a1b2c3"`, `"N12345"`), or satellite name / NORAD catalog ID (e.g., `"ISS (ZARYA)"`, `"25544"`).
  - `targetType`: `"plane"` (or `"aircraft"`) for flights, or `"satellite"` for orbital spacecraft.
- Tracking immediately:
  1. Identifies the target coordinates and centers the map view (`centerMap` / `panTo`).
  2. Plots the target marker with a distinctive trail on the World Map.
  3. Launches a background polling daemon (every 10 seconds for aircraft, 15 seconds for satellites) to continuously stream real-time telemetry.

### 2.2 Viewport Boundary Monitoring & Edge-Triggered Auto-Recentering
- The viewport boundaries are actively monitored as the craft travels across the globe.
- **Edge Threshold**: When the tracked aircraft or satellite approaches within **18% of any viewport boundary edge** (North, South, East, or West), the system automatically triggers a smooth `panTo(lat, lon)` recentering command to keep the vehicle in optimal viewing focus.
- If the user or agent desires an immediate manual view alignment, call `recenterOnTrackedFlight()` or `centerMap(latitude, longitude)`.

### 2.3 Comprehensive Flight Briefing Updates
- As telemetry streams in, the Flight Tracker synthesizes and persists structured Markdown briefings into the system `BriefService`:
  - **Category**: `"flight"`
  - **Code**: `"active_flight_tracking"`
  - **Staff Origin**: `"Flight Tracker"`
- The brief is enriched with all discoverable intelligence:
  - **Transponder & Identification**: Callsign, Mode S 24-bit Hex address, Squawk code, Country of origin.
  - **Flight Dynamics**: Geodetic latitude, longitude, barometric / geometric altitude, ground speed, heading, and vertical climb / descent rate.
  - **FAA Civil Aviation Registry Data**: Registered owner name, owner address (city, state, country), aircraft manufacturer, specific model, serial number, manufacture year, airworthiness status, and engine type.
  - **Orbital Metrics (for Satellites)**: NORAD catalog ID, orbital altitude (km), geocentric coordinates, and visibility pass details.

### 2.4 Status Inspection & Halting Tracking
- To inspect active tracking metrics without interrupting the loop, call `getTrackedFlightStatus()`.
- To terminate active tracking, call `stopTrackingFlight()`.

---

## 3. Map Card & Hover Integration

- Aircraft cards and satellite cards in `map.html` feature a **Track with Flight Tracker** action button.
- When clicked in the UI, the map JavaScript bridge dispatches `trackTarget(name, type)` directly to the `FlightTrackerService`, initiating the single-target tracking loop, centering the viewport, and updating the flight brief synchronously.
- When tracking is active, the UI button illuminates green as `🎯 Active Flight Tracker` with a click-to-stop option.
