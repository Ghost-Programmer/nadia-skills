---
name: record-matching
description: Guidelines and Python CLI references for comparing family historical records (Census, Vital Statistics, Find A Grave, SSDI, Parish Registers) against GEDCOM tree individuals using multi-factor probabilistic scoring, Soundex phonetics, nickname aliasing, and household relational reinforcement.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: genealogy
  display-name: RecordMatchingSkill
allowed-tools: executeSessionCommand searchMemory saveMemory
tools: [executeSessionCommand, searchMemory, saveMemory]
---

# Genealogical Record Matching & Historical Comparison Skill

This skill instructs the agent on how to compare, evaluate, and correlate historical documents (Census, Vital Statistics, Find A Grave, Social Security Death Index, Parish Registers, Military Draft Cards) against family tree profiles. It performs multi-factor probabilistic scoring, Soundex phonetic matching, nickname alias resolution, geographic hierarchy comparison, and household relationship reinforcement.

The record matching tool is implemented as a Python script located at `~/.nadia/skills/genealogy/record-matching/scripts/record_matcher.py` (or `./skills/genealogy/record-matching/scripts/record_matcher.py`).

---

## Setup Instructions

### External App & Integration Setup

- **Python 3.10+ Runtime**:
  - Install Python 3.10+ and ensure `python` is on system `PATH`:
    - **Windows**: `winget install Python.Python.3.12` (enable *"Add python.exe to PATH"*)
    - **macOS**: `brew install python`
    - **Linux**: `sudo apt install python3`
  - Uses Python's built-in standard library only (no `pip install` packages required).
- **GEDCOM & Historical Record Inputs**:
  - Export a `.ged` tree file from **Ancestry**, **MyHeritage**, **Gramps**, or **RootsMagic** into `~/.nadia/session/`, and ensure the companion `gedcom` skill (`~/.nadia/skills/genealogy/gedcom/scripts/gedcom_tool.py`) is installed.
- **Bundled Script**: `~/.nadia/skills/genealogy/record-matching/scripts/record_matcher.py`.

---

## Operational Workflows

### 1. Matching an Individual Against a Historical Record

When evaluating whether a historical record (e.g. Census entry, death record) belongs to a specific person in a family tree:

```bash
python ../skills/genealogy/record-matching/scripts/record_matcher.py match-record \
  --file "<path_to_file.ged>" \
  --id "@I3@" \
  --name "Bill Smith" \
  --birth-year 1880 \
  --place "Chicago, IL" \
  --spouse "Sarah Miller" \
  --record-type "1910 Federal Census"
```

*Or pass record data via JSON string:*
```bash
python ../skills/genealogy/record-matching/scripts/record_matcher.py match-record \
  --file "<path_to_file.ged>" \
  --id "@I3@" \
  --record-json '{"name": "William Smith", "birth_year": 1880, "place": "Cook County, IL", "spouse_name": "Sarah Miller", "record_type": "1900 US Census"}'
```

*Evaluation Breakdown:*
- **Composite Match Score**: 0.0% – 100.0%
- **Confidence Level**: `VERY_HIGH` ($\ge 82\%$), `HIGH` ($\ge 70\%$), `MODERATE` ($\ge 55\%$), `LOW` ($\ge 40\%$), `UNLIKELY` ($< 40\%$)
- **Factor Scores**:
  - Name similarity (Exact, Nickname alias mapping e.g. William $\leftrightarrow$ Bill, Soundex phonetic)
  - Birth/Death date proximity with variance tolerance
  - Geographic token overlap (State, County, City)
  - Relational household reinforcement (matching spouse / parents / children in record)
- **Genealogical Proof Standard (GPS) Assessment**: Written synthesis explaining evidence correlation.

### 2. Searching the Entire Tree for Record Matches

When a historical record is found and you need to search the entire tree for the most likely person it belongs to:

```bash
python ../skills/genealogy/record-matching/scripts/record_matcher.py search-matches \
  --file "<path_to_file.ged>" \
  --name "Margaret Smith" \
  --birth-year 1885 \
  --place "Chicago, IL" \
  --spouse "James Davis" \
  --limit 5
```

### 3. Comparing Two GEDCOM Trees for Common Matches

When comparing two independent trees or GEDCOM files to identify overlapping ancestors or duplicate branches:

```bash
python ../skills/genealogy/record-matching/scripts/record_matcher.py compare-trees \
  --file1 "<path_to_tree1.ged>" \
  --file2 "<path_to_tree2.ged>" \
  --min-score 65.0
```

---

## Execution Pattern

Use `executeSessionCommand` to run the comparison engine. Format the resulting match breakdown, discrepancy notes, and GPS evidentiary conclusions into structured tables for the user.
