---
name: NoteSkill
description: Formats input text into a structured, professional markdown report featuring a generated name, detailed text description, list of actions needed, and possible considerations.
tools: []
---

# Note-Taking and Action Report Skill

This skill allows the agent to ingest unstructured or structured text and format it into a professional markdown report template. Use this skill when the user asks to summarize notes, document a task description, or format incoming information into a structured action plan.

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

## Setup Instructions

### 1. Prerequisites & Storage
- **No External Services Required**: The Note formatting skill operates entirely in-memory as a markdown formatting and synthesis pattern.
- **Renderer**: Rendered note outputs are formatted in GitHub-Flavored Markdown (GFM) compatible with the JavaFX chat stream and markdown viewers.

