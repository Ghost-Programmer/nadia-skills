---
name: chokepoint-supply-chain-monitor
description: Monitors strategic global maritime chokepoints (Hormuz, Bab el-Mandeb, Suez, Malacca, Panama, Turkish Straits, Taiwan Strait, Danish Straits) by combining NGA maritime warnings, ACLED coastal conflict, sanctions vessel screening, and GDELT shipping news.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: geo
  display-name: ChokepointSupplyChainMonitorSkill
allowed-tools: maritimeListChokepoints maritimeGetDisruptions acledSearchEvents sanctionsCheckVesselOrAircraft gdeltSearchArticles storeBriefEntry
tools: [maritimeListChokepoints, maritimeGetDisruptions, acledSearchEvents, sanctionsCheckVesselOrAircraft, gdeltSearchArticles, storeBriefEntry]
properties: []
---

# Chokepoint & Supply Chain Monitor Skill

Monitors maritime trade bottlenecks, naval security warnings, and vessel disruption risks across the world's critical sea lanes.

---

## Setup Instructions

- **Keyless out-of-the-box**: `maritime-chokepoint-mcp` (NGA MSI Broadcast Warnings + chokepoint registry), `sanctions-mcp` (OFAC SDN fallback), and `gdelt-mcp`.
- **Optional keys**: `nadia.prop.acled.email`/`password` for coastal conflict overlay, `nadia.prop.opensanctions.apiKey` for global vessel sanctions screening.

---

## Operational Workflow

1. **Chokepoint Baseline**: Call `maritimeListChokepoints` to retrieve bounding boxes, NAVAREAs, and trade share.
2. **Navigational & Security Alerts**: Call `maritimeGetDisruptions` for the target chokepoint (e.g., `hormuz`, `bab-el-mandeb`, `suez`, `malacca`, `panama`).
3. **Threat & Vessel Correlation**: Check `gdeltSearchArticles` (`query: "<chokepoint> shipping OR tanker OR blockade"`) and `acledSearchEvents` for littoral conflict; screen flagged vessels via `sanctionsCheckVesselOrAircraft`.
4. **Risk Briefing**: Report Chokepoint Status (**Normal / Elevated / Disrupted / Critical**), active NGA warnings, rerouting impacts, and supply-chain exposure.
