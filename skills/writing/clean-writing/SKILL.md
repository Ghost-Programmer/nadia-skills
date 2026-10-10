---
name: CleanWritingSkill
description: Shape, polish, and clean raw material (markdown file, text file, HTML file, or direct chat input) into a clear, cohesive, grounded article paragraph by paragraph. Use when the user wants to clean up, shape, polish, or rewrite messy notes, drafts, transcripts, HTML, or unformatted text into a structured article.
tools: []
---

# Clean-Writing / Article Shaping Skill

This skill transforms unstructured or messy input—whether a Markdown file, plain text file, HTML file, or raw text pasted directly in chat—into a cohesive, well-structured, and rigorously grounded article through a deliberate, step-by-step shaping session.

---

## 1. Input Ingestion & The Quarry Principle

- **Supported Input Sources**:
  - Markdown files (`.md`)
  - Plain text files (`.txt`)
  - HTML documents (`.html`, `.htm`)
  - Direct text, transcripts, or notes pasted in the chat
- **Input Pile is Read-Only**: Treat the raw source strictly as a read-only **input pile** (a quarry of raw ideas, facts, quotes, and fragments). **Never edit or mutate the raw source material**.
- **Target Document**: If the user has not specified a target output file path for the article, ask once at the beginning and remember the destination path.
- **Read First**: Read the entire input pile end-to-end to form a complete mental model of its material, themes, and potential gaps before drafting anything.

---

## 2. The Clean-Writing Cognitive Loop

Follow these structured steps sequentially:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Read the Pile End-to-End                                 │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Establish Prerequisites & Baseline Grounding             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Propose 2–3 Candidate Openings (Distinct Thesis Angles)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Grow Block-by-Block (Defend Format, Ground Concepts)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Incrementally Append to Article & Repeat Until Done      │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Read the Pile
- Ingest and review the entire source pile (strip extraneous HTML tags if parsing HTML, untangle transcript speakers, or index unorganized notes).
- Identify core assertions, key examples, quotes, and structural themes.

### Step 2: Establish Prerequisites (Baseline Grounding)
- Agree with the user on what the target reader knows walking in (the **prerequisite grounded concepts**).
- Balance the threshold: demanding too many prerequisites shuts out readers; demanding too few drowns the opening in tedious baseline definitions.

### Step 3: Propose 2–3 Candidate Openings
- Present 2 to 3 distinct candidate opening paragraphs, each framing a different thesis or rhetorical angle.
- Require the user to choose one or construct a hybrid.
- The chosen opening sets the contract that dictates what the rest of the article must deliver.

### Step 4: Grow Paragraph by Paragraph
- For each subsequent section, ask: *"Given where we are, what does the reader need to hear next?"*
- Mine the pile to supply the content.
- Ensure every new block only leans on previously grounded concepts.
- Have explicit, deliberate arguments about format choice before writing the block.

### Step 5: Incremental Appending
- Append each agreed-upon paragraph or block immediately to the target article file (or output incrementally in chat).
- Re-read the target file from disk before writing to ensure manual user edits are preserved.
- Never batch the entire article silently; write incrementally so progress is transparent.

### Step 6: Completion
- Continue the loop until the user confirms the article is complete.

---

## 3. Concept Grounding Framework

Every concept must be **grounded** before a block can lean on it. A block that relies on an ungrounded concept loses the reader.

- **Unit of Grounding**: The unit is the underlying **concept/idea**, not just the jargon term. Where a term exists, land both the idea and the term together.
- **Two Paths to Grounding**:
  1. **Prerequisite**: Grounded before the opening. The reader brings this knowledge walking in (settled in Step 2).
  2. **Introduced**: Grounded by an earlier block within the article. Once introduced, subsequent blocks may lean on it.
- **Running Ledger**: Maintain a mental ledger of all grounded concepts. If the next move needs an ungrounded concept, ground it first before proceeding.

---

## 4. Conversational Rigor & Editorial Grilling

Act as a rigorous, constructive editor. Challenge weak logic, fuzzy phrasing, and unearned transitions:

- *"What does this paragraph do for the reader that the previous one didn't?"*
- *"If we cut this sentence, what breaks?"*
- *"Is this prose, or should it be a list? Why prose?"*
- *"This sentence is trying to do two jobs at once: split it or pick one."*
- *"The opening promised X, but we have drifted to Y. Do we steer back or revise the opening?"*

---

## 5. Deliberate Format Selection

Weigh format tradeoffs out loud with the user rather than defaulting silently:

- **Prose vs. List**: Use prose to drive an argument or narrative; use bulleted lists only for strictly parallel, scannable items.
- **Inline vs. Callout**: Use callout blocks (`> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`) strictly when an aside or caution would derail the main argument inline. Otherwise, integrate smoothly inline.
- **Table vs. Repeated Structure**: Use Markdown tables when 3+ items share identical attributes/fields. Use prose with bold leads otherwise.
- **Quote vs. Paraphrase**: Use direct quotes only when the exact phrasing is essential. Paraphrase when only the underlying concept matters.
- **Code Block vs. Inline Code**: Use multi-line code blocks for runnable, illustrative, or formatted snippets; use inline code (`foo`) for individual identifiers or tokens.

---

## 6. Mining the Pile (Quarry Rules)

- Treat the raw material as raw stone: split fragments across multiple paragraphs, merge related points, or rewrite unpolished notes into clean prose.
- Speak in **one cohesive voice** across the entire resulting article.
- **Name Gaps Explicitly**: If the article's flow requires an example, stat, or clarification not present in the pile, state the gap directly: *"We need a concrete example here to ground this concept, but the source pile lacks one. Please provide one or we must adjust the claim."*

---

## 7. Safety & Scope Guardrails

- **Do Not Edit the Raw Input File**: The input file is strictly read-only.
- **Do Not Fabricate Extraneous Facts**: Limit factual claims to what is in the pile or what the user provides in the interactive session.
- **Do Not Add Unsolicited Boilerplate**: Do not add publishing metadata, unprompted frontmatter, or extraneous platform tags unless requested by the user.
- **Respect User Edits**: Always re-read the target article file before writing changes to avoid overwriting user edits.

## Setup Instructions

### 1. Prerequisites & Environment
- **Zero External Dependencies**: The Clean-Writing cognitive workflow is a pure procedural reasoning and article-shaping protocol.
- **File System Permissions**: Ensure the agent has read access to the input source pile (`.md`, `.txt`, `.html`) and write access to the designated output file location.
- **GFM Formatting**: Target outputs should follow standard GitHub Flavored Markdown (GFM) conventions.

