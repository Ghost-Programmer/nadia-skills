---
name: AskMeSkill
description: Relentlessly interview and grill the user about a plan, decision, or idea to stress-test their thinking and map out a comprehensive design tree. Use when the user asks to be grilled, stress-tested, or uses trigger phrases like 'ask me', 'grill me', 'stress test', or wants deep interactive requirement probing.
tools: []
---

# Ask-Me / Grilling Skill

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

## Setup Instructions

- **Prerequisites**: Ensure an active Nadia interactive chat session with multi-turn conversation support.
- **Configuration**: No external binaries, third-party libraries, or API credentials required.
- **Workflow Mode**: Operates directly through conversational prompts and structured question rounds; uses system chat memory to track the decision frontier.

---

## 1. The Design Tree & Round Execution

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

### Round Formatting Structure

Format each round strictly as follows:

```markdown
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices or trade-offs>

➡️ <your recommended answer with clear rationale>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices or trade-offs>

➡️ <your recommended answer with clear rationale>
```

---

## 2. Dynamic Tree Expansion & Frontier Evolution

- Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them.
- Recompute the frontier and ask the next round.
- A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

---

## 3. Fact Discovery vs. User Decisions

- **Finding facts is your job, never the user's**: When a frontier question needs a fact from the environment (filesystem, project files, tools, API contracts, etc.), use available tools or investigate directly; do not ask the user for anything you could inspect or look up yourself.
- **Do not block the frontier**: An ongoing exploration is an unsettled prerequisite, so only questions downstream of it wait; ask the rest of the available frontier immediately.
- **Decisions belong to the user**: Clearly formulate the choices and trade-offs, present your recommended path, and wait for the user's input.

---

## 4. Completion Criteria

The interview session is complete when the frontier is empty:

- Every branch of the design tree has been visited.
- Nothing is left silently assumed.
- Summarize the settled decisions clearly.
- **Do not act on or execute the plan** until the user explicitly confirms that you have reached a shared understanding.
