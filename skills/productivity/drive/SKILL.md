---
name: DriveSkill
description: Instruction guidelines and syntax examples for reading Google Drive metadata, listing folders, searching files, downloading content, and exporting documents using the gws CLI.
tools: [executeSessionCommand]
---

# Google Drive Skill (gws CLI)

This skill instructs the agent on how to list, search, download, and export files and folders from Google Drive using the `gws` command-line utility.

## Prerequisites

- The `gws` CLI must be installed and authenticated.
- Always use the `executeSessionCommand` tool to execute `gws` commands.

## 1. Listing & Searching Files (List Operations)

Use the `gws drive files list` command to list and search files/folders in Drive.

> [!NOTE]
> By default, `files list` returns all files, including those in the trash. It is recommended to use `trashed = false` in search queries to exclude them.

### Usage and Flags
```bash
gws drive files list --params '{"q": "<search_query>", "pageSize": <size>}' [flags]
```

- `q`: Query string for searching files. For syntax details, see the [Search Query Syntax](#search-query-syntax) section below.
- `pageSize`: Number of files to return per page (default: 100, max: 100).
- `--format table`: Outputs file details in a clean, readable ASCII table (recommended for log scans).

### Search Query Syntax
Use standard Google Drive query clauses in the `"q"` parameter:
- Search by name: `name = 'filename'` or `name contains 'terms'`
- Exclude trashed files: `trashed = false`
- Filter by folders only: `mimeType = 'application/vnd.google-apps.folder'`
- Filter by files in a folder: `'<FOLDER_ID>' in parents`

### Examples
- List the last 20 active files/folders in table format:
  ```bash
  gws drive files list --params '{"q": "trashed = false", "pageSize": 20}' --format table
  ```
- Search for a specific file by name:
  ```bash
  gws drive files list --params '{"q": "name = '\''Project Report.pdf'\'' and trashed = false"}' --format table
  ```
- List all folders in the root or a parent folder:
  ```bash
  gws drive files list --params '{"q": "mimeType = '\''application/vnd.google-apps.folder'\'' and trashed = false"}' --format table
  ```
- List files inside a specific folder:
  ```bash
  gws drive files list --params '{"q": "'\''1A2B3C4D5E'\'' in parents and trashed = false"}' --format table
  ```

---

## 2. Reading File Metadata

Use `gws drive files get` to retrieve details and metadata of a specific file.

### Usage
```bash
gws drive files get --params '{"fileId": "<FILE_ID>"}'
```

### Example
```bash
gws drive files get --params '{"fileId": "1a2b3c4d5e"}'
```

---

## 3. Downloading File Content (Read Operations)

To download or stream the raw content of binary files stored in Drive (e.g. PDFs, images, text files), set the `"alt": "media"` parameter.

### Usage
```bash
gws drive files get --params '{"fileId": "<FILE_ID>", "alt": "media"}'
```

### Example
- Read contents of a plain text file:
  ```bash
  gws drive files get --params '{"fileId": "1a2b3c4d5e", "alt": "media"}'
  ```

---

## 4. Exporting Google Docs/Sheets/Slides

Google Workspace documents (Docs, Sheets, Slides) cannot be downloaded as raw binary media directly. Instead, you must use the `export` endpoint to convert them to a standard format.

### Usage
```bash
gws drive files export --params '{"fileId": "<FILE_ID>", "mimeType": "<EXPORT_MIME_type>"}'
```

### Common Export Formats
- **Google Docs**:
  - Plain Text: `text/plain`
  - PDF Document: `application/pdf`
  - HTML: `text/html`
- **Google Sheets**:
  - CSV (first sheet only): `text/csv`
  - PDF Document: `application/pdf`
- **Google Slides**:
  - PDF Document: `application/pdf`

### Examples
- Export a Google Doc to plain text:
  ```bash
  gws drive files export --params '{"fileId": "doc_id_12345", "mimeType": "text/plain"}'
  ```
- Export a Google Sheet to CSV:
  ```bash
  gws drive files export --params '{"fileId": "sheet_id_12345", "mimeType": "text/csv"}'
  ```

---

## 5. Uploading Files (Write Operations)

Use the `gws drive +upload` helper command to upload local files.

> [!IMPORTANT]
> This is a **write** operation. Confirm with the user before uploading files.

### Usage
```bash
gws drive +upload <local_file_path> [flags]
```

- `--parent "<folder_id>"`: Target parent folder ID.
- `--name "<name>"`: Target filename on Drive (defaults to local filename).

### Example
```bash
gws drive +upload "./data.csv" --parent "folder_id_12345" --name "Q3 Sales Data.csv"
```
