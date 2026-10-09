---
name: ResearchSkill
description: Conduct comprehensive internet research, investigative fact-finding, and information gathering by utilizing the Researcher staff member and tools (web_search, web_scrape). Use when the user asks to research a topic, look up information online, find data, verify claims, or summarize and format web findings.
tools: [web_search, web_scrape, browser_navigate, browser_snapshot, storeBriefEntry, appendBriefEntry, getBriefEntries, searchMemory, saveMemory, updateMemory, getCurrentDateTime]
---

# Internet Research & Information Synthesis Skill

This skill guides the agent in conducting thorough, multi-source online investigations, fact-checking, and structured summarization by delegating to and adopting the **Researcher** staff workflow.

---

## 1. Triggering the Researcher Workflow

Activate this skill whenever the user requests:

- Deep-dive research on a topic, concept, technology, company, or event
- Fact verification, statistic lookups, or claim confirmation
- Online data extraction and page content analysis
- Competitive intelligence, comparison matrices, or literature summaries

---

## 2. Research Execution Pipeline

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Deconstruct Topic into Targeted Search Queries           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Execute Multi-Angle Search (web_search)                  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Scrape & Ingest Key Source Pages (web_scrape)            │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Cross-Verify Facts & Triangulate Findings                │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Synthesize & Deliver Structured Markdown Report          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Persist Summary to Brief & Long-Term Memory              │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Query Deconstruction

- Break down complex inquiries into 2–4 distinct, focused search queries.
- Incorporate specific domain terminology, entity names, and operator variations.

### Step 2: Multi-Angle Search (`web_search`)

- Invoke `web_search` with each formulated query.
- Evaluate search result titles, snippets, and domain authority.
- Identify the most credible, high-signal target URLs.

### Step 3: Deep Content Extraction (`web_scrape`)

- Call `web_scrape` on the selected primary URLs to retrieve full body text, tables, dates, and detailed statistics.
- If a web page requires complex browser rendering or interaction, fall back to `browser_navigate` and `browser_snapshot`.

### Step 4: Verification & Triangulation

- Compare assertions across multiple independent sources to eliminate bias, outdated information, and inaccuracies.
- If data points diverge between sources, explicitly report both findings and note the discrepancy.

### Step 5: Synthesis, Artifact Delivery & Session Brain Storage

Deliver a polished Markdown report structured as follows:

1. **Executive Summary**: 2–3 concise sentences outlining the primary answer or conclusion.
2. **Key Findings**: Structured bullet points highlighting core facts, numbers, dates, and context.
3. **Comparison Matrix / Data Tables**: Markdown tables when comparing specifications, options, benchmarks, or timelines.
4. **Sources & References**: Inline citations formatted as `[Source Title](URL)` directly alongside the referenced data.
5. **Session Brain Artifact File**: When compiling full reports or in-depth findings, **write and save the markdown file directly to `./session/brain/<topic_report>.md`**.
   - Present the clickable artifact link: `📄 [report_name.md](file:///e:/nadia/session/brain/<report_name>.md)`.
   - Never write to `.gemini` or default CLI AppData directories.

### Step 6: Brief & Memory Persistence

- **Daily Brief**: Call `storeBriefEntry` (or `appendBriefEntry`) with `category: "research"`, `staffName: "Researcher"`, and a concise markdown summary.
- **Long-Term Memory**: Call `saveMemory` with `category: "fact"` and relevant tags to persist valuable findings for future sessions.

---

## 3. Tool Usage Reference

### `web_search`

- **Purpose**: Fast search engine lookup returning top URLs, titles, and snippets.
- **Example**:

  ```json
  {
    "query": "Java 25 latest features release date specification"
  }
  ```

### `web_scrape`

- **Purpose**: Extracts clean, readable text from a destination webpage, stripping HTML boilerplate and ads.
- **Example**:

  ```json
  {
    "url": "https://openjdk.org/projects/jdk/25/"
  }
  ```

### `storeBriefEntry`

- **Purpose**: Persists research summary into the active system brief.
- **Example**:

  ```json
  {
    "category": "research",
    "staffName": "Researcher",
    "code": "research_jdk25_summary",
    "text": "- **JDK 25 Research**: Scanned OpenJDK specifications. Key features include..."
  }
  ```

### `saveMemory`

- **Purpose**: Records verified facts or user research interests into episodic memory.
- **Example**:

  ```json
  {
    "content": "JDK 25 is slated for release in September 2025 featuring enhanced Virtual Threads monitoring.",
    "category": "fact",
    "tags": "java, jdk25, research, openjdk"
  }
  ```

---

## 4. Quality Standards & Guardrails

1. **Mandatory Citations**: Every claim, figure, and date must link directly to the source URL (`[Source](URL)`).
2. **Zero Speculation**: Do not invent facts or extrapolate beyond what was retrieved from search and scrape operations.
3. **No Conversational Filler**: Immediately execute tools without preamble.
4. **Clean Markdown**: Use standard Markdown headings, lists, tables, and callouts (`> [!NOTE]`, `> [!TIP]`).
