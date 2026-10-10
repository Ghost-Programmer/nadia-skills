---
name: DocumentsSkill
description: Instruction guidelines and syntax examples for managing Google Docs (creating documents, reading content, appending text, applying batch updates, and deleting files) using the gws CLI.
tools: [executeSessionCommand]
---

# Google Docs Documents Skill (gws CLI)

This skill instructs the agent on how to see, create, edit, and delete Google Docs using the `gws` command-line utility.

## Prerequisites

- The `gws` CLI must be installed and authenticated.
- Always use the `executeSessionCommand` tool to execute `gws` commands.

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

## Setup Instructions

### 1. Prerequisites & CLI Installation
- **gws CLI**: The Google Workspace CLI utility (`gws`) must be installed and accessible on system `PATH`.
- **Runtime**: Ensure Node.js or the native runtime required by `gws` is available.

### 2. Google Workspace Authentication & Permissions
- **Google Cloud APIs**: Enable both the **Google Docs API** (`https://www.googleapis.com/auth/documents`) and **Google Drive API** (`https://www.googleapis.com/auth/drive`) in Google Cloud Console.
- **Authentication**:
  1. Authenticate `gws` with your Google account:
     ```bash
     gws auth login
     ```
  2. Verify document creation or retrieval access:
     ```bash
     gws docs documents create --json '{"title": "Test Doc"}'
     ```
- **Drive Deletion Permissions**: Google Docs files are stored in Google Drive; deletion operations require full Google Drive API write permissions.

