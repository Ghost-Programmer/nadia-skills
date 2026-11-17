---
name: sec-filings
description: Queries SEC EDGAR corporate filings (10-K, 10-Q, 8-K, Form 4 insider transactions, 13F institutional holdings) and XBRL company financial facts by ticker or CIK.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: finance
  display-name: SecFilingsSkill
allowed-tools: executeSessionCommand storeBriefEntry searchMemory saveMemory getNadiaProperty setNadiaProperty
tools: [executeSessionCommand, storeBriefEntry, searchMemory, saveMemory, getNadiaProperty, setNadiaProperty]
properties: [nadia.prop.sec.userAgent, nadia.prop.arkleon.apiKey]
---

# SEC EDGAR Corporate Filings & Fundamentals Skill

This skill enables the cognitive agent (`@Stock Broker`, `@Researcher`, `@Product Manager`) to query official US Securities and Exchange Commission (**[SEC EDGAR](https://www.sec.gov/edgar/sec-api-documentation)**) corporate submissions (`10-K` annual reports, `10-Q` quarterly reports, `8-K` material event disclosures, `Form 4` insider trades, and `13F-HR` institutional holdings) and standardized XBRL financial facts.

---

## Setup Instructions

### External App & Integration Setup

- **Python 3.10+ Runtime**:
  - Install Python 3.10+ and ensure `python` is on system `PATH`:
    - **Windows**: `winget install Python.Python.3.12` (enable *"Add python.exe to PATH"*)
    - **macOS**: `brew install python`
    - **Linux**: `sudo apt install python3`
  - Uses Python's built-in standard library only (no `pip install` packages required).
- **SEC EDGAR Fair-Access User-Agent (`nadia.prop.sec.userAgent` — Required)**:
  - Per [SEC EDGAR Developer Guidelines](https://www.sec.gov/os/webmaster-faq#developers), all automated requests to `data.sec.gov` must declare a contact `User-Agent` in the format `CompanyOrAppName ContactEmail@domain.com`.
  - In Nadia, open **⚙️ System Settings ➔ Properties** and set:
    ```properties
    nadia.prop.sec.userAgent=MyCompanyName admin@mycompany.com
    ```
- **Arkleon API Key (`nadia.prop.arkleon.apiKey` — Optional)**:
  - If querying Arkleon structured financial endpoints, set `nadia.prop.arkleon.apiKey` in **⚙️ System Settings ➔ Properties**.
- **Bundled Script**: `~/.nadia/skills/finance/sec-filings/scripts/sec_edgar.py`.

---

## 1. Core Operational Workflows

### 1.1 Looking Up Recent SEC Filings for a Ticker (`filings`)
Resolves a company ticker (e.g., `AAPL`, `NVDA`, `MSFT`) to its 10-digit SEC CIK and lists recent filings, optionally filtered by form type (`10-K`, `10-Q`, `8-K`, `4`):

```bash
python ~/.nadia/skills/finance/sec-filings/scripts/sec_edgar.py filings --ticker "NVDA" --form "10-K,10-Q,8-K" --limit 15
```

### 1.2 Fetching Standardized Company XBRL Financial Facts (`facts`)
Retrieve historical GAAP revenue, net income, assets, or EPS reported in SEC XBRL filings:

```bash
python ~/.nadia/skills/finance/sec-filings/scripts/sec_edgar.py facts --ticker "AAPL" --concept "Revenues" --limit 8
```

- Common GAAP concepts: `Revenues`, `NetIncomeLoss`, `Assets`, `Liabilities`, `OperatingIncomeLoss`, `EarningsPerShareDiluted`, `CashAndCash EquivalentsAtCarryingValue`.

---

## 2. Presentation Guidelines

1. Present SEC filings in a Markdown table with columns: `Form`, `Filing Date`, `Report Period`, `Accession Number`, `Description`, and direct clickable `SEC Document URL`.
2. When summarizing `10-K` or `10-Q` metrics for `@Stock Broker`, include both YoY and QoQ comparisons.
