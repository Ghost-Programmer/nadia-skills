---
name: PresentationsSkill
description: Instruction guidelines and syntax examples for managing Google Slides presentations (creating, reading structures, adding/deleting slides, modifying elements, and deleting files) using the gws CLI.
tools: [executeSessionCommand]
---

# Google Slides Presentations Skill (gws CLI)

This skill instructs the agent on how to see, create, edit, and delete Google Slides presentations using the `gws` command-line utility.

## Prerequisites

- The `gws` CLI must be installed and authenticated.
- Always use the `executeSessionCommand` tool to execute `gws` commands.

## 1. Creating Presentations (Create Operations)

Create a new blank presentation.

> [!IMPORTANT]
> This is a **write** operation. Confirm with the user before executing.

### Usage
```bash
gws slides presentations create --json '{"title": "<title>"}'
```

### Example
```bash
gws slides presentations create --json '{"title": "Q3 Sales Presentation"}'
```
*Note:* The response will contain the newly created `presentationId` which is required for subsequent operations.

---

## 2. Seeing/Reading Presentations (Read Operations)

Get the full slide structure, elements layout, and text contents of an existing presentation.

### Usage
```bash
gws slides presentations get --params '{"presentationId": "<id>"}'
```

### Example
```bash
gws slides presentations get --params '{"presentationId": "1a2b3c4d5e"}'
```

---

## 3. Editing Presentations (Update/Write Operations)

Use `gws slides presentations batchUpdate` to apply one or more structural or text changes.

> [!IMPORTANT]
> Updating presentations is a **write** operation. Verify your request JSON and get user confirmation.

### Usage
```bash
gws slides presentations batchUpdate --params '{"presentationId": "<id>"}' --json '{"requests": [<update_requests>]}'
```

### Common Update Requests

#### Creating a New Slide
Add a slide with a specific layout (e.g. `TITLE_AND_BODY`, `SECTION_HEADER`, `BLANK`):
```json
{
  "createSlide": {
    "insertionIndex": 1,
    "slideLayoutReference": {
      "predefinedLayout": "TITLE_AND_BODY"
    }
  }
}
```

#### Inserting Text
Insert text into a specific shape or text box ID (retrieve IDs by running `presentations get`):
```json
{
  "insertText": {
    "objectId": "element_id_123",
    "text": "Meeting Agenda:\n1. Metrics\n2. Next Steps"
  }
}
```

#### Deleting a Slide or Shape
Delete an object (a slide or a single shape) by its ID:
```json
{
  "deleteObject": {
    "objectId": "slide_or_element_id_123"
  }
}
```

### Example Batch Update
Create a slide and add text:
```bash
gws slides presentations batchUpdate --params '{"presentationId": "1a2b3c4d5e"}' --json '{"requests": [{"createSlide": {"insertionIndex": 1, "slideLayoutReference": {"predefinedLayout": "TITLE"}}}, {"insertText": {"objectId": "title_shape_id", "text": "Sales kickoff"}}]}'
```

---

## 4. Deleting Presentations (Delete Operations)

Presentations are stored as files in Google Drive. To delete a presentation, you must use the Google Drive API.

> [!CAUTION]
> Deleting files is permanent. Always verify the presentation ID and get explicit user consent before executing.

### Usage
```bash
gws drive files delete --params '{"fileId": "<PRESENTATION_ID>"}'
```

### Example
```bash
gws drive files delete --params '{"fileId": "1a2b3c4d5e"}'
```
