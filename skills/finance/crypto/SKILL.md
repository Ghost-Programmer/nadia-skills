---
name: crypto
description: Queries real-time cryptocurrency spot prices, 24-hour market changes, market capitalizations, trending coins, and historical price charts using the CoinGecko API.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: finance
  display-name: CryptoSkill
allowed-tools: executeSessionCommand storeBriefEntry searchMemory saveMemory getNadiaProperty setNadiaProperty
tools: [executeSessionCommand, storeBriefEntry, searchMemory, saveMemory, getNadiaProperty, setNadiaProperty]
properties: [nadia.prop.coingecko.apiKey]
---

# Cryptocurrency & Digital Assets Skill (`CoinGecko`)

This skill instructs the cognitive agent (`@Stock Broker`, `@Researcher`) on how to query real-time cryptocurrency prices, 24-hour volume and percentage changes, global market cap rankings, trending tokens, and historical market charts via the **[CoinGecko API](https://www.coingecko.com/en/api)**.

---

## Setup Instructions

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/finance/crypto/scripts/crypto_api.py`.
- **Configuration Properties (`nadia.prop.*`)**:
  - Works out-of-the-box without an API key using CoinGecko's public endpoints.
  - Optional: Configure `nadia.prop.coingecko.apiKey` in `~/.nadia/nadia.properties` (via **Settings ➔ Properties** or `setNadiaProperty`) for higher Demo/Pro rate limits. The script automatically reads `nadia.prop.coingecko.apiKey` from `~/.nadia/nadia.properties` when present.

---

## 1. Core Operational Workflows

### 1.1 Fetching Top Cryptocurrencies & Live Quotes (`markets`)
Retrieve top cryptocurrencies by market cap with live price, 24h high/low, 24h change %, and market capitalization:

```bash
python ~/.nadia/skills/finance/crypto/scripts/crypto_api.py markets --currency "usd" --limit 15
```

- Filter by specific coin IDs (comma-separated, e.g. `bitcoin,ethereum,solana`):
  ```bash
  python ~/.nadia/skills/finance/crypto/scripts/crypto_api.py markets --ids "bitcoin,ethereum,solana" --currency "usd"
  ```

### 1.2 Resolving a Coin Name or Symbol (`search`)
When the user mentions a token ticker or name and you need its canonical CoinGecko ID:

```bash
python ~/.nadia/skills/finance/crypto/scripts/crypto_api.py search --query "solana"
```

### 1.3 Fetching Trending Coins (`trending`)
Discover the top trending cryptocurrencies searched over the last 24 hours:

```bash
python ~/.nadia/skills/finance/crypto/scripts/crypto_api.py trending
```

### 1.4 Historical Price Chart (`history`)
Fetch daily historical prices over the past `N` days for a coin ID:

```bash
python ~/.nadia/skills/finance/crypto/scripts/crypto_api.py history --id "bitcoin" --days 14 --currency "usd"
```

---

## 2. Presentation Guidelines

1. Always present cryptocurrency quotes in a clean Markdown table with columns: `Rank`, `Asset (Symbol)`, `Price (USD)`, `24h Change (%)`, `24h High / Low`, `Market Cap`, and `24h Volume`.
2. When invoked by `@Stock Broker` during market sweeps, store significant crypto market movements in `BriefService` (`storeBriefEntry`) under category `"finance"`.

