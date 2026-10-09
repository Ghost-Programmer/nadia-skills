import sys
import json
import argparse
import os

# Mock database of Plaud recordings and transcripts
MOCK_RECORDINGS = [
    {
        "id": "rec-001",
        "title": "Product Architecture Sync",
        "date": "2026-08-20",
        "duration": "25m 12s",
        "summary": "Discussion on migrating from Maven to Gradle and virtual thread performance optimizations."
    },
    {
        "id": "rec-002",
        "title": "Weekly Engineering Standup",
        "date": "2026-08-22",
        "duration": "12m 45s",
        "summary": "Team updates on Bambu printer skill integration and JavaFX taskbar customizations."
    },
    {
        "id": "rec-003",
        "title": "Bambu Printer Troubleshooting",
        "date": "2026-08-22",
        "duration": "8m 30s",
        "summary": "Reviewing simulated print state bugs and fixing bed temperature status checks."
    }
]

MOCK_DETAILS = {
    "rec-001": {
        "id": "rec-001",
        "title": "Product Architecture Sync",
        "overview": "Detailed planning session reviewing the backend build architecture migration to Gradle 9.1 and using virtual thread task executors for JavaFX chat models to avoid UI thread blocking.",
        "key_points": [
            "Migrated from Maven to Gradle to improve build times and dependency resolution caching.",
            "Wired chat request processing using Executors.newVirtualThreadPerTaskExecutor() to eliminate thread starvation.",
            "Added defensive try-catch handlers in similarity search tasks to survive DNS/network drops gracefully."
        ],
        "transcript": "[00:02] Jeff: Welcome everyone. Today we are looking at our system performance limits.\n"
                      "[01:15] Sarah: Right, the old ThreadPoolExecutor was blocking the main JavaFX Application thread when Ollama requests timed out.\n"
                      "[02:40] Jeff: Switching to Spring AI's chatClient with virtual threads will solve that. Let's make sure the client timeout is increased to 15 minutes for larger local models.\n"
                      "[04:10] Sarah: Yes, and we need to wrap the similarity recall logic. If the local host 'jeffs-mbp.lan' is unresolvable, it shouldn't crash the session."
    },
    "rec-002": {
        "id": "rec-002",
        "title": "Weekly Engineering Standup",
        "overview": "Short sync covering active project tasks: introducing the Bambu 3D printer management dashboard skill, simplifying brief markdown templates, and implementing a staff run toggle.",
        "key_points": [
            "Created the Bambu CLI and service to manage printers via status telemetry.",
            "Simplified the Brief skill output format to produce clean Markdown text without decorative fluff.",
            "Built a taskbar ToggleButton widget to enable/disable background staff scheduler tasks."
        ],
        "transcript": "[00:05] Jeff: Morning team, let's start status updates.\n"
                      "[00:45] Bob: I finished setting up the Bambu printer dashboard view using TilesFX controls. The gauge displays live progress, and the gauge refresh timeline disposes cleanly.\n"
                      "[02:15] Sarah: Excellent. I updated the Brief skill instructions to emit pure markdown. The user requested no extra fluff.\n"
                      "[03:30] Jeff: I added a pause toggle button to the bottom taskbar so we can halt staff service runs. They default to paused now, as requested."
    },
    "rec-003": {
        "id": "rec-003",
        "title": "Bambu Printer Troubleshooting",
        "overview": "Debugging session analyzing connection timeouts and temperature polling bugs during simulation of the Bambu Carbon X1-Carbon.",
        "key_points": [
            "Identified that nozzle temperature target state was reporting null during preparing stages.",
            "Fixed state progress advancing algorithm to reference epoch timestamps correctly.",
            "Wired BambuMonitorEvent to launch stage dock widgets smoothly."
        ],
        "transcript": "[00:10] Bob: I'm seeing a null nozzle target temperature whenever progress is under 1%.\n"
                      "[01:22] Jeff: Ah, the state file stores the start time. If elapsed time is extremely small, it stays in 'Preparing'. We should default target temp to 0.0 in that state.\n"
                      "[02:05] Bob: Got it. I updated the python simulation logic to handle target temperatures based on progress. Tested it and it returns correctly now."
    }
}

def main():
    parser = argparse.ArgumentParser(description="Plaud Voice Recorder Transcripts CLI")
    parser.add_argument("command", choices=["list", "fetch"])
    parser.add_argument("--id", help="Recording ID to fetch")
    args = parser.parse_args()

    # In a production scenario, we would retrieve PLAUD_CLIENT_ID / PLAUD_API_KEY from environment variables
    # or properties and perform requests to: https://platform-us.plaud.ai/api/v1/recordings/
    client_id = os.getenv("PLAUD_CLIENT_ID")
    api_key = os.getenv("PLAUD_API_KEY")

    if args.command == "list":
        # Simulate live fetching or mock fallback
        if client_id and api_key:
            # Placeholder for actual HTTP connection details
            pass
        print(json.dumps(MOCK_RECORDINGS, indent=2))
        return 0

    elif args.command == "fetch":
        if not args.id:
            print(json.dumps({"error": "Recording ID is required for fetch command"}, indent=2))
            return 1

        details = MOCK_DETAILS.get(args.id)
        if not details:
            print(json.dumps({"error": f"Recording not found for ID: {args.id}"}, indent=2))
            return 1

        print(json.dumps(details, indent=2))
        return 0

if __name__ == "__main__":
    sys.exit(main())
