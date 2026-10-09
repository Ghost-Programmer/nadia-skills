---
name: SatelliteSkill
description: Tracks live satellite positions, schedules continuous orbit tracking, and updates satellite positions on the World Map using N2YO.
tools: [trackSatellites, startContinuousSatelliteTracking, stopContinuousSatelliteTracking, getSatelliteTrackingStatus, getSatelliteCategories, showMap, clearMap]
---

# Satellite Skill

Provides capabilities to query live satellite locations, configure automatic orbit tracking loops, and plot satellite trajectories on the World Map.

## Guidelines

1. **Prerequisite - Map Open**:
   - Live tracking operates relative to the current map view boundary. Ensure the World Map Viewer window is opened first using `showMap()`.
   - If the map is not open or loaded, satellite tracking tools will return an error instructing you to open the map.

2. **One-Time Satellite Tracking**:
   - To get active satellites inside the current viewport area and plot them, call `trackSatellites(categoryId)`.
   - The `categoryId` parameter can be used to filter target satellites. Use `0` for All (default), `2` for the International Space Station (ISS), `18` for Amateur Radio, or `30` for Military satellites.
   - Sequential updates of the same satellite will dynamically move its icon and draw a dash-lined orbit path behind it.

3. **Continuous Tracking Loop**:
   - To schedule periodic background satellite tracking updates, call `startContinuousSatelliteTracking(intervalSeconds, categoryId)`.
   - The minimum allowed interval is 5 seconds. However, it is highly recommended to use **30 seconds** (e.g. 30) to respect N2YO API's rate limits and avoid 429 errors.
   - Use `getSatelliteTrackingStatus()` to verify whether background satellite tracking is active and to retrieve its current update interval configuration.
   - To terminate the background updates, call `stopContinuousSatelliteTracking()`.

4. **Displaying Satellite Details**:
   - Whenever you fetch satellite data (either through one-time tracking or when reporting updates), always output a clean, structured Markdown table summarizing all current satellites in the area with their known details.
   - The table columns should include: `Satellite Name`, `NORAD ID`, `Latitude`, `Longitude`, `Altitude (km)`, `Azimuth (°)`, and `Elevation (°)`.

5. **Querying Categories**:
   - Use `getSatelliteCategories()` to retrieve the list of all available satellite categories and their corresponding IDs.
   - When the user asks for available satellite categories, output the list as a clean, structured Markdown table with headers `Category Name` and `Category ID` so the user can easily find categories to filter by.

6. **Cleaning Orbit Paths**:
   - Use `clearMap()` to reset the viewport, removing all satellites, paths, and flags.
