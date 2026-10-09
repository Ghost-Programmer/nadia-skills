---
name: BambuSkill
description: Guidelines and instructions for discovering, monitoring, controlling, and running 3D print jobs, analyzing HMS hardware errors, and tracking AMS multi-color filaments on Bambu 3D printers on the network.
tools: [listPrinters, getPrinterStats, startPrinterMonitor, startPrintJob, stopPrintJob, pausePrintJob, resumePrintJob]
---

# Bambu 3D Printer Management Skill

This skill guides the agent in listing local Bambu printers, fetching telemetry and print metrics, analyzing HMS diagnostic hardware alerts, controlling active print jobs (start, stop, pause, resume), and initiating live visual dashboard monitor windows in the Nadia workspace.

---

## 1. Listing & Discovering 3D Printers

When the user asks to find, list, or discover 3D printers on the network:

1. Call `listPrinters` (requires no arguments).
2. Present the returned list of printers (their IP addresses, models, serial numbers, and online states) in a clean Markdown table.

---

## 2. Viewing Real-Time Printer Telemetry & Status

When the user requests to inspect print progress, temperatures, or metrics for a specific printer:

1. Call `getPrinterStats` passing the target printer's `ip`.
2. Report the telemetry in a clear, formatted breakdown:
   - **Active Model / File**: e.g., `gear_assembly.gcode`
   - **Status/State**: e.g., `Printing`, `Idle`, `Paused`, `Preparing`, `Completed`, `Cancelled`
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

- **Start Job**: Call `startPrintJob` with `ip` and optional `filename` (e.g. `startPrintJob(ip: "192.168.1.50", filename: "gear_housing.gcode")`).
- **Pause Job**: Call `pausePrintJob` with `ip`.
- **Resume Job**: Call `resumePrintJob` with `ip`.
- **Stop / Cancel Job**: Call `stopPrintJob` with `ip`.

---

## 4. Visual Dashboard Monitoring

When the user asks to monitor a printer or open a status window/dashboard:

1. Call `startPrinterMonitor` passing the printer's `ip` address.
2. Confirm to the user that the graphical monitor dashboard window is being opened for the printer at that IP address.
