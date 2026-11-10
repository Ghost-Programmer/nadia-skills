---
name: bambu
description: Guidelines and instructions for discovering, monitoring, controlling, and running 3D print jobs, analyzing HMS hardware errors, and tracking AMS multi-color filaments on Bambu 3D printers on the network.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: hardware
  display-name: BambuSkill
allowed-tools: listPrinters getPrinterStats startPrinterMonitor startPrintJob stopPrintJob pausePrintJob resumePrintJob
tools: [listPrinters, getPrinterStats, startPrinterMonitor, startPrintJob, stopPrintJob, pausePrintJob, resumePrintJob]
---

# Bambu 3D Printer Management Skill

This skill guides the agent in listing local Bambu printers, fetching telemetry and print metrics, analyzing HMS diagnostic hardware alerts, controlling active print jobs (start, stop, pause, resume), and initiating live visual dashboard monitor windows in the Nadia workspace.

## Setup Instructions

- **Network & Connectivity**:
  - Bambu 3D Printer (X1-Carbon, P1P, P1S, A1) powered on and connected to the local LAN.
  - MQTT port 8883 (TLS) accessible from host to printer IP.
  - **Zero-Trust Network Approval Requirement**: To prevent rogue or untrusted network interactions, Nadia strictly enforces zero-trust network safety. **If on an unapproved network, Bambu integrations will NOT attempt to connect** (no MQTT connections on port 8883, no UDP SSDP discovery broadcasts, no TLS camera video streams, and no print job commands). Configured printers on unapproved subnets are reported with status `"unapproved_network"`.
  - The local subnet must be connected and authorized in Nadia's database (`checkNetworkApproval` / `approveCurrentNetwork` from `NetworkSkill`).
  - Approval **requires an active network connection** and will fail if the host machine has no network (disconnected/offline, loopback-only, or unknown gateway).
- **Printer Configuration**:
  - Configure printer IP Address, Serial Number, and Access Code (available on printer LCD under Settings -> Network).
  - Set `BAMBU_PRINTER_IP` and `BAMBU_ACCESS_CODE` in `application.yml` or `~/.nadia/config.json`.
- **LAN Only Mode**:
  - Optional: Enable "LAN Only Mode" on the printer for 100% cloud-free local control.

---

## 1. Listing & Discovering 3D Printers

When the user asks to find, list, or discover 3D printers on the network:

1. **Verify Network Approval**: Ensure the active network is connected and approved. If the network is unapproved or offline, `listPrinters` will suppress SSDP broadcast sweeps and return any configured printers marked as `"unapproved_network"`. Do NOT attempt repeated connection loops if the network is unapproved.
2. Call `listPrinters` (requires no arguments). Native discovery sends UDP SSDP broadcasts on ports 1900 and 2021 when the network is approved.
   - *Note*: If discovering printers across mixed 2D/3D fleets using `scanForPrinters` (`NetworkSkill`), verify that the network is authorized via `checkNetworkApproval` or approved via `approveCurrentNetwork`.
3. Present the returned list of printers (their IP addresses, models, serial numbers, and online states) in a clean Markdown table. If any printers show status `unapproved_network`, inform the user that network approval is required before connections can be established.

---

## 2. Viewing Real-Time Printer Telemetry & Status

When the user requests to inspect print progress, temperatures, or metrics for a specific printer:

1. Call `getPrinterStats` passing the target printer's `ip`.
   - **Unapproved Network Behavior**: If on an unapproved network or disconnected, `getPrinterStats` will refuse to establish an MQTT socket and immediately returns `status: "unapproved_network"` along with an explanatory error. If simulated alerts exist for offline diagnostics, they are surfaced safely without network activity.
2. Report the telemetry in a clear, formatted breakdown:
   - **Active Model / File**: e.g., `gear_assembly.gcode`
   - **Status/State**: e.g., `Printing`, `Idle`, `Paused`, `Preparing`, `Completed`, `Cancelled`, or `Unapproved Network`
   - **Layer Progress**: e.g., `Layer 149 / 350 (42.5%)`
   - **Estimated Time Remaining (ETA)**: e.g., `35m` or `Done`
   - **Thermal Climate**: Nozzle (`220°C / 220°C`), Bed (`60°C / 60°C`), Chamber (`38°C`)
   - **Fan Speeds**: Part Cooling (`100%`), Auxiliary Fan (`80%`), Chamber Exhaust (`50%`)
   - **AMS Filament Slots**: Spool materials (PLA, PETG, PLA-CF, Support), colors, and remaining percentages
   - **Speed Mode**: e.g., `Standard`, `Sport`, `Ludicrous`, `Silent`
   - **HMS Alerts**: Active hardware errors or diagnostic alerts

---

## 3. Starting and Controlling 3D Print Jobs

When the user directs to start, pause, resume, or cancel a 3D print job:

- **Approval Requirement**: All job commands verify network approval upfront. If the network is unapproved, commands return an error with `status: "unapproved_network"` without initiating socket connections.
- **Start Job**: Call `startPrintJob` with `ip` and optional `filename` (e.g. `startPrintJob(ip: "192.168.1.50", filename: "gear_housing.gcode")`).
- **Pause Job**: Call `pausePrintJob` with `ip`.
- **Resume Job**: Call `resumePrintJob` with `ip`.
- **Stop / Cancel Job**: Call `stopPrintJob` with `ip`.

---

## 4. Visual Dashboard Monitoring & Camera Streaming

When the user asks to monitor a printer or open a status window/dashboard:

1. Call `startPrinterMonitor` passing the printer's `ip` address to launch the graphical monitor dashboard window.
2. **Camera Streaming**: The live TLS video stream (port 6000) strictly enforces zero-trust authorization. If on an unapproved network, camera creation is blocked, the camera view displays `🚫 UNAPPROVED NETWORK`, and socket connections are prevented until network approval is granted.
