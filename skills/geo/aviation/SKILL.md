---
name: aviation
description: Tracks live aircraft positions, schedules continuous flight tracking, and updates flight paths on the World Map using OpenSky Network.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: geo
  display-name: AviationSkill
allowed-tools: trackPlanes startContinuousPlaneTracking stopContinuousPlaneTracking getPlaneTrackingStatus showMap clearMap
tools: [trackPlanes, startContinuousPlaneTracking, stopContinuousPlaneTracking, getPlaneTrackingStatus, showMap, clearMap]
properties: [nadia.prop.opensky.username, nadia.prop.opensky.password]
---

# Aviation Skill

Provides capabilities to query live aircraft locations, configure automatic flight tracking loops, and plot plane trajectories on the World Map.

---

## Setup Instructions

### External App & Integration Setup

1. **World Map Viewer PF4J Plugin (`world-map-viewer`)**:
   - In Nadia, open **⚙️ System Settings ➔ Plugins**.
   - Click **Install from URL...** and enter `https://github.com/Ghost-Programmer/nadia-plugins` (or click **Install from Disk...** to select `world-map-viewer-<version>.jar`, or place the JAR directly in `~/.nadia/plugins/`).
   - Verify `world-map-viewer` shows **STARTED / Enabled**, then open **View ➔ 🗺️ World Map** (or invoke `showMap()`).
2. **OpenSky Network Account Setup (Optional — Higher Rate Limits)**:
   - Anonymous queries to `https://opensky-network.org/api` work out-of-the-box with stricter public rate limits.
   - For higher authenticated request quotas:
     1. Create a free account at [OpenSky Network](https://opensky-network.org/).
     2. Open **⚙️ System Settings ➔ Properties** in Nadia (or call `setNadiaProperty`) and configure:
        ```properties
        nadia.prop.opensky.username=your_opensky_username
        nadia.prop.opensky.password=your_opensky_password
        ```
3. **Recommended Polling Cadence**: Use 15–30 second intervals for continuous tracking to avoid HTTP 429 throttling.

---

## Guidelines

1. **Prerequisite - Map Open**:
   - Live tracking operates relative to the current map view boundary. Ensure the World Map Viewer window is opened first using `showMap()`.
   - If the map is not open or loaded, flight tracking tools will return an error instructing you to open the map.

2. **One-Time Flight Tracking**:
   - To get active flights inside the current viewport area and plot them, call `trackPlanes()`.
   - This pulls real-time state vectors (position, altitude, velocity, and true track/heading) from the OpenSky Network REST API and plots them as rotating aircraft icons pointing in the direction of travel.
   - Sequential updates of the same callsign will dynamically move the plane and draw a dash-lined flight path behind it.

3. **Continuous Tracking Loop**:
   - To schedule periodic background flight tracking updates, call `startContinuousPlaneTracking(intervalSeconds)`.
   - The minimum allowed interval is 5 seconds. However, it is highly recommended to use **15 to 30 seconds** (e.g. 15 or 30) to respect OpenSky Network's rate limits and avoid 429 errors.
   - Use `getPlaneTrackingStatus()` to verify whether background plane tracking is active and to retrieve its current update interval configuration.
   - To terminate the background updates, call `stopContinuousPlaneTracking()`.

4. **Cleaning Flight Paths**:
   - Use `clearMap()` to reset the viewport, removing all aircraft, paths, and flags.

5. **Displaying Flight Details**:
   - Whenever you fetch flight data (either through one-time tracking or when reporting updates), always output a clean, structured Markdown table summarizing all current flights in the area with their known details.
   - The table columns should include: `Callsign`, `Latitude`, `Longitude`, `Altitude (m)`, `Speed (m/s)`, `Heading (°)`, and `Country of Origin`.
