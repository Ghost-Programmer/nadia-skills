---
name: BriefSkill
description: Guidelines and instructions for storing, appending, retrieving, and compiling brief entries into nicely formatted markdown report summaries including Blog Watch news.
tools: [storeBriefEntry, appendBriefEntry, getBriefEntries, deleteBriefEntry, clearBriefEntries]
---

# Brief Reporting and Summary Skill

This skill guides the agent in managing temporary briefs and compiling them into polished Markdown summaries. Use this skill when the user asks for a brief, summary report, or status report of stored information, or when automated background tasks (like weather, quotes, blog monitoring, email triage) log information.

---

## Standard Brief Categories

| Category | Typical Source / Tool | Description |
| :--- | :--- | :--- |
| `daily_brief` | Personal Assistant / Nadia | Consolidated morning and executive briefing reports. |
| `news` / `blog` | `watchBlog` / BlogWatcher | Tech blog monitoring articles, RSS/Atom feeds, and software release notes with clickable links `[Title](URL)`. |
| `email` | Personal Assistant / Gmail | Unread email summaries, important sender highlights, and drafted items. |
| `calendar` | Personal Assistant / Google Calendar | Daily agenda, meeting schedule, upcoming deadlines, and focus time blocks. |
| `weather` | Personal Assistant / `weather` | Local meteorological conditions, forecasts, and precipitation alerts. |
| `todo` / `action_items` | Personal Assistant / Architect | Action items, pending approvals (e.g. ADRs), and follow-up checklists. |
| `quote` | Personal Assistant | Daily inspirational quote and motivational reflections. |
| `stock` | Stock Broker | Market summaries, equity price changes, and portfolio indices. |
| `network` | Network Engineer | Host metrics, network gateway ping, and infrastructure diagnostics. |
| `printer` | 3D Printer | Active 3D print progress, AMS filament levels, and printer health. |

---

## Storing & Appending Entries

When a task, scheduled job, or interactive session needs to log or update brief data:

1. **Store New / Replace**: Call `storeBriefEntry` with category, text, staffName, and code to create or replace a brief.
2. **Append to Existing**: Call `appendBriefEntry` with category, text, staffName, and code to append new notes, events, or email batches to the existing brief without wiping previous entries.

---

## Retrieving and Compiling Reports

When the user asks for a brief or summary (e.g., "Give me a brief of the news category", "Give me my daily brief", or "Give me my brief as a markdown report"):

1. **Step 1 - Retrieve the data**: Call `getBriefEntries` passing the requested category (or `"all"`) and call `getCurrentDateTime`.
   > [!IMPORTANT]
   > **CONCURRENCY & SEQUENCE PROTOCOL**:
   > - Do NOT call `getBriefEntries` and `clearBriefEntries` (or `deleteBriefEntry`) in the same heartbeat step. Because independent tool calls execute concurrently, calling them in the same turn will wipe the entries before they can be read.
   > - Always execute `getBriefEntries` first.
2. **Step 2 - Clear Consumed Entries (Mandatory Anti-Duplication Rule)**:
   - Once `getBriefEntries` returns data, you **MUST immediately call `clearBriefEntries(category: "all")`** (or `clearBriefEntries` for the retrieved category) in the following heartbeat step.
   - This prevents old or already-reported items (such as processed emails, past blog discoveries, old quotes, or historical notifications) from being reported again in subsequent briefing cycles.
3. **Step 3 - Compile and present the report**:
   - Group the returned entries logically by **Category**, sort them chronologically by **Date/Time** (newest first), and present the clean, rich Markdown executive report.
   - Optionally call `storeBriefEntry` (`category: "daily_brief"`, `staffName: "Personal Assistant"`, `code: "morning_brief_report"`) to archive the compiled summary if requested.

### Executive Markdown Report Template

Use the following layout structure to compile multi-domain executive briefs:

```markdown
# 🌅 Executive Briefing Report
*Generated on: YYYY-MM-DD HH:MM*

> [Daily Inspirational Quote or Thought]

---

## 📅 Today's Agenda & Schedule
- **09:00 AM** - Team Standup (Zoom)
- **02:00 PM** - Architecture Review

## 📝 Action Items & Pending TODOs
- [ ] Review PR #42 for Nadia UI docking container
- [ ] Approve ADR-005 for Database Connection Pool

## ✉️ Important Email Highlights
- **Subject**: Q3 Budget Sign-off from Alice — *Action required by 5 PM*
- **Subject**: Cloud Provider Invoice from Billing — *Auto-paid*

## 📰 Tech Blog Monitoring & Industry News
- **[Article Title 1](https://blog-url.com/post-1)** (Source: Baeldung)
  - Concise 2-sentence summary of the new feature or pattern.
- **[Article Title 2](https://spring.io/blog/post-2)** (Source: Spring.io)
  - Key highlights and release notes.

## 🌦️ Local Weather
- **Current**: 72°F, Partly Cloudy. High: 78°F, Low: 64°F.

## 🌐 System & Infrastructure Status
- **Database**: Connected (PostgreSQL, 1.2 ms latency)
- **Fleet**: 3D Printer Idle (100% Ready)
```
