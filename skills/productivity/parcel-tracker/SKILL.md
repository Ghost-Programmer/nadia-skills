---
name: parcel-tracker
description: Tracks inbound and outbound shipments across USPS, UPS, FedEx, DHL, and global postal carriers using the WhereParcel API, logging delivery milestones to the daily brief.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
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

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/productivity/parcel-tracker/scripts/parcel_tracker.py`.
- **Configuration Properties (`nadia.prop.*`)**:
  - Requires `nadia.prop.whereparcel.apiKey` in `~/.nadia/nadia.properties` (configure via **Settings ➔ Properties** or `setNadiaProperty`).

---

## 1. Core Operational Workflows

### 1.1 Tracking a Shipment by Carrier & Tracking Number (`track`)
Query the latest transit checkpoints and delivery status for a tracking number:

```bash
python ~/.nadia/skills/productivity/parcel-tracker/scripts/parcel_tracker.py track --carrier "us.usps" --tracking-number "9400100000000000000000"
```

- Common `--carrier` codes: `us.usps`, `us.ups`, `us.fedex`, `de.dhl`, `gb.royalmail`, `ca.canadapost`.

