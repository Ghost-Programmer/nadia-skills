---
name: internet-outage-investigator
description: Diagnoses regional Internet blackouts, subsea cable cuts, BGP hijacks/leaks, and government-mandated shutdowns by correlating Cloudflare Radar outages, traffic anomalies, BGP events, and GDELT news coverage.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: security
  display-name: InternetOutageInvestigatorSkill
allowed-tools: cloudflareRadarGetOutages cloudflareRadarGetTrafficAnomalies cloudflareRadarGetBgpEvents gdeltSearchArticles factCheckSearchClaims storeBriefEntry
tools: [cloudflareRadarGetOutages, cloudflareRadarGetTrafficAnomalies, cloudflareRadarGetBgpEvents, gdeltSearchArticles, factCheckSearchClaims, storeBriefEntry]
properties: [nadia.prop.cloudflare.radar.apiToken]
---

# Internet Outage Investigator Skill

Investigates suspected regional Internet disruptions, ASN blackouts, subsea cable faults, and BGP routing incidents with corroborated telemetry and open-source news.

---

## Setup Instructions

- **Cloudflare Radar (`cloudflare-radar-mcp`)**: Configure `nadia.prop.cloudflare.radar.apiToken` (Radar:Read permission) in **Settings ➔ Properties**.
- **GDELT (`gdelt-mcp`)**: Keyless out-of-the-box.
- **Fact Check (`factcheck-mcp`)**: Optional `nadia.prop.google.factcheck.apiKey` to verify viral shutdown claims.

---

## Operational Workflow

1. **Outage & Traffic Telemetry**: Call `cloudflareRadarGetOutages` and `cloudflareRadarGetTrafficAnomalies` filtered by country ISO-2 code or ASN.
2. **Routing Diagnostics**: Call `cloudflareRadarGetBgpEvents` (`eventType: "hijacks"` and `"leaks"`) to check for BGP route hijacks or leaks.
3. **Corroboration**: Query `gdeltSearchArticles` (`query: "<country> internet outage OR cable cut OR blackout"`, `timespan: "7d"`) and optionally `factCheckSearchClaims`.
4. **Assessment**: Classify probable root cause (Power Grid Failure, Subsea/Terrestrial Cable Cut, BGP Misconfiguration/Hijack, DDoS, or Government Shutdown) with timeline and affected ASNs.
