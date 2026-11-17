---
name: macro-economics
description: Queries macroeconomic indicators including CPI inflation, Federal Funds interest rates, GDP, Treasury yields, and unemployment statistics from FRED (Federal Reserve Economic Data) and the US Bureau of Labor Statistics (BLS).
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
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

### External App & Integration Setup

- **Python 3.10+ Runtime**:
  - Install Python 3.10+ and ensure `python` is on system `PATH`:
    - **Windows**: `winget install Python.Python.3.12` (enable *"Add python.exe to PATH"*)
    - **macOS**: `brew install python`
    - **Linux**: `sudo apt install python3`
  - Uses Python's built-in standard library only (no `pip install` packages required).
- **FRED API Key Setup (`nadia.prop.fred.apiKey`)**:
  1. Register for a free account at [Federal Reserve Bank of St. Louis (FRED)](https://fredaccount.stlouisfed.org/apikeys) and click **Request API Key**.
  2. In Nadia, open **⚙️ System Settings ➔ Properties** (or call `setNadiaProperty`) and set:
     ```properties
     nadia.prop.fred.apiKey=your_32_character_fred_api_key
     ```
  3. US Bureau of Labor Statistics (BLS) public v1 series work without an API key.
- **Bundled Script**: `~/.nadia/skills/finance/macro-economics/scripts/macro_economics.py`.

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
