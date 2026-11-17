---
name: stocks
description: Guidelines and Python CLI references for searching ticker symbols, fetching latest quotes, pulling historical stock prices, and tracking company watchlist preferences in RAG memory.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: finance
  display-name: FinanceSkill
allowed-tools: executeSessionCommand searchMemory saveMemory
tools: [executeSessionCommand, searchMemory, saveMemory]
---

# Finance & Stock Market Skill (Python CLI)

This skill instructs the agent on how to look up financial data, retrieve ticker symbols, get latest quotes, pull historical prices using the Yahoo Finance API, and persist user company interests in long-term RAG memory.

The finance service is implemented as a Python script located at `~/.nadia/skills/finance/stocks/scripts/finance_api.py`.

---

## Setup Instructions

### External App & Integration Setup

- **Python 3.10+ Runtime**:
  - Install Python 3.10+ and ensure `python` is on system `PATH`:
    - **Windows**: `winget install Python.Python.3.12` (enable *"Add python.exe to PATH"*)
    - **macOS**: `brew install python`
    - **Linux**: `sudo apt install python3`
  - Uses Python's built-in standard library only (no `pip install` packages required).
- **Yahoo Finance Market Data (Keyless)**:
  - Requires outbound HTTPS access to Yahoo Finance query endpoints (`https://query1.finance.yahoo.com`). No API key is required for standard quote, search, and historical OHLCV lookups.
- **Bundled Script**: `~/.nadia/skills/finance/stocks/scripts/finance_api.py`.

---

## Operational Workflow

When the user requests stock prices, market quotes, or historical financial charts for a company or fund name (instead of providing a direct ticker symbol like AAPL or MSFT):

1. **Step 1: Resolve the Ticker Symbol**: First run the `resolve` command to find the correct ticker symbol:

   ```bash
   python .~/.nadia/skills/finance/stocks/scripts/finance_api.py resolve --company "<company_name>"
   ```

2. **Step 2: Fetch the Price or Chart Data**: Immediately use the resolved ticker symbol to fetch the actual financial data:
   - For current prices/quotes, run `latest`:

     ```bash
     python .~/.nadia/skills/finance/stocks/scripts/finance_api.py latest --symbol "<resolved_symbol>"
     ```

   - For historical prices/charts, run `historical`:

     ```bash
     python .~/.nadia/skills/finance/stocks/scripts/finance_api.py historical --symbol "<resolved_symbol>" --start "<start_date>" --end "<end_date>"
     ```

3. **Step 3: Present the Results**: Display the resolved symbol, company name, latest price, change, volume, or historical table to the user. **Do not stop or return after only resolving the ticker symbol.**

## Execution Pattern

Call the `run_command` tool to run the finance Python script.

### 1. Resolve Company Name to Ticker Symbol

Finds the closest matching ticker symbol and full company name for a search query.

```bash
python .~/.nadia/skills/finance/stocks/scripts/finance_api.py resolve --company "[company_name]"
```

*Example:*

```bash
python .~/.nadia/skills/finance/stocks/scripts/finance_api.py resolve --company "Apple"
```

*Response JSON returned:*

```json
{
  "symbol": "AAPL",
  "company": "Apple Inc."
}
```

### 2. Fetch Latest Stock Quote

Gets the most recent trading price, change, previous close, high/low, and daily volume.

```bash
python .~/.nadia/skills/finance/stocks/scripts/finance_api.py latest --symbol "[ticker_symbol]"
```

*Example:*

```bash
python .~/.nadia/skills/finance/stocks/scripts/finance_api.py latest --symbol "AAPL"
```

*Response JSON returned:*

```json
{
  "symbol": "AAPL",
  "company": "Apple Inc.",
  "currency": "USD",
  "price": 308.465,
  "previous_close": 316.83,
  "change": -8.365,
  "change_percent": -2.64,
  "high": 312.38,
  "low": 307.68,
  "volume": 6960131,
  "market_time": "2026-08-21T13:15:00",
  "timezone": "America/New_York",
  "api_url": "https://query1.finance.yahoo.com/v8/finance/chart/AAPL?range=1d"
}
```

### 3. Fetch Historical Stock Price Data

Pulls daily historical quotes (Open, High, Low, Close, Adjusted Close, Volume) over a specific date range.

```bash
python .~/.nadia/skills/finance/stocks/scripts/finance_api.py historical --symbol "[ticker_symbol]" --start "[YYYY-MM-DD]" --end "[YYYY-MM-DD]"
```

*Example:*

```bash
python .~/.nadia/skills/finance/stocks/scripts/finance_api.py historical --symbol "AAPL" --start "2026-08-01" --end "2026-08-20"
```

*Response JSON returned:*

```json
{
  "symbol": "AAPL",
  "company": "Apple Inc.",
  "currency": "USD",
  "timezone": "America/New_York",
  "quotes": [
    {
      "date": "2026-08-03",
      "open": 315.2,
      "high": 318.4,
      "low": 312.1,
      "close": 316.5,
      "adj_close": 316.5,
      "volume": 32104000
    }
  ],
  "api_url": "https://query1.finance.yahoo.com/v8/finance/chart/AAPL?period1=...&period2=...&interval=1d"
}
```
