---
name: blogwatcher
description: Guidelines and instructions for automatically discovering blog feeds, checking for new articles, generating summaries, and logging them as briefs.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: research
  display-name: BlogWatcherSkill
allowed-tools: watchBlog
tools: [watchBlog]
---

# BlogWatcher Skill

This skill allows the agent to automatically monitor any blog, discover its feed (RSS/Atom or WordPress API), detect new posts, summarize them in plain English, and store them in the briefs system.

---

## Setup Instructions

### External App & Integration Setup

- **External Applications & Integrations**: No third-party accounts or API keys are required—Nadia's built-in `watchBlog` tool natively discovers and parses public RSS 2.0 and Atom XML feeds over HTTP/HTTPS.
- **State & Brief Persistence**:
  - Seen post GUIDs (`blog_watcher_state`) and article summaries are stored automatically in Nadia's episodic vector store and relational brief database.
  - To monitor blogs on a recurring schedule, add a cron job in **View ➔ 🕒 Scheduled Jobs**.

---

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
