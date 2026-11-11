---
name: national-parks
description: Queries the US National Park Service (NPS) API for park alerts, campgrounds, visitor centers, and events, and queries iNaturalist for local wildlife and plant observations.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: geo
  display-name: NationalParksSkill
allowed-tools: showMap plotObject setFlag clearMap executeSessionCommand storeBriefEntry searchMemory saveMemory getNadiaProperty setNadiaProperty
tools: [showMap, plotObject, setFlag, clearMap, executeSessionCommand, storeBriefEntry, searchMemory, saveMemory, getNadiaProperty, setNadiaProperty]
properties: [nadia.prop.nps.apiKey]
---

# National Parks & Biodiversity Skill (`NPS` & `iNaturalist`)

This skill empowers `@Scoutmaster` and `@Personal Assistant` to retrieve official US National Park Service (**[NPS API](https://www.nps.gov/subjects/developer/api-documentation.htm)**) park details, active trail/road closures and safety alerts, campground availability, and nearby biodiversity/wildlife observations from **[iNaturalist](https://api.inaturalist.org/v1/docs/)**, and plot park locations and campgrounds on the Nadia World Map.

---

## Setup Instructions

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/geo/national-parks/scripts/parks_wildlife.py`.
- **Configuration Properties (`nadia.prop.*`)**:
  - Requires `nadia.prop.nps.apiKey` in `~/.nadia/nadia.properties` (configure via **Settings ➔ Properties** or `setNadiaProperty`).

---

## 1. Core Operational Workflows

### 1.1 Searching National Parks by State or Keyword (`parks`)
Search US National Parks, Monuments, and Recreation Areas by two-letter state code or query:

```bash
python ~/.nadia/skills/geo/national-parks/scripts/parks_wildlife.py parks --state "UT" --limit 10
```

### 1.2 Checking Active Park Alerts & Trail Closures (`alerts`)
Before planning a backcountry trek (`@Scoutmaster`), check active road closures, bear warnings, or weather alerts for a park code (e.g., `yose`, `zion`, `grca`, `romo`, `yell`):

```bash
python ~/.nadia/skills/geo/national-parks/scripts/parks_wildlife.py alerts --park-code "yose"
```

### 1.3 Finding Campgrounds in a National Park (`campgrounds`)
Retrieve campground locations, reservation links, campsite counts, and fees:

```bash
python ~/.nadia/skills/geo/national-parks/scripts/parks_wildlife.py campgrounds --park-code "zion"
```

### 1.4 Querying Local Wildlife & Flora Observations (`wildlife`)
Query recent research-grade wildlife and plant sightings via iNaturalist around coordinates (`lat`, `lon`, `radius-km`):

```bash
python ~/.nadia/skills/geo/national-parks/scripts/parks_wildlife.py wildlife --lat 37.8651 --lon -119.5383 --radius-km 25 --limit 15
```

---

## 2. World Map Integration

1. Call `showMap()` and plot parks or campgrounds using `setFlag(latitude, longitude, "green")`.
2. Plot active park hazard alerts using `setFlag(latitude, longitude, "orange")` or `"red"`.

