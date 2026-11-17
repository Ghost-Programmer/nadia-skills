---
name: air-quality
description: Queries quantitative Air Quality Index (AQI), PM2.5, PM10, Ozone (O3), NO2, and wildfire smoke advisories from US EPA AirNow and the World Air Quality Index (AQICN), and toggles the World Map AQI layer.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: geo
  display-name: AirQualitySkill
allowed-tools: showMap setMapAirQualityView setFlag plotObject executeSessionCommand storeBriefEntry searchMemory saveMemory getNadiaProperty setNadiaProperty
tools: [showMap, setMapAirQualityView, setFlag, plotObject, executeSessionCommand, storeBriefEntry, searchMemory, saveMemory, getNadiaProperty, setNadiaProperty]
properties: [nadia.prop.airnow.apiKey, nadia.prop.aqicn.apiKey]
---

# Air Quality & Atmospheric Pollutants Skill (`AirNow` & `AQICN`)

This skill enables `@Scoutmaster`, `@Personal Assistant`, and `@Researcher` to retrieve real-time Air Quality Index (AQI), particulate matter (`PM2.5`, `PM10`), ground-level Ozone (`O3`), Nitrogen Dioxide (`NO2`), and health advisories from **[US EPA AirNow](https://docs.airnowapi.org/)** and the **[World Air Quality Index (AQICN)](https://aqicn.org/api/)**, alongside activating the World Map AQI overlay (`setMapAirQualityView`).

---

## Setup Instructions

### External App & Integration Setup

1. **World Map Viewer PF4J Plugin (`world-map-viewer`)**:
   - In Nadia, open **⚙️ System Settings ➔ Plugins**.
   - Click **Install from URL...** and enter `https://github.com/Ghost-Programmer/nadia-plugins` (or click **Install from Disk...** to select `world-map-viewer-<version>.jar`, or place the JAR directly in `~/.nadia/plugins/`).
   - Verify `world-map-viewer` shows **STARTED / Enabled**, then open **View ➔ 🗺️ World Map** (or invoke `showMap()`).
2. **Python 3.10+ Runtime**:
   - Install Python 3.10+ on system `PATH` (uses standard library only; script at `~/.nadia/skills/geo/air-quality/scripts/air_quality.py`).
3. **AirNow & AQICN API Keys (`nadia.prop.*`)**:
   - **US EPA AirNow**: Register for a free account at [AirNow API Account Request](https://docs.airnowapi.org/account/request/) to obtain an API key, then set `nadia.prop.airnow.apiKey` in **⚙️ System Settings ➔ Properties**.
   - **World Air Quality Index (AQICN)**: Request a free API token at [AQICN Data Platform Token](https://aqicn.org/data-platform/token/), then set `nadia.prop.aqicn.apiKey` in **⚙️ System Settings ➔ Properties**.

---

## 1. Core Operational Workflows

### 1.1 Querying Global Station AQI by City or Coordinates (`aqicn`)
Retrieve station AQI, dominant pollutant, and pollutant breakdown (`pm25`, `pm10`, `o3`, `no2`, `so2`, `co`):

```bash
python ~/.nadia/skills/geo/air-quality/scripts/air_quality.py aqicn --city "Denver"
```

- Or by coordinates:
  ```bash
  python ~/.nadia/skills/geo/air-quality/scripts/air_quality.py aqicn --lat 39.7392 --lon -104.9903
  ```

### 1.2 Querying US EPA AirNow Observations by Lat/Lon (`airnow`)
Retrieve official US EPA AQI readings and health categories (`Good`, `Moderate`, `Unhealthy for Sensitive Groups`, `Unhealthy`, `Very Unhealthy`, `Hazardous`):

```bash
python ~/.nadia/skills/geo/air-quality/scripts/air_quality.py airnow --lat 37.7749 --lon -122.4194 --distance-miles 25
```

---

## 2. World Map Integration

1. When reporting air quality for a region, call `showMap()`, `setMapAirQualityView(true)`, and place a color-coded marker via `setFlag(latitude, longitude, color)` (`green` for AQI 0–50, `yellow` for 51–100, `orange` for 101–150, `red` for 151+).
