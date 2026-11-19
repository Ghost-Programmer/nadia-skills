---
name: humanitarian-crisis-tracker
description: Monitors active humanitarian emergencies, natural disasters, wildfires, disease outbreaks, and refugee displacement using ReliefWeb, NASA EONET/FIRMS, WHO DON, UNHCR, and GDELT GEO.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: geo
  display-name: HumanitarianCrisisTrackerSkill
allowed-tools: reliefwebSearchDisasters reliefwebSearchReports reliefwebSearchCountries eonetSearchNaturalEvents firmsGetActiveFires whoGetOutbreakNews unhcrGetDisplacementStats gdeltSearchGeoEvents storeBriefEntry
tools: [reliefwebSearchDisasters, reliefwebSearchReports, reliefwebSearchCountries, eonetSearchNaturalEvents, firmsGetActiveFires, whoGetOutbreakNews, unhcrGetDisplacementStats, gdeltSearchGeoEvents, storeBriefEntry]
properties: [nadia.prop.reliefweb.appname]
---

# Humanitarian Crisis Tracker Skill

Tracks ongoing humanitarian emergencies, natural disasters, epidemics, and forced displacement to produce situation reports (SitReps) and aid-needs summaries.

---

## Setup Instructions

- **ReliefWeb (`reliefweb-mcp`)**: Configure `nadia.prop.reliefweb.appname` in **Settings ➔ Properties**.
- **NASA FIRMS (`nasa-firms-mcp`)**: Optional `nadia.prop.nasa.firms.apiKey` for satellite thermal anomalies (`eonetSearchNaturalEvents` is keyless).
- **WHO DON (`radiation-health-mcp`)**, **UNHCR (`ucdp-displacement-mcp`)**, and **GDELT (`gdelt-mcp`)**: Keyless out-of-the-box.

---

## Operational Workflow

1. **Active Emergencies**: Call `reliefwebSearchDisasters` (`status: "current"`) and `reliefwebSearchReports` for the target country or crisis.
2. **Physical Hazards & Health**: Cross-check `eonetSearchNaturalEvents`, `firmsGetActiveFires` (for wildfire crises), and `whoGetOutbreakNews` for secondary epidemic risks.
3. **Displacement Scale**: Query `unhcrGetDisplacementStats` using origin/asylum ISO-3 codes.
4. **SitRep Output**: Summarize affected populations, displacement figures, active hazards, top humanitarian needs, and primary ReliefWeb source links.
