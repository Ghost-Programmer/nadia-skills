---
name: documents
description: Instruction guidelines and syntax examples for managing Google Docs (creating documents, reading content, appending text, applying batch updates, and deleting files) using the gws CLI.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: productivity
  display-name: DocumentsSkill
allowed-tools: executeSessionCommand
tools: [executeSessionCommand]
---

# Google Docs Documents Skill (gws CLI)

This skill instructs the agent on how to see, create, edit, and delete Google Docs using the `gws` command-line utility.

---

## Setup Instructions

### External App & Integration Setup (`gws` Google Workspace CLI)

1. **Install Node.js & Google Workspace CLI (`gws`)**:
   - Install **Node.js 20+** (`https://nodejs.org/`), then install `@googleworkspace/cli` globally and ensure `gws` is on system `PATH`:
     ```bash
     npm install -g @googleworkspace/cli
     gws --version
     ```
2. **Enable Google Docs API & Google Drive API in Google Cloud Console**:
   - Open [Google Cloud Console — API Library](https://console.cloud.google.com/apis/library), select or create a project, and enable **Google Docs API & Google Drive API** (scope: `https://www.googleapis.com/auth/documents, https://www.googleapis.com/auth/drive`).
   - Under **APIs & Services ➔ Credentials**, create an **OAuth 2.0 Client ID** (*Desktop app*)—or run `gws auth setup` if `gcloud` CLI is installed to provision credentials automatically.
3. **Authenticate & Verify**:
   - Sign in from a terminal so OAuth tokens are cached for `executeSessionCommand`:
     ```bash
     gws auth login
     gws drive files list --params '{"pageSize": 3}' --format table
     ```

---

## 1. Creating Documents (Create Operations)

Create a new blank document.

> [!IMPORTANT]
> This is a **write** operation. Confirm with the user before executing.

### Usage
```bash
gws docs documents create --json '{"title": "<title>"}'
```

### Example
```bash
gws docs documents create --json '{"title": "Project Meeting Notes"}'
```
*Note:* The response will contain the newly created `documentId` which is required for subsequent operations.

---

## 2. Seeing/Reading Documents (Read Operations)

To view the plain text content of a Google Doc, it is highly recommended to export it. For structural metadata, use the get endpoint.

### Reading Document Text Content (Recommended)
Export the document to plain text so that it can be easily read:
```bash
gws drive files export --params '{"fileId": "<id>", "mimeType": "text/plain"}'
```
- Example:
  ```bash
  gws drive files export --params '{"fileId": "doc_id_12345", "mimeType": "text/plain"}'
  ```

### Getting Document Structure/Metadata
Retrieve the structural outline of the document (paragraphs, tables, lists, and elements metadata):
```bash
gws docs documents get --params '{"documentId": "<id>"}'
```

---

## 3. Editing Documents (Update/Write Operations)

Use the helper command to append text or `batchUpdate` for structural changes.

> [!IMPORTANT]
> Updating document content is a **write** operation. Confirm text changes with the user.

### Appending Plain Text (Helper Command)
Append text directly to the end of the document body:
```bash
gws docs +write --document <id> --text "<text>"
```
- Example:
  ```bash
  gws docs +write --document doc_id_12345 --text "This is an appended summary line."
  ```

### Inserting Rich Formatting or Inserting Text at Indices (batchUpdate)
Apply one or more insertions or formatting commands:
```bash
gws docs documents batchUpdate --params '{"documentId": "<id>"}' --json '{"requests": [<update_requests>]}'
```

#### Inserting text at a specific index
Index `1` represents the very beginning of the document body:
```json
{
  "insertText": {
    "location": {
      "index": 1
    },
    "text": "Executive Summary:\n"
  }
}
```

#### Example Batch Update
```bash
gws docs documents batchUpdate --params '{"documentId": "doc_id_12345"}' --json '{"requests": [{"insertText": {"location": {"index": 1}, "text": "Draft Title\n"}}]}'
```

---

## 4. Deleting Documents (Delete Operations)

Documents are stored as files in Google Drive. To delete a document, you must use the Google Drive API.

> [!CAUTION]
> Deleting files is permanent. Always verify the document ID and get explicit user consent before executing.

### Usage
```bash
gws drive files delete --params '{"fileId": "<DOCUMENT_ID>"}'
```

### Example
```bash
gws drive files delete --params '{"fileId": "doc_id_12345"}'
```
