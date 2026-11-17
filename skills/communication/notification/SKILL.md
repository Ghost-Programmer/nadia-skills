---
name: notification
description: Orchestrates multi-modal notifications including text-based chat reports, Slack channel alerts, visual Philips Hue pulses, and persistent system briefs.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: communication
  display-name: NotificationSkill
allowed-tools: flashHueAlert setHueLightState sendSlackNotification getSlackNotificationChannel storeBriefEntry appendBriefEntry
tools: [flashHueAlert, setHueLightState, sendSlackNotification, getSlackNotificationChannel, storeBriefEntry, appendBriefEntry]
---

# Notification Skill

This skill provides a unified interface for notifying the User of system events, task completions, scheduled job runs, or critical errors across digital channels (Chat, Slack, Briefs) and physical smart environments (Philips Hue Smart Lighting).

---

## Setup Instructions

### External App & Integration Setup

1. **Slack Socket Mode App Setup (Optional — Remote & Mobile Alerts)**:
   - Open [Slack API Apps](https://api.slack.com/apps) ➔ **Create New App ➔ From scratch** and select your workspace.
   - **Enable Socket Mode**: Navigate to **Settings ➔ Socket Mode**, toggle **Enable Socket Mode** ON, and generate an **App-Level Token** (`xapp-...`) with the `connections:write` scope.
   - **Configure Bot Scopes**: Navigate to **Features ➔ OAuth & Permissions** and add Bot Token Scopes: `chat:write`, `channels:read`, `channels:history`, `groups:history`, `im:history`, and `app_mentions:read`. Click **Install to Workspace** and copy the **Bot User OAuth Token** (`xoxb-...`).
   - **Invite Bot**: In Slack, invite the bot to your alert channel (e.g., `/invite @Nadia` in `#notifications`).
   - **Configure in Nadia**: Open **⚙️ System Settings ➔ Slack Integration** (or edit `~/.nadia/nadia.properties`):
     ```properties
     nadia.slack.enabled=true
     nadia.slack.bot-token=xoxb-...
     nadia.slack.app-token=xapp-...
     nadia.slack.allowed-users=U0123456789
     nadia.slack.notification-channel=#notifications
     ```
2. **Philips Hue Smart Bridge Setup (Optional — Ambient Visual Alerts)**:
   - Connect your Philips Hue Bridge to the same local subnet as Nadia (HTTP/HTTPS ports `80`/`443`).
   - Authorize the local network in **View ➔ 🌐 Network Engineer** (or call `approveCurrentNetwork()`).
   - Press the physical round **Link Button** on top of the Hue Bridge, then pair within 30 seconds in the **🌐 Network Engineer ➔ Philips Hue** panel (or call `pairHueBridge(bridgeIp)`).
3. **Nadia Briefs**:
   - Backed automatically by Nadia's configured relational database (**⚙️ System Settings ➔ Database Connection**).

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
