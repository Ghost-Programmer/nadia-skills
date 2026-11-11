---
name: forex
description: Retrieves real-time and historical foreign exchange (FX) rates and performs currency conversions across 150+ fiat and digital currencies using the open Currency-API.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: finance
  display-name: ForexSkill
allowed-tools: executeSessionCommand storeBriefEntry searchMemory saveMemory
tools: [executeSessionCommand, storeBriefEntry, searchMemory, saveMemory]
properties: []
---

# Foreign Exchange & Currency Conversion Skill (`Currency-API`)

This skill enables the cognitive agent (`@Stock Broker`, `@Personal Assistant`, `@Researcher`) to fetch daily foreign exchange rates across 150+ world currencies and perform exact currency conversions using the keyless, rate-limit-free **[Currency-API](https://github.com/fawazahmed0/currency-api)**.

---

## Setup Instructions

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/finance/forex/scripts/forex_api.py`.
- **Network Access**: Outbound HTTPS access to `https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest` (with automatic failover to `https://latest.currency-api.pages.dev`).
- **Configuration Properties (`nadia.prop.*`)**: Keyless (`properties: []`).

---

## 1. Core Operational Workflows

### 1.1 Converting Between Currencies (`convert`)
Convert any numeric amount from a base currency (`--from`) to one or more target currencies (`--to`, comma-separated):

```bash
python ~/.nadia/skills/finance/forex/scripts/forex_api.py convert --from "USD" --to "EUR,GBP,JPY,CAD,CHF" --amount 1000
```

- **Historical Date Conversion** (optional `--date YYYY-MM-DD`):
  ```bash
  python ~/.nadia/skills/finance/forex/scripts/forex_api.py convert --from "USD" --to "EUR,GBP" --amount 500 --date "2025-01-15"
  ```

### 1.2 Listing Exchange Rates for a Base Currency (`rates`)
Retrieve major exchange rates for a base currency:

```bash
python ~/.nadia/skills/finance/forex/scripts/forex_api.py rates --base "USD" --targets "EUR,GBP,JPY,CAD,AUD,CHF,CNY,INR,MXN,BRL"
```

### 1.3 Searching Available Currency Codes (`currencies`)
Search the 150+ supported ISO currency codes by country or currency name:

```bash
python ~/.nadia/skills/finance/forex/scripts/forex_api.py currencies --search "franc"
```

---

## 2. Presentation Guidelines

1. Present foreign exchange tables with columns: `Base Currency`, `Target Currency`, `Exchange Rate`, `Converted Amount`, and `Rate Date`.
2. Always include at least 4 decimal places for FX exchange rates and 2 decimal places for converted fiat amounts.

