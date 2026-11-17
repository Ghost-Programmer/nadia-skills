---
name: bambu
description: Guidelines and instructions for discovering, monitoring, controlling, and running 3D print jobs, analyzing HMS hardware errors, and tracking AMS multi-color filaments on Bambu 3D printers on the network.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: hardware
  display-name: BambuSkill
allowed-tools: listPrinters getPrinterStats startPrinterMonitor startPrintJob stopPrintJob pausePrintJob resumePrintJob
tools: [listPrinters, getPrinterStats, startPrinterMonitor, startPrintJob, stopPrintJob, pausePrintJob, resumePrintJob]
---

# Bambu 3D Printer Management Skill

This skill guides the agent in listing local Bambu printers, fetching telemetry and print metrics, analyzing HMS diagnostic hardware alerts, controlling active print jobs (start, stop, pause, resume), and initiating live visual dashboard monitor windows in the Nadia workspace.

---

## Setup Instructions

### External App & Integration Setup

1. **Prepare Your Bambu Lab 3D Printer (X1C, P1S, P1P, A1, A1 mini)**:
   - Power on the printer and connect it to the **same local Wi-Fi/LAN subnet** as Nadia.
   - On the printer touchscreen, navigate to **Settings (⚙️) ➔ Network / LAN Only Mode** and record:
     1. **IP Address** (assigning a DHCP reservation on your router is recommended)
     2. **Device Serial Number** (also visible in Bambu Studio / Bambu Handy under *Device ➔ Update / SN*)
     3. **8-Digit LAN Access Code**
   - *(Optional)* Enable **LAN Only Mode** for 100% local, cloud-free operation. Ensure local firewall allows outbound **TCP `8883`** (MQTT TLS), **TCP `6000` / `322`** (chamber camera video), and **UDP `1900` / `2021`** (SSDP discovery).
2. **Authorize Local Network (Zero-Trust Guard)**:
   - Nadia blocks all 3D printer MQTT, SSDP, and camera connections on unapproved networks (`status: "unapproved_network"`).
   - Open **View ➔ 🌐 Network Engineer** and click **Approve Current Network** (or invoke `approveCurrentNetwork()` from `NetworkSkill`).
3. **Register Printer in Nadia**:
   - Open **⚙️ System Settings ➔ Bambu 3D Printers**, enter the printer **Name**, **IP Address**, **Serial Number**, and **Access Code**, and click **Save**.

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
