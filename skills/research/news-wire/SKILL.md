---
name: news-wire
description: Queries breaking global news headlines, topic searches, and live technology/startup wire stories using HackerNews (keyless), NewsData.io, and GNews APIs.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: research
  display-name: NewsWireSkill
allowed-tools: executeSessionCommand storeBriefEntry searchMemory saveMemory getNadiaProperty setNadiaProperty
tools: [executeSessionCommand, storeBriefEntry, searchMemory, saveMemory, getNadiaProperty, setNadiaProperty]
properties: [nadia.prop.newsdata.apiKey, nadia.prop.gnews.apiKey]
---

# Breaking News & Tech Wire Skill (`HackerNews`, `NewsData.io` & `GNews`)

This skill enables `@Journalist`, `@Researcher`, `@Product Manager`, and `@Personal Assistant` to monitor breaking global news, search topical news wires, and pull trending technology/startup stories.

---

## Setup Instructions

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/research/news-wire/scripts/news_wire.py`.
- **Configuration Properties (`nadia.prop.*`)**:
  - **Keyless Out-of-the-Box**: `hn-top` and `search` (via HackerNews Firebase & Algolia APIs) require no API key.
  - **Global News Wire Properties (Optional)**:
    - `nadia.prop.newsdata.apiKey`: API key for **[NewsData.io](https://newsdata.io/docs)** (`headlines` command).
    - `nadia.prop.gnews.apiKey`: API key for **[GNews.io](https://gnews.io/)** (`headlines` fallback/provider).
    - Both properties are automatically registered in **Settings ➔ Properties** (`~/.nadia/nadia.properties`).

---

## 1. Core Operational Workflows

### 1.1 Fetching Top Technology & Startup Wire Stories (`hn-top`)
Retrieve top front-page stories from HackerNews (keyless):

```bash
python ~/.nadia/skills/research/news-wire/scripts/news_wire.py hn-top --limit 15
```

### 1.2 Searching News & Tech Stories by Keyword (`search`)
Search stories by topic, company, or breaking event (uses GNews/NewsData when configured, and always includes HackerNews Algolia search results):

```bash
python ~/.nadia/skills/research/news-wire/scripts/news_wire.py search --query "artificial intelligence" --limit 10
```

### 1.3 Fetching Global Breaking Headlines (`headlines`)
Query breaking world/business/technology headlines via `NewsData.io` or `GNews.io` (falls back to HackerNews top stories if neither API key is set yet):

```bash
python ~/.nadia/skills/research/news-wire/scripts/news_wire.py headlines --category "technology" --country "us" --limit 10
```

---

## 2. Editorial & Brief Guidelines

1. **Source Attribution**: Always cite the original publication source, publication timestamp, and article URL for every story.
2. **Living Stories & Daily Brief**: When `@Journalist` or `@Personal Assistant` discovers high-priority breaking news, log a concise summary via `storeBriefEntry` under category `"news"`.

