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

## Setup Instructions

### 1. Prerequisites & Host System Clock
- **System Clock**: Ensure the host operating system clock is synchronized via NTP (Network Time Protocol).
- **Timezone Configuration**: Nadia inherits the host operating system timezone by default. To override, set the `user.timezone` system property or `TZ` environment variable (e.g., `-Duser.timezone=America/New_York`).
- **Spring AI Tool**: The `getCurrentDateTime` tool is auto-registered by Nadia's runtime context.

