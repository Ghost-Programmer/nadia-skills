---
name: hue
description: Instructions on how to discover Philips Hue Bridges, pair via the link button, list and control connected smart lights, manage room groups, set colors/brightness, and trigger visual ambient alert notifications.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: hardware
  display-name: PhilipsHueSmartLightingSkill
allowed-tools: discoverHueBridges pairHueBridge listHueLights setHueLightState listHueRooms setHueRoomState flashHueAlert
tools: [discoverHueBridges, pairHueBridge, listHueLights, setHueLightState, listHueRooms, setHueRoomState, flashHueAlert]
---

# Philips Hue Smart Lighting & Ambient Control Guidelines

Use this skill when interacting with smart home lighting, managing Philips Hue Bridges, adjusting room illumination, setting scene colors, or triggering visual alert flashes for build notifications, alarms, and focus modes.

---

## Setup Instructions

### External App & Integration Setup

1. **Connect Philips Hue Bridge to Local LAN**:
   - Plug your Philips Hue Bridge into the same local router/subnet as Nadia via Ethernet and ensure lights/rooms are configured in the official **Philips Hue** mobile app.
   - Ensure local LAN HTTP/HTTPS ports `80` and `443` on the Hue Bridge are reachable from the Nadia host.
2. **Approve Local Subnet (Zero-Trust Guard)**:
   - Open **View ➔ 🌐 Network Engineer** and approve the active network (or call `approveCurrentNetwork()` from `NetworkSkill`), which also auto-detects local Hue Bridges via ARP/mDNS.
3. **Pair Nadia with the Hue Bridge (One-Time Physical Button Press)**:
   - Run `discoverHueBridges()` (or open **View ➔ 🌐 Network Engineer ➔ Philips Hue**).
   - Press the large round **physical Link Button** on top of your Philips Hue Bridge, then invoke `pairHueBridge(bridgeIp)` (or click **Pair Bridge** in the UI) within **30 seconds**. Nadia persists the generated application key automatically in its database.

---

## Guidelines

1. **Bridge Discovery & Authentication**:
   - Call `discoverHueBridges` to locate local Hue hubs on the subnet via cloud broker discovery and local ARP inspection.
   - **Troubleshooting Local Discovery**: If `discoverHueBridges` reports no bridges on the local LAN, check if the subnet is authorized using `checkNetworkApproval` or view saved bridge records using `listApprovedNetworks` from `NetworkSkill`. If unapproved, approve the subnet via `approveCurrentNetwork`.
   - If the bridge is not yet paired, instruct the user to press the large round button on top of their Philips Hue Bridge, then immediately invoke `pairHueBridge(bridgeIp)` within 30 seconds.
   - Once paired, credentials are permanently saved and used for all future operations.

2. **Inspecting Lights & Rooms**:
   - Call `listHueLights` to get a list of all connected bulbs, lightstrips, and lamps with their current power state (ON/OFF), brightness %, and active color.
   - Call `listHueRooms` to see all configured rooms/zones (e.g. "Office", "Living Room", "Bedroom").

3. **Controlling Lights & Rooms**:
   - Use `setHueLightState` for individual light fixtures (e.g., turning on/off, setting brightness from 1-100%, or changing color).
   - Use `setHueRoomState` to adjust all lights in an entire room simultaneously (e.g., turning on the Office lights to 80% warm white).
   - Color values can be passed as named colors (e.g., `red`, `blue`, `green`, `cyan`, `magenta`, `yellow`, `orange`, `purple`, `warm white`, `cool white`, `daylight`, `relax`, `candlelight`) or hex color codes (e.g., `#FF4500`, `#00E5FF`).

4. **Visual Ambient Alerts (`flashHueAlert`)**:
   - Use `flashHueAlert` to signal key system events to the user:
     - Short green pulse on successful build/test completion.
     - Short red pulse on build error or test failure.
     - Pulse alert on long-running task completion or alarm trigger.
