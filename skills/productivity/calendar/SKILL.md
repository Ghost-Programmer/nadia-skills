---
name: CalendarSkill
description: Instruction guidelines and syntax examples for managing Google Calendar events, creating agendas, and performing read, insert, patch, and delete actions using the gws CLI.
tools: [executeSessionCommand]
---

# Google Calendar Skill (gws CLI)

This skill instructs the agent on how to manage Google Calendar events and compile agenda schedules using the `gws` command-line utility.

## Prerequisites

- The `gws` CLI must be installed and authenticated.
- Always use the `executeSessionCommand` tool to execute `gws` commands.

## 1. Retrieving Agendas (Read Operations)

Use the `gws calendar +agenda` helper command to retrieve upcoming schedules and events.

### Usage and Flags
```bash
gws calendar +agenda [flags]
```

- `--today`: Limit events to the current day.
- `--tomorrow`: Limit events to tomorrow.
- `--week`: Show events for the current week.
- `--days <N>`: Retrieve events for the next `<N>` days.
- `--calendar "<name_or_id>"`: Filter events to a specific calendar (default: all calendars).
- `--timezone "<iana_tz>"`: Override the default timezone (e.g., `America/New_York`).
- `--format table`: Outputs the agenda in a clean, readable ASCII table (recommended for log scans).

### Examples
- Show today's agenda:
  ```bash
  gws calendar +agenda --today
  ```
- Show this week's agenda in table format:
  ```bash
  gws calendar +agenda --week --format table
  ```
- Show events for the next 3 days on a specific calendar:
  ```bash
  gws calendar +agenda --days 3 --calendar "Work" --format table
  ```

---

## 2. Creating Events (Create/Write Operations)

Use the `gws calendar +insert` helper command to create new events.

> [!IMPORTANT]
> This is a **write** operation. Ensure you have the user's confirmation before executing, or double-check conflict times first using `gws calendar +agenda`.

### Usage and Flags
```bash
gws calendar +insert --summary "<text>" --start "<time>" --end "<time>" [flags]
```

- `--summary "<text>"`: The title/summary of the event (required).
- `--start "<iso_8601>"`: Start time in ISO 8601 / RFC3339 format (e.g. `2026-08-28T14:00:00-04:00`) (required).
- `--end "<iso_8601>"`: End time in ISO 8601 / RFC3339 format (required).
- `--calendar "<id>"`: Target calendar ID (default: `primary`).
- `--location "<text>"`: Location details.
- `--description "<text>"`: Event details or agenda notes.
- `--attendee "<email>"`: Add attendees (repeat flag to add multiple).
- `--meet`: Automatically generates and attaches a Google Meet video conference link.

### Examples
- Create a simple meeting:
  ```bash
  gws calendar +insert --summary "Project Sync" --start "2026-08-28T14:00:00-04:00" --end "2026-08-28T14:30:00-04:00"
  ```
- Create a client review event with attendees and a Google Meet link:
  ```bash
  gws calendar +insert --summary "Q3 Business Review" --start "2026-08-31T10:00:00-04:00" --end "2026-08-31T11:00:00-04:00" --attendee "client@example.com" --attendee "manager@example.com" --meet --description "Quarterly progress review session."
  ```

---

## 3. Listing & Searching Events (Detailed API)

If you need to search or locate a specific event to edit, query the events database.

### Usage
```bash
gws calendar events list --params '{"calendarId": "primary", "q": "search_query"}' --format table
```

- `"q"`: Search terms matching the title, description, location, attendee, etc.
- `"timeMin"`: Lower bound for an event's end time (formatted as RFC3339, e.g. `2026-08-28T00:00:00Z`).
- `"timeMax"`: Upper bound for an event's start time (formatted as RFC3339).

### Example
- Find an event named "Sync":
  ```bash
  gws calendar events list --params '{"calendarId": "primary", "q": "Sync"}' --format table
  ```

---

## 4. Editing & Modifying Events (Edit Operations)

Use the `patch` method on the `events` resource to modify parts of an event. You need the `eventId` of the targeted event.

> [!CAUTION]
> Modifying events can reschedule meetings or add/remove attendees. Always verify the `eventId` and get user confirmation.

### Usage
```bash
gws calendar events patch --params '{"calendarId": "primary", "eventId": "<EVENT_ID>"}' --json '{"summary": "New Title", "start": {"dateTime": "NewStartTime"}, "end": {"dateTime": "NewEndTime"}}'
```

### Examples
- Reschedule an event to a new time:
  ```bash
  gws calendar events patch --params '{"calendarId": "primary", "eventId": "a1b2c3d4e5"}' --json '{"start": {"dateTime": "2026-08-29T15:00:00-04:00"}, "end": {"dateTime": "2026-08-29T15:30:00-04:00"}}'
  ```
- Update the title and description:
  ```bash
  gws calendar events patch --params '{"calendarId": "primary", "eventId": "a1b2c3d4e5"}' --json '{"summary": "Updated Project Sync", "description": "Reviewing backlog and Q3 milestones."}'
  ```

---

## 5. Deleting Events (Delete Operations)

Use the `delete` method on the `events` resource to remove an event.

> [!CAUTION]
> Deletion is permanent. Always verify the `eventId` and get user consent before executing.

### Usage
```bash
gws calendar events delete --params '{"calendarId": "primary", "eventId": "<EVENT_ID>"}'
```

### Example
- Delete event with ID `a1b2c3d4e5`:
  ```bash
  gws calendar events delete --params '{"calendarId": "primary", "eventId": "a1b2c3d4e5"}'
  ```
