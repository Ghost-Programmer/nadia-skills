---
name: TasksSkill
description: Instruction guidelines and syntax examples for managing Google Tasks and Task Lists (listing, searching, creating, updating/patching, moving, and deleting) using the gws CLI.
tools: [executeSessionCommand]
---

# Google Tasks Skill (gws CLI)

This skill instructs the agent on how to manage Google Task Lists (tasklists) and individual Tasks using the `gws` command-line utility.

## Prerequisites

- The `gws` CLI must be installed and authenticated.
- Always use the `executeSessionCommand` tool to execute `gws` commands.

## 1. Managing Task Lists (Tasklists Operations)

### Listing Task Lists
Retrieve all task lists for the authenticated user.
```bash
gws tasks tasklists list --format table
```

### Retrieving a Task List
Retrieve metadata for a specific task list by its ID.
```bash
gws tasks tasklists get --params '{"tasklist": "<tasklist_id>"}'
```

### Creating a Task List
> [!IMPORTANT]
> This is a **write** operation. Confirm with the user before executing.
```bash
gws tasks tasklists insert --json '{"title": "<title>"}'
```

### Updating/Patching a Task List
Use `update` to overwrite or `patch` to partially modify a task list.
- **Update**:
  ```bash
  gws tasks tasklists update --params '{"tasklist": "<tasklist_id>"}' --json '{"id": "<tasklist_id>", "title": "<new_title>"}'
  ```
- **Patch**:
  ```bash
  gws tasks tasklists patch --params '{"tasklist": "<tasklist_id>"}' --json '{"title": "<new_title>"}'
  ```

### Deleting a Task List
> [!CAUTION]
> Deletion is permanent and removes all tasks inside the list. Get explicit user consent.
```bash
gws tasks tasklists delete --params '{"tasklist": "<tasklist_id>"}'
```

---

## 2. Managing Tasks (Tasks Operations)

### Listing Tasks in a List
Retrieve all tasks in a specific task list.
```bash
gws tasks tasks list --params '{"tasklist": "<tasklist_id>"}' --format table
```
*Optional parameters (within `--params`):*
- `"showCompleted": true` - Include completed tasks.
- `"showHidden": true` - Include hidden/cleared tasks.

### Retrieving a Specific Task
```bash
gws tasks tasks get --params '{"tasklist": "<tasklist_id>", "task": "<task_id>"}'
```

### Creating/Inserting a Task
> [!IMPORTANT]
> This is a **write** operation. Confirm with the user before executing.
```bash
gws tasks tasks insert --params '{"tasklist": "<tasklist_id>"}' --json '{"title": "<title>", "notes": "<notes>", "due": "<rfc3339_date>"}'
```
*Note:* The `"due"` field must be an RFC 3339 formatted date-time string (e.g., `2026-08-30T12:00:00Z`). Only the date portion is stored; time components are discarded.

### Updating/Patching a Task
Modify properties of an existing task (e.g., to mark it as completed).
- **Patch** (partial update, e.g. complete a task):
  ```bash
  gws tasks tasks patch --params '{"tasklist": "<tasklist_id>", "task": "<task_id>"}' --json '{"status": "completed"}'
  ```
- **Update** (overwrite entire task details):
  ```bash
  gws tasks tasks update --params '{"tasklist": "<tasklist_id>", "task": "<task_id>"}' --json '{"id": "<task_id>", "title": "<new_title>", "notes": "<new_notes>", "status": "needsAction"}'
  ```

### Deleting a Task
> [!CAUTION]
> Deleting a task is permanent. Confirm with the user.
```bash
gws tasks tasks delete --params '{"tasklist": "<tasklist_id>", "task": "<task_id>"}'
```

### Clearing Completed Tasks
Marks all completed tasks in a list as `hidden`. They will no longer appear in default task lists.
```bash
gws tasks tasks clear --params '{"tasklist": "<tasklist_id>"}'
```

---

## 3. Moving Tasks (Move Operations)

Move a task to a different position, nest it under a parent task (subtask), or move it to a different task list.

### Usage
```bash
gws tasks tasks move --params '{"tasklist": "<src_list_id>", "task": "<task_id>", "destinationTasklist": "<dst_list_id>", "parent": "<parent_task_id>", "previous": "<prev_sibling_task_id>"}'
```

*Query Parameters inside `--params`:*
- `"destinationTasklist"`: (Optional) ID of a different task list to move the task into.
- `"parent"`: (Optional) ID of a task to nest this task under as a subtask. Omit this to move a task back to the top level.
- `"previous"`: (Optional) ID of the sibling task directly preceding this one. Omit to move to the first position.

### Examples
- Make a task a subtask of another task (e.g., parent ID `parent123`):
  ```bash
  gws tasks tasks move --params '{"tasklist": "list123", "task": "task456", "parent": "parent123"}'
  ```
- Move a task to a different task list:
  ```bash
  gws tasks tasks move --params '{"tasklist": "list123", "task": "task456", "destinationTasklist": "list789"}'
  ```
