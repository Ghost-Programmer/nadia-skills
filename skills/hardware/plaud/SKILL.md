---
name: plaud
description: Guidelines and instructions for listing audio recordings and fetching transcripts/summaries directly from the Plaud voice recorder CLI.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: hardware
  display-name: PlaudSkill
allowed-tools: executeSessionCommand
tools: [executeSessionCommand]
---

# Plaud Transcript Management Skill

This skill allows the agent to interact with a Plaud voice recorder to retrieve voice recording details, transcripts, and summaries of recorded meetings by executing the Plaud CLI script directly.

---

## Setup Instructions

### External App & Integration Setup

- **Python 3.10+ Runtime**:
  - Install Python 3.10+ and ensure `python` is on system `PATH`:
    - **Windows**: `winget install Python.Python.3.12` (enable *"Add python.exe to PATH"*)
    - **macOS**: `brew install python`
    - **Linux**: `sudo apt install python3`
  - Uses Python's built-in standard library only (no `pip install` packages required).
- **Plaud Note Cloud & Developer SDK Credentials**:
  1. Sync your Plaud Note / Plaud NotePin recordings via the **PLAUD** mobile app so transcripts/summaries are uploaded to Plaud Cloud.
  2. Sign in to the [Plaud Developer Portal](https://platform-us.plaud.ai/), create an Embedded SDK Application, and copy your **Client ID** and **API Key**.
  3. Export `PLAUD_CLIENT_ID` and `PLAUD_API_KEY` in the host environment before launching Nadia:
     ```bash
     export PLAUD_CLIENT_ID="your_client_id_here"
     export PLAUD_API_KEY="your_api_key_here"
     ```
  4. *(Fallback)* When credentials are unset, `plaud_cli.py` runs safely in realistic Simulation Mode.
- **Bundled Script**: `~/.nadia/skills/hardware/plaud/scripts/plaud_cli.py`.

---

## Listing Recordings

When the user asks to see their audio files, voice recordings, or Plaud transcript list:

1. Call the `executeSessionCommand` tool passing the exact command line:

   ```bash
   python ~/.nadia/skills/hardware/plaud/scripts/plaud_cli.py list
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
   python ~/.nadia/skills/hardware/plaud/scripts/plaud_cli.py fetch --id [recordingId]
   ```

2. Parse the returned JSON object.
3. Present the returned content in a structured layout:
   - **Overview**: A high-level description of what was discussed.
   - **Key Bullet Points**: Major takeaways, action items, or conclusions.
   - **Detailed Transcript**: The full timestamped transcript text formatted with speakers (e.g., `[00:12] Alice: ...`).
