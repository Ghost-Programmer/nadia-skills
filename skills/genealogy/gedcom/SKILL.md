---
name: GedcomSkill
description: Guidelines and Python CLI references for parsing, validating, inspecting, and querying GEDCOM family tree files (5.5, 5.5.1, 7.0 standard formats), extracting individual vitals, pedigree trees, descendant lines, and detecting logical tree anomalies.
tools: [executeSessionCommand, searchMemory, saveMemory]
---

# GEDCOM Family Tree Parsing & Diagnostics Skill

This skill instructs the agent on how to parse, inspect, query, and validate GEDCOM format family tree data files (`.ged`), extracting individuals, family relationships, ancestral lineages, descendant trees, and chronological consistency anomalies.

The GEDCOM parser tool is implemented as a Python script located at `~/.nadia/skills/genealogy/gedcom/scripts/gedcom_tool.py` (or `./skills/genealogy/gedcom/scripts/gedcom_tool.py`).

## Setup Instructions

- **Python Runtime & Dependencies**:
  - Python 3.10+ installed and available on system `PATH`.
  - Built with pure Python standard library modules (`argparse`, `json`, `re`, `pathlib`, `collections`). No external pip dependencies required.
- **Script Location**:
  - `~/.nadia/skills/genealogy/gedcom/scripts/gedcom_tool.py`
  - Workspace relative path: `./skills/genealogy/gedcom/scripts/gedcom_tool.py` or `../skills/genealogy/gedcom/scripts/gedcom_tool.py`
- **File System Permissions**:
  - Read access to target `.ged` or `.gedcom` files within session directories or attached project folders.

---

## Operational Workflows

### 1. Tree Overview and Statistical Summary

When a user provides or asks about a GEDCOM file:

```bash
python ../skills/genealogy/gedcom/scripts/gedcom_tool.py summary --file "<path_to_file.ged>"
```

*Output summary provides:*
- Total individuals, families, and source citations.
- Gender breakdown (males, females, unknown).
- Timeline boundaries (earliest birth year, latest death year, average lifespan).
- Top 10 surnames and frequency distribution.

### 2. Inspecting Individual Profiles

To retrieve full vital events (birth, death, burial, christening), occupations, residences, parents, spouses, and children:

- By Individual XREF ID:
  ```bash
  python ../skills/genealogy/gedcom/scripts/gedcom_tool.py individual --file "<path_to_file.ged>" --id "@I1@"
  ```
- By Fuzzy Name Search:
  ```bash
  python ../skills/genealogy/gedcom/scripts/gedcom_tool.py individual --file "<path_to_file.ged>" --name "John Smith"
  ```

### 3. Inspecting Family Records

To inspect husband, wife, marriage dates/places, and all linked children:

```bash
python ../skills/genealogy/gedcom/scripts/gedcom_tool.py family --file "<path_to_file.ged>" --id "@F1@"
```

### 4. Recursive Pedigree & Descendant Exploration

- **Ancestors Tree (Direct Lineage)**:
  ```bash
  python ../skills/genealogy/gedcom/scripts/gedcom_tool.py ancestors --file "<path_to_file.ged>" --id "@I1@" --generations 4
  ```
- **Descendants Tree**:
  ```bash
  python ../skills/genealogy/gedcom/scripts/gedcom_tool.py descendants --file "<path_to_file.ged>" --id "@I1@" --generations 4
  ```

### 5. Multi-Criteria Individual Search

Search individuals across names, date spans, and locations:

```bash
python ../skills/genealogy/gedcom/scripts/gedcom_tool.py search --file "<path_to_file.ged>" --name "Smith" --birth-from 1850 --birth-to 1900 --place "Illinois" --limit 20
```

### 6. Logical Tree Validation & Anomaly Detection

Scan the entire GEDCOM tree for chronological contradictions, biologically improbable ages, and potential duplicate records:

```bash
python ../skills/genealogy/gedcom/scripts/gedcom_tool.py validate --file "<path_to_file.ged>"
```

*Detects and flags:*
- `CHRONOLOGY_ERROR`: Death date precedes birth date.
- `IMPOSSIBLE_LIFESPAN`: Lifespan > 120 years.
- `PARENT_BORN_AFTER_CHILD`: Child birth precedes parent birth.
- `IMPROBABLE_PARENT_AGE`: Parent age < 12 or mother age > 60 at child's birth.
- `BORN_AFTER_MOTHER_DEATH` / `BORN_AFTER_FATHER_DEATH`: Biological timeline violations.
- `POTENTIAL_DUPLICATES`: Same or similar names with overlapping birth dates.

---

## Execution Pattern

Use the `executeSessionCommand` tool to run the CLI commands, parsing the structured JSON output into clean Markdown tables, lists, and genealogical summaries for the user.
