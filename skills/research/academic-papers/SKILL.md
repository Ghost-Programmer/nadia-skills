---
name: academic-papers
description: Searches peer-reviewed scientific papers, preprints, DOIs, citation counts, and book metadata across arXiv, Europe PMC, Crossref, and Open Library without requiring API keys.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.0"
  category: research
  display-name: AcademicPapersSkill
allowed-tools: executeSessionCommand storeBriefEntry searchMemory saveMemory
tools: [executeSessionCommand, storeBriefEntry, searchMemory, saveMemory]
properties: []
---

# Academic Literature & Scientific Preprints Skill (`arXiv`, `Europe PMC`, `Crossref` & `Open Library`)

This skill equips `@Researcher`, `@Journalist`, and `@Software Architect` to search scientific preprints on **[arXiv](https://info.arxiv.org/help/api/user-manual.html)**, biomedical and life-sciences literature on **[Europe PMC](https://europepmc.org/RestfulWebService)**, scholarly DOI metadata and citation counts on **[Crossref](https://api.crossref.org)**, and book editions on **[Open Library](https://openlibrary.org/developers/api)**.

---

## Setup Instructions

- **Python Runtime**: Python 3.10+ (uses standard library only).
- **Bundled Script**: `./skills/research/academic-papers/scripts/academic_search.py`.
- **Configuration Properties (`nadia.prop.*`)**: Keyless (`properties: []`). Works out-of-the-box with no API keys required.

---

## 1. Core Operational Workflows

### 1.1 Searching arXiv Preprints (`arxiv`)
Search Computer Science, Physics, Mathematics, Quantitative Finance, and AI preprints:

```bash
python ~/.nadia/skills/research/academic-papers/scripts/academic_search.py arxiv --query "retrieval augmented generation" --limit 10
```

### 1.2 Searching Europe PMC Biomedical & Scientific Literature (`europepmc`)
Search PubMed/PMC papers with abstracts, open-access PDF links, and citation counts:

```bash
python ~/.nadia/skills/research/academic-papers/scripts/academic_search.py europepmc --query "CRISPR gene editing" --limit 10
```

### 1.3 Resolving & Searching DOIs via Crossref (`crossref`)
Search scholarly works by keyword or resolve a specific DOI (`--doi`):

```bash
python ~/.nadia/skills/research/academic-papers/scripts/academic_search.py crossref --query "attention is all you need" --limit 5
```

### 1.4 Searching Books & ISBNs via Open Library (`books`)
Look up book metadata, authors, publication years, and ISBNs:

```bash
python ~/.nadia/skills/research/academic-papers/scripts/academic_search.py books --query "Designing Data-Intensive Applications" --limit 5
```

---

## 2. Citation & Dossier Standards

1. Always include the paper title, authors, publication year, venue/journal, citation count (when available), and direct URL or DOI link.
2. When compiling research dossiers (`@Researcher`), cross-verify preprints (`arXiv`) against published journal records (`Crossref` / `Europe PMC`).

