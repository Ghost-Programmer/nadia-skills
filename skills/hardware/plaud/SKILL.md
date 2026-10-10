---
name: PlaudSkill
description: Guidelines and instructions for listing audio recordings and fetching transcripts/summaries directly from the Plaud voice recorder CLI.
tools: [executeSessionCommand]
---

# Plaud Transcript Management Skill

This skill allows the agent to interact with a Plaud voice recorder to retrieve voice recording details, transcripts, and summaries of recorded meetings by executing the Plaud CLI script directly.

## Setup Instructions

- **Python Runtime**:
  - Python 3.10+ installed and on system `PATH`.
  - Script located at `./skills/plaud/scripts/plaud_cli.py`.
- **Authentication**:
  - Log in to the [Plaud Developer Portal](https://platform-us.plaud.ai/) and create an Embedded SDK Application.
  - Set `PLAUD_CLIENT_ID` and `PLAUD_API_KEY` in your environment or `.env` file in the workspace root:
    ```env
    PLAUD_CLIENT_ID=your_client_id_here
    PLAUD_API_KEY=your_api_key_here
    ```
- **Simulation Fallback**:
  - If credentials are not configured, the script automatically executes in realistic Simulation Mode.

---

## Listing Recordings

When the user asks to see their audio files, voice recordings, or Plaud transcript list:

1. Call the `executeSessionCommand` tool passing the exact command line:

   ```bash
   python ./skills/plaud/scripts/plaud_cli.py list
   ```

2. Parse the returned JSON array of recordings.
3. Format the response as a clean Markdown table including:
   - **ID**: The recording identifier (e.g., `rec-001`).
   - **Title**: The title of the recording (e.g., *Weekly Engineering Standup*).
   - **Date**: The date of the recording.
   - **Duration**: Length of the audio (e.g., *15m 30s*).
   - **Overview Summary**: A short, single-sentence summary of the meeting.

## Fetching a Specific Transcript

When the user wants to read a transcript, review meeting notes, or retrieve summaries for a specific recording ID:

1. Call the `executeSessionCommand` tool passing the exact command line:

   ```bash
   python ./skills/plaud/scripts/plaud_cli.py fetch --id [recordingId]
   ```

2. Parse the returned JSON object.
3. Present the returned content in a structured layout:
   - **Overview**: A high-level description of what was discussed.
   - **Key Bullet Points**: Major takeaways, action items, or conclusions.
   - **Detailed Transcript**: The full timestamped transcript text formatted with speakers (e.g., `[00:12] Alice: ...`).
