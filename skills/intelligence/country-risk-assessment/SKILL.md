---
name: country-risk-assessment
description: Produces a multi-domain Country Instability Index (CII) and geopolitical risk assessment by correlating ACLED conflict events and CAST forecasts, UCDP/UNHCR displacement, ReliefWeb disasters, GDELT media tone, and Cloudflare Radar Internet outages.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: intelligence
  display-name: CountryRiskAssessmentSkill
allowed-tools: acledGetCountrySummary acledGetCastForecast reliefwebSearchDisasters gdeltGetTimeline cloudflareRadarGetOutages unhcrGetDisplacementStats storeBriefEntry searchMemory saveMemory
tools: [acledGetCountrySummary, acledGetCastForecast, reliefwebSearchDisasters, gdeltGetTimeline, cloudflareRadarGetOutages, unhcrGetDisplacementStats, storeBriefEntry, searchMemory, saveMemory]
properties: [nadia.prop.acled.email, nadia.prop.acled.password, nadia.prop.reliefweb.appname, nadia.prop.cloudflare.radar.apiToken]
---

# Country Risk Assessment Skill

Generates an executive Country Instability Index (CII) and multi-domain risk brief for any country by fusing conflict telemetry, humanitarian emergency status, media sentiment, forced displacement, and digital connectivity disruptions.

---

## Setup Instructions

### Required Plugins & Properties
Install the corresponding MCP plugins in **Settings ➔ Plugins** and configure their keys in **Settings ➔ Properties** (`~/.nadia/nadia.properties`):
- **ACLED (`acled-mcp`)**: `nadia.prop.acled.email` + `nadia.prop.acled.password` (or `nadia.prop.acled.apiKey`).
- **ReliefWeb (`reliefweb-mcp`)**: `nadia.prop.reliefweb.appname` (free registered appname from ReliefWeb).
- **Cloudflare Radar (`cloudflare-radar-mcp`)**: `nadia.prop.cloudflare.radar.apiToken` (Radar:Read token).
- **GDELT (`gdelt-mcp`)** & **UNHCR (`ucdp-displacement-mcp`)**: Work keyless out-of-the-box.

---

## Operational Workflow

1. **Conflict & Forecast Baseline**:
   - Call `acledGetCountrySummary` for the last 30–90 days and `acledGetCastForecast` to gauge violence trajectory, fatalities, and top actors.
2. **Humanitarian & Displacement Pressure**:
   - Call `reliefwebSearchDisasters` (status `current`) and `unhcrGetDisplacementStats` (using the country's ISO-3 code).
3. **Information & Infrastructure Signals**:
   - Call `gdeltGetTimeline` (`mode: "timelinetone"`, `timespan: "30d"`) to track media tone shifts and `cloudflareRadarGetOutages` (ISO-2 country code) for telecom/Internet disruptions.
4. **Synthesis & Delivery**:
   - Assign a qualitative risk tier (**Low / Moderate / Elevated / High / Critical**) with a 1–100 composite score, summarize top 3 escalation drivers, and archive significant changes via `storeBriefEntry`.
