---
name: QuestionnaireSkill
description: Turn a decision, requirement, or topic you can't fully resolve alone into a targeted discovery questionnaire for a stakeholder, domain expert, or team member to fill out, and record it in the system brief as an actionable TODO item.
tools: [storeBriefEntry, appendBriefEntry]
---

# Questionnaire Generation Skill

Turn something you cannot answer alone into a **discovery questionnaire**: a structured Markdown document to hand to a specific person to fill in asynchronously, or to work through together during a meeting. The recipient holds knowledge the user lacks; the questionnaire extracts it cleanly and efficiently.

## Setup Instructions

- **Prerequisites**: Ensure `storeBriefEntry` and `appendBriefEntry` tools are registered in Nadia's `ToolRegistry`.
- **Configuration**: Active session workspace folder or project directory with write permissions for storing `to-questionnaire-<slug>.md` files.
- **Brief Integration**: System Briefing database table or in-memory brief service configured to record pending discovery questionnaires.

---

## 1. The Interview Workflow: "Grill the Send, Not the Subject"

Interview the user only about the *send*, which they can always answer: who it goes to, and what they need back. The questions in the document then target the **gap** between what the recipient knows and what the user needs.

### Step 1: Who is it going to?

Ask, in one concise exchange, the recipient's role, expertise, and relationship to the user. This establishes the questionnaire's tone and how much background context it must provide.
- *Done when*: You know who the recipient is and what domain knowledge they hold that the user lacks.

### Step 2: What do you need back?

Ask, in one concise exchange, the specific decisions, constraints, or facts the user cannot resolve alone and needs from this person.
- *Done when*: You have a concrete list of what the user must walk away able to decide or execute.

### Step 3: Write the Questionnaire

Draft questions specifically targeting the gap identified in Steps 1 and 2, following the Document Structure below.
- Save the file as `to-questionnaire-<slug>.md` in the active project/session directory (deriving the `<slug>` from the topic).
- Report the saved filepath.
- *Done when*: The file exists and every item the user named in Step 2 is covered by a focused question.

### Step 4: Record Questionnaire in the Brief as a TODO

Once the questionnaire file is created, automatically register it as a pending action item in the system brief using `appendBriefEntry` (or `storeBriefEntry`):

- **Tool Call**: `appendBriefEntry`
- **Parameters**:
  - `category`: `"todo"`
  - `text`: `- [ ] Send Questionnaire: **<Title>** to <Recipient> (File: `to-questionnaire-<slug>.md`)\n  - Purpose: <Brief Purpose>\n  - Action: Deliver to recipient and collect required inputs.`
  - `staffName`: `"Personal Assistant"`
  - `code`: `"questionnaire_<slug>"`
- *Done when*: The brief entry is stored so it surfaces in daily morning briefings and dashboard action item lists.

---

## 2. Document Structure & Template

Frame the document as a **discovery questionnaire**: the user lacks context, the recipient holds it. Order questions most-important-first, since async workflows mean you may only get one pass. Group questions under `##` headings by theme once there are more than a handful.

```markdown
# <Questionnaire Title>

**Purpose:** Why this questionnaire exists and the decisions riding on it.

**From:** <The User>  
**To:** <The Recipient>  
**How your answers will be used:** <Where the answers go and how they drive next steps>

---

## Context

One paragraph orienting a recipient who was not in the user's head. Provide enough background to answer well, without unnecessary filler.

---

## How to Answer

Deadline and estimated effort. Note that partial answers and "I don't know" are helpful: flag anything you are unsure of rather than skipping it.

---

## <Theme Heading 1>

One `##` section per theme. Under each, list questions ordered most-important-first. Every question represents a single idea (never compound), with a blockquote answer stub directly beneath, and a one-line *Why this matters* where helpful.

### 1. What load is the system expected to handle at launch?

*Why this matters: It decides whether we provision for burst traffic now or defer it.*

> 

---

### 2. What authentication provider will be used?

*Why this matters: Dictates required security integrations and client libraries.*

> 

---

## Anything Else?

A closing catch-all question:

### Is there anything critical we didn't ask that we should know?

> 
```

---

## 3. Execution Rules

- **Single Idea Per Question**: Never ask compound questions like "What database will we use and how will we back it up?". Split them into distinct questions.
- **Answer Stubs**: Always provide a clean markdown blockquote stub (`> `) beneath each question so the recipient can immediately type their answer.
- **Prioritize Importance**: Put high-impact, blocking questions at the top of each section.
- **Brief / TODO Integration**: Always ensure Step 4 is executed so that follow-up and delivery tracking remain visible across sessions and daily briefings.
