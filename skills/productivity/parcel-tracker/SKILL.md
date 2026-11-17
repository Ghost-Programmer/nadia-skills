---
name: parcel-tracker
description: Tracks inbound and outbound shipments across USPS, UPS, FedEx, DHL, and global postal carriers using the WhereParcel API, logging delivery milestones to the daily brief.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: productivity
  display-name: ParcelTrackerSkill
allowed-tools: executeSessionCommand storeBriefEntry searchMemory saveMemory getNadiaProperty setNadiaProperty
tools: [executeSessionCommand, storeBriefEntry, searchMemory, saveMemory, getNadiaProperty, setNadiaProperty]
properties: [nadia.prop.whereparcel.apiKey]
---

# Parcel & Shipment Tracking Skill (`WhereParcel`)

This skill enables `@Personal Assistant` to track packages across USPS, UPS, FedEx, DHL, and international postal carriers using **[WhereParcel](https://whereparcel.com/docs)** and update the executive morning brief when deliveries arrive or experience transit exceptions.

---

## Setup Instructions

### External App & Integration Setup

- **Python 3.10+ Runtime**:
  - Install Python 3.10+ and ensure `python` is on system `PATH`:
    - **Windows**: `winget install Python.Python.3.12` (enable *"Add python.exe to PATH"*)
    - **macOS**: `brew install python`
    - **Linux**: `sudo apt install python3`
  - Uses Python's built-in standard library only (no `pip install` packages required).
- **WhereParcel API Key (`nadia.prop.whereparcel.apiKey` — Required)**:
  1. Create an account at [WhereParcel](https://whereparcel.com/) and generate a REST API key from your developer dashboard.
  2. Open **⚙️ System Settings ➔ Properties** in Nadia (or call `setNadiaProperty`) and configure:
     ```properties
     nadia.prop.whereparcel.apiKey=your_whereparcel_api_key
     ```
- **Bundled Script**: `~/.nadia/skills/productivity/parcel-tracker/scripts/parcel_tracker.py`.

---

## 1. Core Operational Workflows

### 1.1 Tracking a Shipment by Carrier & Tracking Number (`track`)
Query the latest transit checkpoints and delivery status for a tracking number:

```bash
python ~/.nadia/skills/productivity/parcel-tracker/scripts/parcel_tracker.py track --carrier "us.usps" --tracking-number "9400100000000000000000"
```

- Common `--carrier` codes: `us.usps`, `us.ups`, `us.fedex`, `de.dhl`, `gb.royalmail`, `ca.canadapost`.
