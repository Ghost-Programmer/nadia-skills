---
name: BlogWatcherSkill
description: Guidelines and instructions for automatically discovering blog feeds, checking for new articles, generating summaries, and logging them as briefs.
tools: [watchBlog]
---

# BlogWatcher Skill

This skill allows the agent to automatically monitor any blog, discover its feed (RSS/Atom or WordPress API), detect new posts, summarize them in plain English, and store them in the briefs system.

## State Tracking (RAG Memory)

The tool saves check state facts inside the episodic (RAG) memory under the `blog_watcher_state` type. The state holds the last checked post ID or GUID, preventing duplicate notifications.

## Execution Pattern

1. Call the `watchBlog` tool with the target `blogUrl`.
2. The tool automatically resolves the feed URL using HTML header discovery or fallback endpoint probing.
3. If new post(s) are found since the last check, the tool:
   - Summarizes the post contents in 2-3 sentences.
   - Logs the summary as a brief entry under the `news` category.
   - Updates RAG memory with the new latest post ID.
4. Report the summary of the check results to the user.

## Setup Instructions

### 1. Prerequisites & Outbound Connectivity
- **Network Access**: Nadia requires outbound HTTP/HTTPS access to probe target websites and fetch RSS/Atom XML feeds.
- **RAG & Brief Storage**: Ensure episodic memory (PGVector or local vector store) and relational brief tables are initialized.

### 2. Feed State Tracking
- **Automatic State Storage**: The `watchBlog` tool automatically creates and updates `blog_watcher_state` memory records tracking the latest post GUIDs. No manual configuration is required.
- **Scheduled Checks**: If recurring monitoring is desired, register a cron trigger in Nadia (e.g., every 6 hours).

