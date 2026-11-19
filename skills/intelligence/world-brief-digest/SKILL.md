---
name: world-brief-digest
description: Produces a daily executive global situational awareness brief across geopolitics, cyber threats, humanitarian crises, natural hazards, maritime chokepoints, and prediction markets, archiving the digest in Nadia Briefs.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: intelligence
  display-name: WorldBriefDigestSkill
allowed-tools: cisaGetKevSummary cisaGetAdvisories cloudflareRadarGetOutages reliefwebSearchDisasters eonetSearchNaturalEvents gdeltSearchArticles polymarketSearchMarkets maritimeGetDisruptions whoGetOutbreakNews storeBriefEntry
tools: [cisaGetKevSummary, cisaGetAdvisories, cloudflareRadarGetOutages, reliefwebSearchDisasters, eonetSearchNaturalEvents, gdeltSearchArticles, polymarketSearchMarkets, maritimeGetDisruptions, whoGetOutbreakNews, storeBriefEntry]
properties: []
---

# World Brief Digest Skill

Compiles a concise, multi-domain daily executive intelligence brief suitable for scheduled cron execution or on-demand morning briefings.

---

## Setup Instructions

- Most data sources (`cisa-kev-mcp`, `gdelt-mcp`, `nasa-firms-mcp` EONET, `polymarket-mcp`, `radiation-health-mcp`, `maritime-chokepoint-mcp`) work **keyless** immediately after installing the plugins.
- Optionally configure `nadia.prop.cloudflare.radar.apiToken` and `nadia.prop.reliefweb.appname` in **Settings ➔ Properties** for enriched outage and humanitarian sections.

---

## Operational Workflow

1. **Cyber & Telecom**: Call `cisaGetKevSummary` + `cisaGetAdvisories` (`limit: 5`) + `cloudflareRadarGetOutages` (`dateRange: "1d"`).
2. **Natural Hazards & Health**: Call `eonetSearchNaturalEvents` (`days: 7`, `limit: 8`) + `whoGetOutbreakNews` (`limit: 5`) + `reliefwebSearchDisasters` (`status: "current"`, `limit: 5`).
3. **Geopolitics, Maritime & Markets**: Call `maritimeGetDisruptions` (`limit: 5`) + `polymarketSearchMarkets` (`limit: 8`) + `gdeltSearchArticles` (`timespan: "24h"`, `maxRecords: 10`).
4. **Publish**: Format into a crisp 5-section executive brief (Top Signals, Cyber/Infra, Humanitarian/Hazards, Maritime/Supply Chain, Market Odds) and persist via `storeBriefEntry`.
