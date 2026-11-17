---
name: presentations
description: Instruction guidelines and syntax examples for managing Google Slides presentations (creating, reading structures, adding/deleting slides, modifying elements, and deleting files) using the gws CLI.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: productivity
  display-name: PresentationsSkill
allowed-tools: executeSessionCommand
tools: [executeSessionCommand]
---

# Google Slides Presentations Skill (gws CLI)

This skill instructs the agent on how to see, create, edit, and delete Google Slides presentations using the `gws` command-line utility.

---

## Setup Instructions

### External App & Integration Setup (`gws` Google Workspace CLI)

1. **Install Node.js & Google Workspace CLI (`gws`)**:
   - Install **Node.js 20+** (`https://nodejs.org/`), then install `@googleworkspace/cli` globally and ensure `gws` is on system `PATH`:
     ```bash
     npm install -g @googleworkspace/cli
     gws --version
     ```
2. **Enable Google Slides API & Google Drive API in Google Cloud Console**:
   - Open [Google Cloud Console — API Library](https://console.cloud.google.com/apis/library), select or create a project, and enable **Google Slides API & Google Drive API** (scope: `https://www.googleapis.com/auth/presentations, https://www.googleapis.com/auth/drive`).
   - Under **APIs & Services ➔ Credentials**, create an **OAuth 2.0 Client ID** (*Desktop app*)—or run `gws auth setup` if `gcloud` CLI is installed to provision credentials automatically.
3. **Authenticate & Verify**:
   - Sign in from a terminal so OAuth tokens are cached for `executeSessionCommand`:
     ```bash
     gws auth login
     gws drive files list --params '{"q": "mimeType=\x27application/vnd.google-apps.presentation\x27", "pageSize": 3}' --format table
     ```

---

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
