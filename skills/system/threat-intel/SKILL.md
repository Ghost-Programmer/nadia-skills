---
name: threat-intel
description: Performs cybersecurity threat intelligence lookups including IP abuse reputation (AbuseIPDB), internet-facing host/port exposure (Shodan), domain/file/URL reputation (VirusTotal), and malware URL feeds (URLhaus).
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
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

### External App & Integration Setup

- **Python 3.10+ Runtime**:
  - Install Python 3.10+ and ensure `python` is on system `PATH`:
    - **Windows**: `winget install Python.Python.3.12` (enable *"Add python.exe to PATH"*)
    - **macOS**: `brew install python`
    - **Linux**: `sudo apt install python3`
  - Uses Python's built-in standard library only (no `pip install` packages required).
- **Threat Intelligence API Keys (`nadia.prop.*`)**:
  - **URLhaus Malware Feed** (`abuse.ch`) works keyless out-of-the-box.
  - Configure one or more of the following in **⚙️ System Settings ➔ Properties** (`~/.nadia/nadia.properties`):
    1. **AbuseIPDB (`nadia.prop.abuseipdb.apiKey`)**: Create a free account at [AbuseIPDB](https://www.abuseipdb.com/register) and generate a key under *User Account ➔ API*.
    2. **Shodan (`nadia.prop.shodan.apiKey`)**: Register at [Shodan Account](https://account.shodan.io/) and copy the API key from your Account Overview page.
    3. **VirusTotal (`nadia.prop.virustotal.apiKey`)**: Sign up at [VirusTotal](https://www.virustotal.com/), click your profile avatar ➔ **API Key**, and copy your v3 API key.
- **Bundled Script**: `~/.nadia/skills/system/threat-intel/scripts/threat_intel.py`.

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
