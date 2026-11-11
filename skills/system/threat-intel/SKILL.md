---
name: threat-intel
description: Performs cybersecurity threat intelligence lookups including IP abuse reputation (AbuseIPDB), internet-facing host/port exposure (Shodan), domain/file/URL reputation (VirusTotal), and malware URL feeds (URLhaus).
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: system
  display-name: ThreatIntelSkill
allowed-tools: executeSessionCommand storeBriefEntry searchMemory saveMemory getNadiaProperty setNadiaProperty
tools: [executeSessionCommand, storeBriefEntry, searchMemory, saveMemory, getNadiaProperty, setNadiaProperty]
properties: [nadia.prop.abuseipdb.apiKey, nadia.prop.shodan.apiKey, nadia.prop.virustotal.apiKey]
---

# Cybersecurity Threat Intelligence Skill (`AbuseIPDB`, `Shodan`, `VirusTotal` & `URLhaus`)

This skill empowers `@Network Engineer` and `@Software Architect` to investigate suspicious IP addresses, check open internet-facing ports and vulnerabilities on external hosts, verify domain/file/URL malware reputations, and query active malware distribution URLs.

---

## Setup Instructions

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/system/threat-intel/scripts/threat_intel.py`.
- **Configuration Properties (`nadia.prop.*`)**:
  - `nadia.prop.abuseipdb.apiKey`: API key for **[AbuseIPDB](https://docs.abuseipdb.com/)**.
  - `nadia.prop.shodan.apiKey`: API key for **[Shodan](https://developer.shodan.io/)**.
  - `nadia.prop.virustotal.apiKey`: API key for **[VirusTotal v3](https://docs.virustotal.com/reference/overview)**.

---

## 1. Core Operational Workflows

### 1.1 Checking IP Reputation via AbuseIPDB (`abuseipdb`)
Check abuse confidence score (0–100%), ISP, country, usage type, and total abuse reports for an IPv4/IPv6 address:

```bash
python ~/.nadia/skills/system/threat-intel/scripts/threat_intel.py abuseipdb --ip "1.1.1.1" --days 90
```

### 1.2 Inspecting Host Port & CVE Exposure via Shodan (`shodan`)
Inspect open ports, banners, ASN, organization, and known CVEs for an external IP:

```bash
python ~/.nadia/skills/system/threat-intel/scripts/threat_intel.py shodan --ip "8.8.8.8"
```

### 1.3 Checking Domain, IP, or File Hash via VirusTotal (`virustotal`)
Query multi-engine antivirus and threat intelligence verdicts for a domain, IP, or SHA-256 hash:

```bash
python ~/.nadia/skills/system/threat-intel/scripts/threat_intel.py virustotal --type "domains" --target "example.com"
```

- Supported `--type` values: `ip_addresses`, `domains`, `files` (pass SHA-256 hash as `--target`).

