---
name: PlaudSkill
description: Guidelines and instructions for listing audio recordings and fetching transcripts/summaries directly from the Plaud voice recorder CLI.
tools: [executeSessionCommand]
---

# Plaud Transcript Management Skill

This skill allows the agent to interact with a Plaud voice recorder to retrieve voice recording details, transcripts, and summaries of recorded meetings by executing the Plaud CLI script directly.

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

## Authentication Setup

To connect the Plaud CLI script to the live Plaud developer platform instead of running in simulated/mock mode:

1. **Plaud Developer Portal**: Log in to the [Plaud Developer Portal](https://platform-us.plaud.ai/) and create an Embedded SDK Application.
2. **Obtain Keys**: Go to App Settings > API Keys to generate your Client ID and API Key.
3. **Configure Environment Variables**:
   - Save the credentials in a local `.env` file in the workspace root directory:

     ```env
     PLAUD_CLIENT_ID=your_client_id_here
     PLAUD_API_KEY=your_api_key_here
     ```

   - *Note*: The `.env` file is already listed in `.gitignore` to prevent credentials from being committed to source control.
4. **Database Storage Fallback**: Alternatively, you can save the settings to the SQLite database via setting keys `plaud_client_id` and `plaud_api_key` using layout/system settings.
5. **Simulation Fallback**: If no credentials are found or configured, the script automatically runs in **Simulation Mode** using local realistic voice recordings to maintain local functionality.
