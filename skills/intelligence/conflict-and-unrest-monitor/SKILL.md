---
name: conflict-and-unrest-monitor
description: Tracks active armed conflict, protests, political violence, and fatality spikes globally using ACLED, UCDP GED, and GDELT GEO 2.0, optionally plotting hotspots on the World Map Viewer.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: intelligence
  display-name: ConflictAndUnrestMonitorSkill
allowed-tools: acledSearchEvents acledGetCountrySummary ucdpSearchGedEvents gdeltSearchGeoEvents gdeltSearchArticles storeBriefEntry searchMemory saveMemory
tools: [acledSearchEvents, acledGetCountrySummary, ucdpSearchGedEvents, gdeltSearchGeoEvents, gdeltSearchArticles, storeBriefEntry, searchMemory, saveMemory]
properties: [nadia.prop.acled.email, nadia.prop.acled.password]
---

# Conflict & Unrest Monitor Skill

Monitors armed conflicts, civil unrest, protests, and security flashpoints in near-real time and produces georeferenced situational briefings.

---

## Setup Instructions

- **ACLED (`acled-mcp`)**: Configure `nadia.prop.acled.email` and `nadia.prop.acled.password` (or `nadia.prop.acled.apiKey`) in **Settings ➔ Properties**.
- **UCDP (`ucdp-displacement-mcp`)**: Optionally configure `nadia.prop.ucdp.accessToken`.
- **GDELT (`gdelt-mcp`)**: Keyless out-of-the-box.

---

## Operational Workflow

1. **Pull Recent Conflict Events**:
   - Call `acledSearchEvents` filtered by target country/region, `eventType` (`Battles`, `Protests`, `Explosions/Remote violence`, `Violence against civilians`), and date window.
   - Cross-check historical/georeferenced baselines with `ucdpSearchGedEvents`.
2. **Correlate Real-Time News & Coordinates**:
   - Call `gdeltSearchGeoEvents` and `gdeltSearchArticles` (`theme: "PROTEST"` or `"ARMEDCONFLICT"`) for breaking developments not yet coded in ACLED.
3. **Report**:
   - Output a structured Markdown table of top hotspots (Date, Location, Event Type, Actors, Fatalities, Source) and highlight emerging escalation clusters.
