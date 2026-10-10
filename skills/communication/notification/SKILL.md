---
name: NotificationSkill
description: Orchestrates multi-modal notifications including text-based chat reports, Slack channel alerts, visual Philips Hue pulses, and persistent system briefs.
tools: [flashHueAlert, setHueLightState, sendSlackNotification, getSlackNotificationChannel, storeBriefEntry, appendBriefEntry]
---

# Notification Skill

This skill provides a unified interface for notifying the User of system events, task completions, scheduled job runs, or critical errors across digital channels (Chat, Slack, Briefs) and physical smart environments (Philips Hue Smart Lighting).

## Setup Instructions

- **Slack Integration**:
  - Set `SLACK_BOT_TOKEN` or `SLACK_WEBHOOK_URL` in your environment or `~/.nadia/config.json`.
  - Ensure the bot is invited to target notification channels (e.g. `/invite @Nadia`).
  - Configure default channel in `application.yml` via `nadia.slack.default-channel` (defaults to `#notifications`).
- **Philips Hue Smart Lighting**:
  - Configure Hue Bridge IP in `application.yml` under `nadia.hue.bridge-ip` or via discovery.
  - Set `HUE_APPLICATION_KEY` or pair with the bridge by pressing the physical link button during initial setup.
  - Verify local LAN connectivity to the bridge on port 80/443.
- **Briefs & Database**:
  - Ensure Nadia Brief repository database is initialized (configured in `application.yml`).

---

## 1. Operational Modalities

### A. Visual Alerts (Physical Environment)

Use `flashHueAlert` to provide high-signal, low-latency ambient awareness without requiring the user to monitor screen logs or chat windows.

- **Success (Green)**: Use for successful builds, completed background tasks, or passed tests.
  - *Pattern*: `flashHueAlert(lightIdOrAll='all', alertDuration='short')` + (Optional) `setHueLightState(color='green')`.
- **Failure (Red/Pulse)**: Use for errors, failed Docker containers, or broken builds.
  - *Pattern*: `flashHueAlert(lightIdOrAll='all', alertDuration='long')`.

### B. Slack Notifications (Remote & Mobile Alerting)

Use `sendSlackNotification` to dispatch structured, real-time alerts directly to the designated Slack notification channel (or an explicitly provided target channel).

- **Designated Channel**: Automatically delivers to the configured default Slack notification channel (e.g. `#notifications` or `#general`).
- **Channel Override**: Optionally specify the `channel` parameter (e.g. `channel="#alerts"`, `channel="#dev-feed"`, or channel ID `C0123456789`).
- **Formatting**: Format messages with clear Markdown headers, bold highlights, status emojis (`✅`, `⚠️`, `🚨`, `🚀`), and actionable links or code blocks (automatically converted to Slack mrkdwn).
- *Pattern*: `sendSlackNotification(message="🚀 *Build Complete*: Successfully packaged Nadia artifacts. Unit tests passed.")`
- *Pattern with Override*: `sendSlackNotification(message="🚨 *Critical Alert*: Database failover triggered.", channel="#urgent-alerts")`

### C. Digital Briefs (Asynchronous Log)

Use the `BriefSkill` integration (`storeBriefEntry`, `appendBriefEntry`) to record a permanent trail of notifications in the system database for retrospective analysis or morning briefings.

- **Category**: `notifications` or `system_events`.
- **Content**: Timestamp, Event Type, and Severity.

### D. Chat Notifications (Synchronous/Immediate)

For immediate interactive feedback within the active desktop session, use structured Markdown headers and callout blocks (`> [!NOTE]`, `> [!WARNING]`, `> [!CAUTION]`).

## 2. Notification Logic & Thresholds

| Event Type | Priority | Primary Modality | Secondary Modality |
| :--- | :--- | :--- | :--- |
| **Task Completion** | Low | Chat (Markdown) | Brief Entry |
| **Build/Test Success** | Medium | Visual (Green Pulse) | Slack (`sendSlackNotification`) / Brief Entry |
| **Scheduled Job Summary** | Medium | Slack (`sendSlackNotification`) | Brief Entry |
| **System Error / Failure** | High | Visual (Red Pulse) + Slack (`sendSlackNotification`) | Chat (Warning Block) + Brief Entry |
| **Security Alert / Critical Error** | Critical | Slack (`sendSlackNotification`) + Visual (Long Pulse) | Chat (Critical Callout) + Brief Entry |

## 3. Execution Guidelines

1. **Avoid Notification Fatigue**: Do not trigger visual pulses or Slack messages for routine conversational filler. Only send notifications for state changes, milestones, scheduled job results, or failures.
2. **Contextual Grounding**: When notifying about an error or failure, always provide the immediate error trace, affected component, and suggested resolution in the Slack message.
3. **Graceful Fallbacks & Resilience**: If a notification modality fails (e.g., Slack service disabled, tokens missing, or Hue Bridge unreachable), fall back immediately to Desktop Chat and Brief entries without interrupting task execution.
4. **Setup Verification**: Use `getSlackNotificationChannel` to check if Slack notifications are enabled and verify the active channel before attempting bulk alert dispatches.

---
