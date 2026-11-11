---
name: macro-economics
description: Queries macroeconomic indicators including CPI inflation, Federal Funds interest rates, GDP, Treasury yields, and unemployment statistics from FRED (Federal Reserve Economic Data) and the US Bureau of Labor Statistics (BLS).
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: finance
  display-name: MacroEconomicsSkill
allowed-tools: executeSessionCommand storeBriefEntry searchMemory saveMemory getNadiaProperty setNadiaProperty
tools: [executeSessionCommand, storeBriefEntry, searchMemory, saveMemory, getNadiaProperty, setNadiaProperty]
properties: [nadia.prop.fred.apiKey]
---

# Macroeconomics & Central Bank Indicators Skill (`FRED` & `BLS`)

This skill equips the cognitive agent (`@Stock Broker`, `@Product Manager`, `@Researcher`) to retrieve authoritative US and global macroeconomic time series—including Consumer Price Index (CPI), Federal Funds Effective Rate (`FEDFUNDS`), Real GDP (`GDPC1`), 10-Year Treasury Constant Maturity (`DGS10`), and Civilian Unemployment Rate (`UNRATE`)—using the **[Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/docs/api/fred/)** API and the **[US Bureau of Labor Statistics (BLS)](https://www.bls.gov/developers/)** Public Data API.

---

## Setup Instructions

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/finance/macro-economics/scripts/macro_economics.py`.
- **Configuration Properties (`nadia.prop.*`)**:
  - Requires `nadia.prop.fred.apiKey` in `~/.nadia/nadia.properties` (configure via **Settings ➔ Properties** or `setNadiaProperty`).

---

## 1. Core Operational Workflows

### 1.1 Fetching a Macroeconomic Series from FRED (`series`)
Retrieve recent observations for any FRED series ID (e.g., `FEDFUNDS`, `CPIAUCSL`, `UNRATE`, `GDPC1`, `DGS10`, `T10Y2Y`, `MORTGAGE30US`):

```bash
python ~/.nadia/skills/finance/macro-economics/scripts/macro_economics.py series --id "FEDFUNDS" --limit 12
```

### 1.2 Searching FRED Economic Data Series (`search`)
Find FRED series IDs matching an economic topic or keyword:

```bash
python ~/.nadia/skills/finance/macro-economics/scripts/macro_economics.py search --query "consumer price index" --limit 10
```

### 1.3 Fetching Key Macro Dashboard Snapshot (`snapshot`)
Pull the latest values for the core macroeconomic dashboard (`FEDFUNDS`, `CPIAUCSL`, `UNRATE`, `DGS10`, `T10Y2Y`, `GDPC1`):

```bash
python ~/.nadia/skills/finance/macro-economics/scripts/macro_economics.py snapshot
```

### 1.4 Fetching Bureau of Labor Statistics Series (`bls`)
Query BLS time series (e.g., `CUUR0000SA0` for US All Items CPI, `LNS14000000` for Unemployment Rate):

```bash
python ~/.nadia/skills/finance/macro-economics/scripts/macro_economics.py bls --series "CUUR0000SA0,LNS14000000" --start-year 2024 --end-year 2026
```

---

## 2. Presentation Guidelines

1. Present macroeconomic observations in a Markdown table with columns: `Series ID`, `Indicator Title`, `Latest Date`, `Value`, `Units / Frequency`, and `Prior Period Comparison`.
2. When assisting `@Stock Broker`, correlate yield curve spreads (`T10Y2Y`) and Fed rate shifts (`FEDFUNDS`) with equity sector performance.

