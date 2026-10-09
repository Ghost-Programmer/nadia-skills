---
name: AviationSkill
description: Tracks live aircraft positions, schedules continuous flight tracking, and updates flight paths on the World Map using OpenSky Network.
tools: [trackPlanes, startContinuousPlaneTracking, stopContinuousPlaneTracking, getPlaneTrackingStatus, showMap, clearMap]
---

# Aviation Skill

Provides capabilities to query live aircraft locations, configure automatic flight tracking loops, and plot plane trajectories on the World Map.

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
