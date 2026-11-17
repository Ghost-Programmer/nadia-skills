---
name: note
description: Formats input text into a structured, professional markdown report featuring a generated name, detailed text description, list of actions needed, and possible considerations.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: productivity
  display-name: NoteSkill
tools: []
---

# Note-Taking and Action Report Skill

This skill allows the agent to ingest unstructured or structured text and format it into a professional markdown report template. Use this skill when the user asks to summarize notes, document a task description, or format incoming information into a structured action plan.

---

## Setup Instructions

- **External Applications & Integrations**: None required. Operates in-memory as a structured GitHub-Flavored Markdown (GFM) synthesis pattern rendered directly in Nadia's chat and Markdown studio.

---

## Report Template Structure

When creating a note report, use the following template format:

### 📋 [Generated Name/Title]
*Created on: YYYY-MM-DD HH:MM*

#### 🔍 Details / Description
[A polished, summarized description of the input text, providing context and main points.]

#### ⚡ Actions Needed
- [ ] Action Item 1
- [ ] Action Item 2
- [ ] ...

#### 💡 Considerations & Risks
- **Consideration 1**: Details...
- **Consideration 2**: Details...
