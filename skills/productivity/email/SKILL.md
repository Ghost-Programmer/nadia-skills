---
name: email
description: Instruction guidelines and syntax examples for managing Gmail messages (listing/triaging, reading, sending, replying, replying-all, and forwarding) using the gws CLI.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: productivity
  display-name: EmailSkill
allowed-tools: executeSessionCommand
tools: [executeSessionCommand]
---

# Gmail Email Skill (gws CLI)

This skill instructs the agent on how to list, read, send, reply to, and forward email messages using the `gws` command-line utility.

---

## Setup Instructions

### External App & Integration Setup (`gws` Google Workspace CLI)

1. **Install Node.js & Google Workspace CLI (`gws`)**:
   - Install **Node.js 20+** (`https://nodejs.org/`), then install `@googleworkspace/cli` globally and ensure `gws` is on system `PATH`:
     ```bash
     npm install -g @googleworkspace/cli
     gws --version
     ```
2. **Enable Gmail API in Google Cloud Console**:
   - Open [Google Cloud Console — API Library](https://console.cloud.google.com/apis/library), select or create a project, and enable **Gmail API** (scope: `https://mail.google.com/`).
   - Under **APIs & Services ➔ Credentials**, create an **OAuth 2.0 Client ID** (*Desktop app*)—or run `gws auth setup` if `gcloud` CLI is installed to provision credentials automatically.
3. **Authenticate & Verify**:
   - Sign in from a terminal so OAuth tokens are cached for `executeSessionCommand`:
     ```bash
     gws auth login
     gws gmail +triage --max 5 --format table
     ```
4. **Real-Time Gmail IMAP IDLE Push Setup (Optional — Zero-Polling Inbound Triage)**:
   - In your Google Account ([myaccount.google.com/security](https://myaccount.google.com/security)), enable **2-Step Verification**, then visit [Google App Passwords](https://myaccount.google.com/apppasswords) to generate a 16-character App Password.
   - In Gmail Settings (*See all settings ➔ Forwarding and POP/IMAP*), ensure **IMAP access** is enabled.
   - Open **⚙️ System Settings ➔ System Settings** in Nadia (or edit `~/.nadia/nadia.properties`):
     ```properties
     gmail.push.enabled=true
     gmail.username=your.email@gmail.com
     gmail.password=abcd efgh ijkl mnop
     ```

---

## 1. Listing & Triaging Emails (List Operations)

Use the `gws gmail +triage` helper command to list, search, and summarize incoming emails.

### Usage and Flags
```bash
gws gmail +triage [flags]
```

- `--query "<search_terms>"`: Search query. Defaults to `is:unread`. Supports standard Gmail search syntax (e.g. `from:boss`, `subject:urgent`).
- `--max <N>`: Maximum number of messages to list (default: 20).
- `--labels`: Include labels associated with each message in the output.
- `--format table`: Outputs the message summary in a clean, readable table.

### Examples
- List recent unread emails:
  ```bash
  gws gmail +triage --format table
  ```
- Search for the last 5 emails from a specific sender:
  ```bash
  gws gmail +triage --max 5 --query "from:manager@example.com" --format table
  ```

---

## 2. Reading Emails (Read Operations)

Use the `gws gmail +read` helper command to read the full body and headers of a specific email message.

### Usage and Flags
```bash
gws gmail +read --id <MESSAGE_ID> [flags]
```

- `--id <MESSAGE_ID>`: The unique Gmail message ID to retrieve (required).
- `--headers`: Include metadata headers (From, To, Subject, Date) in the output.
- `--html`: Returns the raw HTML body instead of converting it to plain text.
- `--format json`: Outputs the raw message JSON (useful for custom extraction/piping).

### Examples
- Read plain text content of a message:
  ```bash
  gws gmail +read --id 18f1a2b3c4d
  ```
- Read message content including headers:
  ```bash
  gws gmail +read --id 18f1a2b3c4d --headers
  ```

---

## 3. Sending New Emails (Send Operations)

Use the `gws gmail +send` helper command to send a new email.

> [!IMPORTANT]
> This is a **write** operation. Get user confirmation before executing.

### Usage and Flags
```bash
gws gmail +send --to <emails> --subject "<text>" --body "<text>" [flags]
```

- `--to "<emails>"`: Comma-separated list of recipient email addresses (required).
- `--subject "<text>"`: The email subject line (required).
- `--body "<text>"`: The message body (plain text, or HTML if `--html` is set) (required).
- `--cc "<emails>"`: CC recipient email addresses, comma-separated.
- `--bcc "<emails>"`: BCC recipient email addresses, comma-separated.
- `--html`: Treats the body string as HTML formatting.
- `--attach "<file_path>"`: Attach a local file (repeat the flag for multiple files, up to 25MB total).
- `--draft`: Saves the email as a draft in Gmail instead of sending it immediately.

### Examples
- Send a simple email:
  ```bash
  gws gmail +send --to "recipient@example.com" --subject "Status Update" --body "Everything is running smoothly."
  ```
- Send an HTML email with an attachment:
  ```bash
  gws gmail +send --to "client@example.com" --subject "Q2 Report" --body "Please find the <b>Q2 Report</b> attached." --html -a "Q2_Report.pdf"
  ```

---

## 4. Replying & Replying-All (Reply Operations)

Use `gws gmail +reply` or `gws gmail +reply-all` to respond to a message. Both commands handle threading and reference headers automatically.

> [!IMPORTANT]
> Replying is a **write** operation. Always confirm the message contents with the user before sending.

### Usage and Flags
```bash
gws gmail +reply --message-id <ID> --body "<text>" [flags]
gws gmail +reply-all --message-id <ID> --body "<text>" [flags]
```

- `--message-id <ID>`: The Gmail message ID you are replying to (required).
- `--body "<text>"`: The reply body (plain text, or HTML if `--html` is set) (required).
- `--to "<emails>"` / `--cc "<emails>"` / `--bcc "<emails>"`: Add additional recipients.
- `--attach "<file_path>"`: Attach a file (repeat the flag for multiple files).
- `--draft`: Saves the reply as a draft instead of sending it.
- `--remove "<emails>"`: (*reply-all only*) Excludes specified recipients from the reply list.

### Examples
- Reply to a message:
  ```bash
  gws gmail +reply --message-id 18f1a2b3c4d --body "Thanks for the update. I will look into it."
  ```
- Reply-all with cc, omitting one person:
  ```bash
  gws gmail +reply-all --message-id 18f1a2b3c4d --body "Agree with the plan." --cc "partner@example.com" --remove "unrelated@example.com"
  ```

---

## 5. Forwarding Emails (Forward Operations)

Use the `gws gmail +forward` helper command to forward an existing email.

> [!IMPORTANT]
> Forwarding is a **write** operation. Always get user confirmation before executing.

### Usage and Flags
```bash
gws gmail +forward --message-id <ID> --to <emails> [flags]
```

- `--message-id <ID>`: The Gmail message ID to forward (required).
- `--to "<emails>"`: Comma-separated list of recipient email addresses (required).
- `--body "<text>"`: Optional introductory text to place above the forwarded content.
- `--no-original-attachments`: Excludes any files attached to the original message.
- `--attach "<file_path>"`: Attach additional local files to the forward.
- `--draft`: Saves the forwarded email as a draft.

### Example
- Forward an email with a custom intro:
  ```bash
  gws gmail +forward --message-id 18f1a2b3c4d --to "review@example.com" --body "Forwarding this client inquiry for review."
  ```

---

## 6. Managing Email Labels (Label Operations)

Use Gmail labels to categorize and manage email messages and threads.

### Listing All Mailbox Labels
Retrieve a list of all user-defined and system labels.
```bash
gws gmail users labels list --params '{"userId": "me"}' --format table
```

### Retrieving a Specific Label
```bash
gws gmail users labels get --params '{"userId": "me", "id": "<label_id>"}'
```

### Creating a Label
Create a new custom label.
> [!IMPORTANT]
> This is a **write** operation. Confirm with the user before executing.
```bash
gws gmail users labels create --params '{"userId": "me"}' --json '{"name": "<label_name>", "labelListVisibility": "labelShow", "messageListVisibility": "show"}'
```

### Updating a Label
Rename or modify visibility settings of a label.
```bash
gws gmail users labels update --params '{"userId": "me", "id": "<label_id>"}' --json '{"id": "<label_id>", "name": "<new_label_name>"}'
```

### Deleting a Label
> [!CAUTION]
> Deleting a label is permanent. However, it only deletes the label itself; the messages associated with it will NOT be deleted. Confirm with the user.
```bash
gws gmail users labels delete --params '{"userId": "me", "id": "<label_id>"}'
```

### Modifying Labels on Specific Messages
Add or remove labels from a specific message ID (e.g. to mark as read or archive).
```bash
gws gmail users messages modify --params '{"userId": "me", "id": "<message_id>"}' --json '{"addLabelIds": [<labels_to_add>], "removeLabelIds": [<labels_to_remove>]}'
```

#### Examples
- **Mark an email as read** (remove `UNREAD` label):
  ```bash
  gws gmail users messages modify --params '{"userId": "me", "id": "18f1a2b3c4d"}' --json '{"removeLabelIds": ["UNREAD"]}'
  ```
- **Archive an email** (remove `INBOX` label):
  ```bash
  gws gmail users messages modify --params '{"userId": "me", "id": "18f1a2b3c4d"}' --json '{"removeLabelIds": ["INBOX"]}'
  ```
- **Star an email and apply a custom label** (add `STARRED` and `PROJECT` labels):
  ```bash
  gws gmail users messages modify --params '{"userId": "me", "id": "18f1a2b3c4d"}' --json '{"addLabelIds": ["STARRED", "LABEL_PROJECT_ID"]}'
  ```
