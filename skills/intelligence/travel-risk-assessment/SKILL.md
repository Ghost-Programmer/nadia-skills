---
name: travel-risk-assessment
description: Generates an actionable traveler safety dossier for a destination country or city by combining ReliefWeb crises, ACLED local unrest, WHO disease outbreaks, Cloudflare connectivity status, and FAA/NOTAM aviation disruptions.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: intelligence
  display-name: TravelRiskAssessmentSkill
allowed-tools: acledSearchEvents reliefwebSearchDisasters reliefwebSearchCountries whoGetOutbreakNews cloudflareRadarGetOutages faaGetAirportDelays notamSearchByAirportOrFir gdeltSearchArticles storeBriefEntry
tools: [acledSearchEvents, reliefwebSearchDisasters, reliefwebSearchCountries, whoGetOutbreakNews, cloudflareRadarGetOutages, faaGetAirportDelays, notamSearchByAirportOrFir, gdeltSearchArticles, storeBriefEntry]
properties: [nadia.prop.acled.email, nadia.prop.acled.password, nadia.prop.reliefweb.appname]
---

# Travel Risk Assessment Skill

Builds an executive pre-travel safety and logistics dossier covering physical security, health advisories, natural hazards, digital connectivity, and airspace/airport status.

---

## Setup Instructions

- Configure `nadia.prop.acled.email` + `nadia.prop.acled.password` (`acled-mcp`) and `nadia.prop.reliefweb.appname` (`reliefweb-mcp`) in **Settings ➔ Properties**.
- Optional: `nadia.prop.cloudflare.radar.apiToken` (`cloudflare-radar-mcp`) and `nadia.prop.faa.notam.clientId`/`clientSecret` (`aviation-notam-mcp`).
- `whoGetOutbreakNews`, `faaGetAirportDelays`, and `gdeltSearchArticles` work keyless out-of-the-box.

---

## Operational Workflow

1. **Security & Civil Unrest**: Query `acledSearchEvents` (last 30 days) and `gdeltSearchArticles` for protests, crime spikes, or border closures at the destination.
2. **Health & Natural Hazards**: Query `whoGetOutbreakNews` and `reliefwebSearchDisasters` (`status: "current"`).
3. **Connectivity & Aviation**: Check `cloudflareRadarGetOutages` for the destination country and `faaGetAirportDelays` / `notamSearchByAirportOrFir` for departure/arrival hubs.
4. **Deliverable**: Present a Go / Exercise Caution / Reconsider / Do Not Travel summary with emergency contacts, regional no-go zones, and contingency guidance.
