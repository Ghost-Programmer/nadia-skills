---
name: energy-shock-assessment
description: Evaluates global oil, gas, and electricity supply shocks by combining U.S. EIA price/inventory series, GIE AGSI+ EU gas storage, ENTSO-E grid load, maritime chokepoint disruptions, and Polymarket energy odds.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: finance
  display-name: EnergyShockAssessmentSkill
allowed-tools: eiaGetEnergySeries gieGetEuGasStorage entsoeGetGridLoad maritimeGetDisruptions polymarketSearchMarkets gdeltSearchArticles fredGetSeries storeBriefEntry
tools: [eiaGetEnergySeries, gieGetEuGasStorage, entsoeGetGridLoad, maritimeGetDisruptions, polymarketSearchMarkets, gdeltSearchArticles, fredGetSeries, storeBriefEntry]
properties: [nadia.prop.eia.apiKey, nadia.prop.gie.apiKey]
---

# Energy Shock Assessment Skill

Assesses geopolitical and infrastructure shocks to oil, LNG, natural gas storage, and electrical grids, quantifying macro-inflationary spillover.

---

## Setup Instructions

- Configure free API keys in **Settings ➔ Properties**:
  - `nadia.prop.eia.apiKey` (`energy-grid-mcp`) — U.S. EIA Open Data.
  - `nadia.prop.gie.apiKey` (`energy-grid-mcp`) — GIE AGSI+ EU gas storage.
  - Optional: `nadia.prop.entsoe.token` (EU power grid), `nadia.prop.fred.apiKey` (`macro-trade-mcp`).
- `maritimeGetDisruptions`, `polymarketSearchMarkets`, and `gdeltSearchArticles` work keyless.

---

## Operational Workflow

1. **Supply & Inventory Telemetry**: Query `eiaGetEnergySeries` (`petroleum/pri/spt/data` or `natural-gas/stor/wkly/data`) and `gieGetEuGasStorage` (`country: "EU"` or `"DE"`).
2. **Transit & Geopolitical Triggers**: Check `maritimeGetDisruptions` (`hormuz` / `bab-el-mandeb` / `suez`) and `gdeltSearchArticles` (`query: "oil supply OR LNG OR pipeline disruption"`).
3. **Market Expectations**: Query `polymarketSearchMarkets` (`query: "oil"` or `"OPEC"`) and `fredGetSeries` (`CPIAUCSL` / `DCOILWTICO`).
4. **Deliverable**: Provide an Energy Shock Scorecard (Supply Risk, Storage Buffer, Price Impact, Grid Stress, Macro Spillover).
