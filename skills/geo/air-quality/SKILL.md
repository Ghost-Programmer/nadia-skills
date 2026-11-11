---
name: air-quality
description: Queries quantitative Air Quality Index (AQI), PM2.5, PM10, Ozone (O3), NO2, and wildfire smoke advisories from US EPA AirNow and the World Air Quality Index (AQICN), and toggles the World Map AQI layer.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
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

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/geo/air-quality/scripts/air_quality.py`.
- **Configuration Properties (`nadia.prop.*`)**:
  - `nadia.prop.airnow.apiKey`: US EPA AirNow API key.
  - `nadia.prop.aqicn.apiKey`: World Air Quality Index (AQICN) token.

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

