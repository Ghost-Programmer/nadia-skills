---
name: cyber-threat-briefing
description: Synthesizes an executive cyber threat intelligence briefing by correlating CISA KEV & Advisories, EuRepoC cyber incidents, NIST NVD CVEs, Cloudflare Radar L3/L7 DDoS & BGP events, and IOC lookups (AbuseIPDB, OTX, URLhaus).
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: security
  display-name: CyberThreatBriefingSkill
allowed-tools: cisaSearchKev cisaGetKevByCve cisaGetAdvisories eurepocSearchIncidents nvdGetCve abuseIpCheck otxGetIndicator urlhausLookup cloudflareRadarGetLayer7Attacks cloudflareRadarGetBgpEvents storeBriefEntry
tools: [cisaSearchKev, cisaGetKevByCve, cisaGetAdvisories, eurepocSearchIncidents, nvdGetCve, abuseIpCheck, otxGetIndicator, urlhausLookup, cloudflareRadarGetLayer7Attacks, cloudflareRadarGetBgpEvents, storeBriefEntry]
properties: [nadia.prop.cloudflare.radar.apiToken]
---

# Cyber Threat Briefing Skill

Produces actionable cybersecurity threat reports, vulnerability prioritization lists, and incident attribution summaries for security teams.

---

## Setup Instructions

- **Keyless out-of-the-box**: `cisa-kev-mcp`, `eurepoc-mcp`, `nvdGetCve`, and `urlhausLookup`.
- **Optional keys in Settings ➔ Properties**: `nadia.prop.cloudflare.radar.apiToken`, `nadia.prop.nvd.apiKey`, `nadia.prop.abuseipdb.apiKey`, `nadia.prop.otx.apiKey`.

---

## Operational Workflow

1. **Active Exploitation & Patching**: Call `cisaSearchKev` (`ransomwareOnly` or `addedSince`) and `cisaGetAdvisories` (`feedType: "all"`). Enrich high-priority CVEs with `nvdGetCve`.
2. **Geopolitical Cyber Incidents**: Query `eurepocSearchIncidents` by target country, sector, or initiator.
3. **Network & Infrastructure Threats**: Call `cloudflareRadarGetLayer7Attacks` and `cloudflareRadarGetBgpEvents` (`hijacks` / `leaks`).
4. **IOC Enrichment**: When IPs, domains, or URLs are supplied, run `abuseIpCheck`, `otxGetIndicator`, and `urlhausLookup`.
5. **Deliverable**: Provide a prioritized remediation table (CVE, Vendor/Product, Due Date, Ransomware Flag, Action) and archive critical alerts via `storeBriefEntry`.
