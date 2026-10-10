---
name: PhilipsHueSmartLightingSkill
description: Instructions on how to discover Philips Hue Bridges, pair via the link button, list and control connected smart lights, manage room groups, set colors/brightness, and trigger visual ambient alert notifications.
tools: [discoverHueBridges, pairHueBridge, listHueLights, setHueLightState, listHueRooms, setHueRoomState, flashHueAlert]
---
# Philips Hue Smart Lighting & Ambient Control Guidelines

Use this skill when interacting with smart home lighting, managing Philips Hue Bridges, adjusting room illumination, setting scene colors, or triggering visual alert flashes for build notifications, alarms, and focus modes.

## Setup Instructions

- **Bridge Network Connectivity**:
  - Philips Hue Bridge connected to the same local subnet as Nadia.
  - HTTP port 80 / HTTPS port 443 open on the Bridge.
- **Initial Pairing**:
  - Call `discoverHueBridges` to locate the bridge IP.
  - Press the physical link button on top of the bridge, then invoke `pairHueBridge(bridgeIp)` within 30 seconds to generate and persist the `HUE_APPLICATION_KEY`.
- **Configuration**:
  - Credentials saved in `~/.nadia/config.json` or `application.yml` under `nadia.hue.application-key`.

---

## Guidelines

1. **Bridge Discovery & Authentication**:
   - Call `discoverHueBridges` to locate local Hue hubs on the subnet.
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
