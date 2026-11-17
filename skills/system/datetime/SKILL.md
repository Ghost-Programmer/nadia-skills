---
name: datetime
description: Instructions on how to retrieve the current date, time, and timezone of the host system.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: system
  display-name: DateTimeSkill
allowed-tools: getCurrentDateTime
tools: [getCurrentDateTime]
---

# Date and Time Guidelines

- **Current Date and Time**:
  - When asked for the current date, time, or relative timestamp, always invoke the `getCurrentDateTime` tool.
  - Never estimate the time or assume a static reference date.
- **Formatting**:
  - Format the returned date and time in a clear, human-readable layout.
  - Mention that the returned values are based on the host system's local clock.

---

## Setup Instructions

- **External Applications & Integrations**: None required. Uses Nadia's built-in `getCurrentDateTime` tool reading the host OS clock (keep NTP time synchronization enabled on the host OS; override timezone if needed via `-Duser.timezone=America/New_York` or `TZ`).
