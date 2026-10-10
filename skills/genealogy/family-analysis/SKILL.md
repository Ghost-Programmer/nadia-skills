---
name: FamilyAnalysisSkill
description: Guidelines and Python CLI references for kinship calculation, Most Recent Common Ancestor (MRCA) discovery, shared autosomal DNA centiMorgan (cM) estimation, ASCII pedigree charts, and chronological family life timelines.
tools: [executeSessionCommand, searchMemory, saveMemory]
---

# Family Kinship & Lineage Analysis Skill

This skill instructs the agent on how to calculate precise genealogical relationships between family members, discover Most Recent Common Ancestors (MRCA), estimate theoretical shared autosomal DNA ranges (cM), render visual pedigree charts, and compile chronological family life timelines from GEDCOM data.

The family analysis tool is implemented as a Python script located at `~/.nadia/skills/genealogy/family-analysis/scripts/family_analyzer.py` (or `./skills/genealogy/family-analysis/scripts/family_analyzer.py`).

## Setup Instructions

- **Python Runtime & Dependencies**:
  - Python 3.10+ installed and available on system `PATH`.
  - Built with pure Python standard library modules (`argparse`, `json`, `collections`, `typing`, `pathlib`). No external pip dependencies required.
- **Script Location**:
  - `~/.nadia/skills/genealogy/family-analysis/scripts/family_analyzer.py`
  - Workspace relative path: `./skills/genealogy/family-analysis/scripts/family_analyzer.py` or `../skills/genealogy/family-analysis/scripts/family_analyzer.py`
- **Dependencies**:
  - Automatically interfaces with `gedcom_tool.py` located under `../gedcom/scripts/`.

---

## Operational Workflows

### 1. Calculating Exact Blood Relationship & Kinship

To determine the exact biological or legal kinship between two individuals:

```bash
python ../skills/genealogy/family-analysis/scripts/family_analyzer.py relationship --file "<path_to_file.ged>" --id1 "@I5@" --id2 "@I8@"
```

*JSON output provides:*
- Formal relationship title (e.g. `1st Cousin`, `2nd Cousin Once Removed`, `Great-Uncle`, `Half-Sister`, `Great-Grandmother`).
- Generation distances from the common ancestor down to each individual ($d_1$, $d_2$).
- List of Most Recent Common Ancestors (MRCA).
- DNA sharing estimates (average cM, 95% range min/max cM, percentage of shared DNA according to standard Shared cM Project benchmarks).

### 2. Identifying Most Recent Common Ancestor (MRCA)

To trace the common ancestors and path lengths connecting two individuals:

```bash
python ../skills/genealogy/family-analysis/scripts/family_analyzer.py mrca --file "<path_to_file.ged>" --id1 "@I5@" --id2 "@I8@"
```

### 3. Rendering ASCII / Markdown Pedigree Charts

To generate a clean, structured text-based pedigree chart for chat responses and reports:

```bash
python ../skills/genealogy/family-analysis/scripts/family_analyzer.py chart --file "<path_to_file.ged>" --id "@I5@" --generations 3
```

*Example Output:*
```
Pedigree Chart for: Robert Smith (1910-1985)
============================================================
1. [Self] Robert Smith (1910-1985)
   ├── 2. [Father] William Smith (1880-1955)
   │   ├── 4. [Paternal Grandfather] John Smith (1850-1920)
   │   └── 5. [Paternal Grandmother] Mary Johnson (1855-1930)
   └── 3. [Mother] Sarah Miller (1882-1960)
       ├── 6. [Maternal Grandfather] Unknown
       └── 7. [Maternal Grandmother] Unknown
```

### 4. Compiling Chronological Family Unit Timelines

To generate a unified chronological life timeline (births, christenings, marriages, children's births, parent passings, census appearances, death):

```bash
python ../skills/genealogy/family-analysis/scripts/family_analyzer.py timeline --file "<path_to_file.ged>" --id "@I3@"
```

---

## Execution Pattern

Use `executeSessionCommand` to execute the Python script. Present the resulting kinship details, DNA statistics, and visual pedigree trees to the user in formatted Markdown tables and diagrams.
