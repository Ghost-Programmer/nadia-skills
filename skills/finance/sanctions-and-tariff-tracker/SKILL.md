---
name: sanctions-and-tariff-tracker
description: Tracks sanctions designations, shadow-fleet vessels/aircraft, bilateral tariffs, and macroeconomic trade impacts using OpenSanctions/OFAC SDN, WTO Timeseries, IMF indicators, FRED, and GDELT.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: finance
  display-name: SanctionsAndTariffTrackerSkill
allowed-tools: sanctionsSearchEntity sanctionsCheckVesselOrAircraft wtoGetTariffs imfGetIndicator fredGetSeries gdeltSearchArticles polymarketSearchMarkets storeBriefEntry
tools: [sanctionsSearchEntity, sanctionsCheckVesselOrAircraft, wtoGetTariffs, imfGetIndicator, fredGetSeries, gdeltSearchArticles, polymarketSearchMarkets, storeBriefEntry]
properties: []
---

# Sanctions & Tariff Tracker Skill

Screens entities, vessels, and aircraft against sanctions lists and analyzes tariff regimes, trade-flow shifts, and macroeconomic impacts.

---

## Setup Instructions

- **Keyless out-of-the-box**: `sanctions-mcp` (U.S. Treasury OFAC SDN fallback), `imfGetIndicator`, `gdeltSearchArticles`, and `polymarketSearchMarkets`.
- **Optional keys in Settings ➔ Properties**:
  - `nadia.prop.opensanctions.apiKey` for multi-jurisdiction EU/UN/UK/US sanctions & PEP screening.
  - `nadia.prop.wto.apiKey` for WTO Timeseries tariff/trade queries.
  - `nadia.prop.fred.apiKey` for U.S. macro & trade balance series.

---

## Operational Workflow

1. **Entity & Asset Screening**: Run `sanctionsSearchEntity` for individuals/companies or `sanctionsCheckVesselOrAircraft` for IMO/tail numbers.
2. **Tariff & Macro Exposure**: Query `wtoGetTariffs` (e.g., `TP_A_0010`) and `imfGetIndicator` (`NGDP_RPCH`, `PCPIPCH`) for affected countries.
3. **Policy & Market Signals**: Check `gdeltSearchArticles` (`query: "sanctions OR tariff"`) and `polymarketSearchMarkets` (`query: "tariff"`).
4. **Deliverable**: Present a structured compliance & trade impact report listing matched designations, tariff rates, and macro exposure.
