---
name: SpreadsheetsSkill
description: Instruction guidelines and syntax examples for managing Google Sheets (reading values, creating sheets, appending rows, updating cell ranges, clearing values, and deleting files) using the gws CLI.
tools: [executeSessionCommand]
---

# Google Sheets Skill (gws CLI)

This skill instructs the agent on how to see, create, append, edit, and delete Google Sheets using the `gws` command-line utility.

## Prerequisites

- The `gws` CLI must be installed and authenticated.
- Always use the `executeSessionCommand` tool to execute `gws` commands.

## 1. Seeing/Reading Values (Read Operations)

To view spreadsheet values or metadata, you can use helper commands or the raw API.

### Reading Cell Ranges (Helper Command)
```bash
gws sheets +read --spreadsheet <ID> --range "<sheet_name>!<range>"
```
- Example (read A1 to C10 on Sheet1):
  ```bash
  gws sheets +read --spreadsheet 1a2b3c4d5e --range "Sheet1!A1:C10"
  ```

### Reading Cell Ranges (Raw API with Table Formatting)
This is recommended for displaying output in clean tables:
```bash
gws sheets spreadsheets values get --params '{"spreadsheetId": "<id>", "range": "<range>"}' --format table
```
- Example:
  ```bash
  gws sheets spreadsheets values get --params '{"spreadsheetId": "1a2b3c4d5e", "range": "Sheet1!A1:C10"}' --format table
  ```

### Getting Spreadsheet Metadata (Listing Tab Names)
Retrieve the structure of the spreadsheet (such as sheet/tab names and grid properties):
```bash
gws sheets spreadsheets get --params '{"spreadsheetId": "<id>"}'
```

---

## 2. Creating Spreadsheets (Create Operations)

Create a new blank spreadsheet.

> [!IMPORTANT]
> This is a **write** operation. Confirm with the user before executing.

### Usage
```bash
gws sheets spreadsheets create --json '{"properties": {"title": "<title>"}}'
```

### Example
```bash
gws sheets spreadsheets create --json '{"properties": {"title": "Q3 Sales Budget"}}'
```
*Note:* The response will contain the newly created `spreadsheetId` which is required for subsequent operations.

---

## 3. Appending Rows (Write Operations)

Use the `gws sheets +append` helper command to add new rows of data to the end of a sheet.

> [!IMPORTANT]
> This is a **write** operation. Confirm the rows to append with the user.

### Usage and Flags
```bash
gws sheets +append --spreadsheet <ID> [flags]
```
- `--values "<comma_separated_text>"`: A single row of simple string values.
- `--json-values "<json_array_of_arrays>"`: Bulk import of multiple rows.

### Examples
- Append a single row:
  ```bash
  gws sheets +append --spreadsheet 1a2b3c4d5e --values "John Doe,30,Sales"
  ```
- Append multiple rows in bulk:
  ```bash
  gws sheets +append --spreadsheet 1a2b3c4d5e --json-values '[["Jane Smith",28,"Marketing"],["Bob Johnson",35,"IT"]]'
  ```

---

## 4. Updating & Editing Ranges (Update/Write Operations)

Use `update` to overwrite specific cell ranges, or `clear` to delete cell values.

> [!IMPORTANT]
> Overwriting cell values can destroy existing formulas or data. Verify ranges and get user confirmation.

### Overwriting specific cell ranges
```bash
gws sheets spreadsheets values update --params '{"spreadsheetId": "<id>", "range": "<range>", "valueInputOption": "USER_ENTERED"}' --json '{"values": <array_of_arrays>}'
```
- `"valueInputOption"`: Supported values are `"USER_ENTERED"` (recommended; parses formulas like `=SUM()` and formats numbers/booleans) or `"RAW"` (treats everything as plain strings).

### Example
- Update cells A1 to B2 with headers and values:
  ```bash
  gws sheets spreadsheets values update --params '{"spreadsheetId": "1a2b3c4d5e", "range": "Sheet1!A1:B2", "valueInputOption": "USER_ENTERED"}' --json '{"values": [["Name", "Score"], ["Alice", 95]]}'
  ```

### Clearing values in a range
```bash
gws sheets spreadsheets values clear --params '{"spreadsheetId": "<id>", "range": "<range>"}'
```
- Example:
  ```bash
  gws sheets spreadsheets values clear --params '{"spreadsheetId": "1a2b3c4d5e", "range": "Sheet1!A2:C100"}'
  ```

---

## 5. Deleting Spreadsheets (Delete Operations)

Spreadsheets are stored as files in Google Drive. To delete a spreadsheet, you must use the Google Drive API.

> [!CAUTION]
> Deleting files is permanent. Always verify the spreadsheet ID and get explicit user consent before executing.

### Usage
```bash
gws drive files delete --params '{"fileId": "<SPREADSHEET_ID>"}'
```

### Example
```bash
gws drive files delete --params '{"fileId": "1a2b3c4d5e"}'
```

## Setup Instructions

### 1. Prerequisites & CLI Installation
- **gws CLI**: The Google Workspace CLI utility (`gws`) must be installed and available on system `PATH`.
- **Runtime**: Ensure Node.js or the required executable for `gws` is installed.

### 2. Google Sheets API Configuration
- **Google Cloud APIs**: Enable the **Google Sheets API** (`https://www.googleapis.com/auth/spreadsheets`) and **Google Drive API** (`https://www.googleapis.com/auth/drive`) in Google Cloud Console.
- **Authentication**:
  1. Authenticate `gws` with your Google account:
     ```bash
     gws auth login
     ```
  2. Verify access by creating or reading a spreadsheet:
     ```bash
     gws sheets spreadsheets create --json '{"properties": {"title": "Test Sheet"}}'
     ```
- **Formulas vs Raw Strings**: Set `valueInputOption: "USER_ENTERED"` when updating values to ensure formulas (e.g. `=SUM(A1:A10)`) and numeric types are interpreted correctly.

