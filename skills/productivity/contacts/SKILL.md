---
name: ContactsSkill
description: Instruction guidelines and syntax examples for managing Google Contacts (listing, searching, reading, creating, updating, and deleting) using the gws CLI.
tools: [executeSessionCommand]
---

# Google Contacts Skill (gws CLI)

This skill instructs the agent on how to list, search, read, create, update, and delete Google Contacts using the `gws` command-line utility.

## Prerequisites

- The `gws` CLI must be installed and authenticated.
- Always use the `executeSessionCommand` tool to execute `gws` commands.

## 1. Listing Contacts (List Operations)

Use the `gws people connections list` command to retrieve a list of the user's contacts.

### Usage and Flags
```bash
gws people connections list --params '{"resourceName": "people/me", "personFields": "<fields>"}' [flags]
```

- `"resourceName"`: Must always be `people/me` to represent the authenticated user.
- `"personFields"`: Comma-separated list of fields to return. Valid values: `names`, `emailAddresses`, `phoneNumbers`, `organizations`, `addresses`, `birthdays`, `metadata`, `biographies`.
- `"sortOrder"`: (Optional) Sort order of returned contacts. Supported: `FIRST_NAME_ASCENDING`, `LAST_NAME_ASCENDING`, `LAST_MODIFIED_DESCENDING`.
- `--format table`: Outputs the contact list in a clean, readable ASCII table (recommended for log scans).

### Example
- List all contacts with names, emails, and phone numbers in a table:
  ```bash
  gws people connections list --params '{"resourceName": "people/me", "personFields": "names,emailAddresses,phoneNumbers"}' --format table
  ```

---

## 2. Searching & Finding Contacts (Search Operations)

Use `gws people people searchContacts` to search for specific contacts matching query terms.

### Usage and Flags
```bash
gws people people searchContacts --params '{"query": "<term>", "readMask": "<fields>"}' [flags]
```

- `"query"`: The search term (matches prefix phrases of names, nicknames, email addresses, phone numbers, and organizations).
- `"readMask"`: Comma-separated list of fields to return (e.g. `names,emailAddresses,phoneNumbers`).
- `--format table`: Outputs the search results in a clean table format.

### Example
- Search for a contact named "John":
  ```bash
  gws people people searchContacts --params '{"query": "John", "readMask": "names,emailAddresses,phoneNumbers"}' --format table
  ```

---

## 3. Reading Specific Contact Details (Read Operations)

Use `gws people people get` to retrieve detailed information and the etag for a specific contact using their resource name ID (e.g., `people/c1234567890123456789`).

### Usage
```bash
gws people people get --params '{"resourceName": "people/<id>", "personFields": "<fields>"}'
```

### Example
```bash
gws people people get --params '{"resourceName": "people/c8976543210123456789", "personFields": "names,emailAddresses,phoneNumbers,metadata"}'
```

---

## 4. Creating New Contacts (Create/Write Operations)

Use `gws people people createContact` to add a new contact.

> [!IMPORTANT]
> Creating contacts is a **write** operation. Confirm the contact details with the user before executing.

### Usage
```bash
gws people people createContact --json '<person_object_json>'
```

### Example
- Create a contact with a name, email address, and phone number:
  ```bash
  gws people people createContact --json '{"names": [{"givenName": "Alice", "familyName": "Smith"}], "emailAddresses": [{"value": "alice.smith@example.com", "type": "work"}], "phoneNumbers": [{"value": "555-9876", "type": "mobile"}]}'
  ```

---

## 5. Updating & Editing Contacts (Update Operations)

Use `gws people people updateContact` to modify an existing contact.

> [!IMPORTANT]
> The Google People API requires the current contact's `etag` value to update fields safely and avoid conflicts. Always run `gws people people get` first to retrieve the current contact details and `etag`.

### Usage
```bash
gws people people updateContact --params '{"resourceName": "people/<id>", "updatePersonFields": "<fields_to_update>"}' --json '<updated_person_object_json>'
```

- `"updatePersonFields"`: Comma-separated list of fields that are being modified (e.g. `names,emailAddresses`). Only fields specified here will be overwritten.
- `"etag"`: The current ETag of the contact (must be included inside the `--json` body).

### Example
- Update Alice's email address (assuming ETag is `"%123456789"`):
  ```bash
  gws people people updateContact --params '{"resourceName": "people/c8976543210123456789", "updatePersonFields": "emailAddresses"}' --json '{"etag": "%123456789", "emailAddresses": [{"value": "alice.new@example.com", "type": "work"}]}'
  ```

---

## 6. Deleting Contacts (Delete Operations)

Use `gws people people deleteContact` to permanently remove a contact.

> [!CAUTION]
> Deletion is permanent. Always verify the contact name/ID and get user consent before executing.

### Usage
```bash
gws people people deleteContact --params '{"resourceName": "people/<id>"}'
```

### Example
- Delete a contact by ID:
  ```bash
  gws people people deleteContact --params '{"resourceName": "people/c8976543210123456789"}'
  ```
