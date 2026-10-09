---
name: DossierSkill
description: Build a comprehensive background dossier and biographical intelligence report on an individual using email, username, full name, contacts, RAG memory, social profile lookups (Facebook, GitHub, LinkedIn, X, Gravatar), web scraping, and interactive disambiguation via the Ask-Me skill. Use when asked to research a person, look up background details, build a dossier, or compile biographical profiles.
tools: [web_search, web_scrape, searchMemory, saveMemory, storeBriefEntry, appendBriefEntry, executeSessionCommand, getCurrentDateTime]
---

# Person Dossier & Intelligence Gathering Skill

This skill guides the agent in compiling a thorough, multi-source intelligence report and background dossier on an individual by leveraging the **Researcher** staff workflow, public web footprint lookups, email and handle profiling, Gravatar resolution, Google Contacts, internal episodic memory, and the **Ask-Me** interview protocol to resolve ambiguities and verify target identity.

---

## 1. Identity Resolution & Core Profile Channels

When initiating a dossier investigation, capture all available starting identifiers (Full Name, Email Address, Username/Handle, Affiliation/Company, Location, Phone Number).

### 1.1 Automated Profile & Social URL Formats

Construct direct lookup endpoints for known handles and email addresses:

- **Facebook**: `https://www.facebook.com/<username>/`
- **GitHub**: `https://github.com/<username>`
- **LinkedIn**: `https://www.linkedin.com/in/<username>`
- **X (Twitter)**: `https://x.com/<username>`
- **Gravatar (Username)**: `https://gravatar.com/<username>`
- **Gravatar (Email)**: `https://en.gravatar.com/<md5_hex_email>`
  - *MD5 Generation*: Lowercase and trim the email address before computing the 32-character hexadecimal MD5 hash (e.g. `user@example.com` → `https://en.gravatar.com/b4c347f82428848cf147c33947d12e2f`).
  - *Gravatar Avatar*: `https://www.gravatar.com/avatar/<md5_hex_email>?d=identicon&s=256`

### 1.2 Dossier Helper CLI

Execute the bundled Python helper script via `executeSessionCommand` to compute Gravatar hashes, generate platform links, and formulate targeted search queries:

```bash
python ../skills/research/dossier/scripts/dossier_helper.py --username "<username>" --email "<email>" --name "<full_name>" --company "<company>" --fetch-gravatar
```

---

## 2. Dossier Investigation Pipeline

Follow this structured investigation pipeline:

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. Ingest Identifiers & Generate Platform Target URLs       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Query Internal Memory & Google Contacts Directory        │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Execute Multi-Angle Web Searches (web_search)            │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Scrape Key Profiles, Bio Pages & Sites (web_scrape)      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Disambiguation & Ask-Me Grilling (If Identity Ambiguous) │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Render Standard Markdown Dossier Report                  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Persist Key Facts to Memory & Log Brief Entry            │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Internal Intelligence Search

1. **Episodic RAG Memory**:
   - Call `searchMemory` with query `"<full_name>"`, `"<email>"`, or `"<username>"` to surface prior notes, past conversations, project links, or personal context.
2. **Google Contacts (gws CLI)**:
   - Search address book via `executeSessionCommand`:

     ```bash
     gws people searchContacts --params '{"query": "<email_or_name>"}'
     ```

### Step 2: External Discovery & Search Strategy (`web_search`)

Run high-signal search queries across multiple angles:

- `"<Full Name>"` `"<Company or University>"`
- `"<Full Name>"` `"<Location or Title>"`
- `"<email@domain.com>"` (finds public commits, forum posts, author signatures)
- `"<username>" site:github.com OR site:linkedin.com OR site:x.com`
- `"<Full Name>" resume OR bio OR "about me"`

### Step 3: Deep Content Extraction (`web_scrape`)

- Call `web_scrape` on key identified URLs (LinkedIn public profiles, GitHub profile/pinned repos, personal websites, company team pages, conference bios, blog posts).
- Extract career trajectory, current role, location, educational background, public achievements, and social links.

### Step 4: Disambiguation & Ask-Me Grilling (If Identity is Ambiguous)

If web searches uncover multiple plausible individuals sharing the same name or handle, or if critical context is missing (such as distinguishing between two candidates in different industries or locations):

1. **Investigate Environment First**: Always run tool lookups (`searchMemory`, `web_search`, `web_scrape`) before asking the user.
2. **Ask-Me Interactive Protocol**: If ambiguity remains, present a focused round of questions strictly using the **Ask-Me** format to discern the correct identity:

   ```markdown
   ❓ **Q1** - **Disambiguate Target Identity**: Found multiple candidate profiles for "[Full Name]". Which individual are you investigating?
   - **Option A**: [Title] at [Company A] based in [Location A] (GitHub: `[handleA]`).
   - **Option B**: [Title] at [Company B] based in [Location B] (LinkedIn: `[handleB]`).
   - **Option C**: Neither (provide additional anchor details such as past company or email).

   ➡️ **Recommendation**: Option A matches the company/project context found in recent memory notes.
   ```

3. **Wait for Confirmation**: Once the user selects or clarifies the identity anchor, resume the pipeline to complete the target profile.

---

## 3. Standard Markdown Dossier Report Format

Present the final intelligence report adhering strictly to this standard Markdown template:

```markdown
# 👤 Person Dossier: [Full Name]

> **Entity Status**: [Verified | Partially Verified | Preliminary]  
> **Primary Affiliation**: [Current Title, Organization]  
> **Location**: [City, State / Country]  
> **Report Generated**: [YYYY-MM-DD] via Researcher & Dossier Skill

---

## 1. Executive Summary

[2–3 concise sentences summarizing who the person is, their primary domain of expertise, current role, and notable relevance.]

---

## 2. Profile & Identity Card

| Field | Details | Source / Verification |
| :--- | :--- | :--- |
| **Full Name** | [Full Legal / Professional Name] | [Source Link] |
| **Known Aliases / Handles** | `[handle1]`, `[handle2]` | [Platform / Bio] |
| **Primary Email** | `[email@example.com]` | [Source / Contacts] |
| **Secondary Emails** | `[other@domain.com]` | [GitHub Commits / Web] |
| **Phone Number(s)** | [Phone or "None public"] | [Source] |
| **Current Organization** | [Company / Institution Name] | [LinkedIn / Web] |
| **Primary Role / Title** | [Job Title] | [Current Role] |
| **Location / Base** | [City, Region, Country] | [Public Records / Social] |
| **Gravatar Profile** | [Gravatar Link](https://en.gravatar.com/<hash>) | [Gravatar Hash] |

---

## 3. Web & Social Footprint Matrix

| Platform | Profile URL | Status | Key Highlights |
| :--- | :--- | :--- | :--- |
| **LinkedIn** | [linkedin.com/in/<username>](https://www.linkedin.com/in/<username>) | [Active / Found / Not Found] | [Role, Connections, Summary] |
| **GitHub** | [github.com/<username>](https://github.com/<username>) | [Active / Found / Not Found] | [Top Repos, Primary Languages, Stars] |
| **X (Twitter)** | [x.com/<username>](https://x.com/<username>) | [Active / Found / Not Found] | [Bio, Follower count, Topics] |
| **Facebook** | [facebook.com/<username>/](https://www.facebook.com/<username>/) | [Found / Private / Not Found] | [Public details] |
| **Gravatar** | [gravatar.com/<username>](https://gravatar.com/<username>) | [Verified / Default] | [Associated accounts, Avatar image] |
| **Personal / Blog** | [example.com](https://example.com) | [Active] | [Domain, Topics covered] |

---

## 4. Professional Background & Career Trajectory

- **Current Position**: [Role, Company, Start Date – Present]
  - Key focus areas and responsibilities.
- **Previous Roles**:
  - **[Past Role]** — [Past Company] ([Start Year – End Year])
  - **[Past Role]** — [Past Company] ([Start Year – End Year])
- **Education & Credentials**:
  - [Degree / Field of Study], [University / Institution] ([Graduation Year])
  - Certifications, licenses, or specialized training.

---

## 5. Public Contributions, Projects & Media

- **Open Source / Code Projects**:
  - `[Project Name]`: [Brief summary, GitHub URL, stars/forks].
- **Publications, Articles & Talks**:
  - *[Article / Paper Title]* ([Year]) — [[Publisher / URL](URL)]
  - *[Conference Talk / Podcast]* — [[Event Link](URL)]
- **Notable News & Press Mentions**:
  - [Summary of press coverage with link].

---

## 6. Internal Memory & Interaction History

- **Contacts Record**: [Found in Google Contacts / Not in Contacts]
- **Episodic Memory Logs**:
  - [Key memory entries, past discussed topics, or projects involving this person from Nadia's RAG memory.]
- **Relationship / Context to User**: [Collaborator, Client, Vendor, Industry Contact, Unknown].

---

## 7. Key Synthesis & Insights

- **Primary Expertise**: [Core skills and domain strengths].
- **Communication Style / Preferences**: [Preferred channels, public engagement habits].
- **Network & Affiliations**: [Key communities, boards, organizations].

---

## 8. Verified Sources & Investigation Trail

1. [Source 1 Title](https://example.com/link1)
2. [Source 2 Title](https://example.com/link2)
3. [Source 3 Title](https://example.com/link3)
```

---

## 4. Post-Investigation Persistence

1. **Episodic Memory**:
   - Save essential facts to long-term memory via `saveMemory`:

     ```json
     {
       "content": "Dossier Profile for [Name] ([Company]): Email=[Email], GitHub=[GitHub], LinkedIn=[LinkedIn]. Primary expertise in [Field].",
       "category": "fact",
       "tags": "dossier, contact, [name_slug], [company_slug]"
     }
     ```

2. **Executive Brief**:
   - Log completion in the system brief via `storeBriefEntry`:

     ```json
     {
       "category": "research",
       "staffName": "Researcher",
       "code": "dossier_[name_slug]",
       "text": "- **Dossier Completed**: Compiled intelligence report for [Name] ([Company]). Profile verified across [Platforms]."
     }
     ```
