---
name: DateTimeSkill
description: Instructions on how to retrieve the current date, time, and timezone of the host system.
tools: [getCurrentDateTime]
---
# Date and Time Guidelines

- **Current Date and Time**:
  - When asked for the current date, time, or relative timestamp, always invoke the `getCurrentDateTime` tool.
  - Never estimate the time or assume a static reference date.
- **Formatting**:
  - Format the returned date and time in a clear, human-readable layout.
  - Mention that the returned values are based on the host system's local clock.
