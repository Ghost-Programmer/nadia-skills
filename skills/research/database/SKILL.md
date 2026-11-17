---
name: database
description: Guidelines and tool references for listing database connections, inspecting database schemas, and executing SQL queries against user connections by name.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: research
  display-name: DatabaseQuerySkill
allowed-tools: getDatabaseConnectionsList getDatabaseSchema executeDatabaseQuery
tools: [getDatabaseConnectionsList, getDatabaseSchema, executeDatabaseQuery]
---

# Database Querying Skill

This skill allows the agent to discover configured database connections and execute schema inspections and SQL queries against them (supporting PostgreSQL, MySQL, MariaDB, SQLite, or H2).

---

## Setup Instructions

### External App & Integration Setup

1. **Supported Relational Databases**:
   - Nadia ships with built-in JDBC drivers for **PostgreSQL**, **MySQL**, **MariaDB**, **SQLite**, and **H2** (no extra driver JAR installation needed).
2. **Register External Database Connections in Nadia**:
   - Open **⚙️ System Settings ➔ Database Connection**.
   - Click **New / Add Connection** and enter:
     - **Connection Name** (used when calling `getDatabaseSchema` / `executeDatabaseQuery`)
     - **Driver / Engine** (`PostgreSQL`, `MySQL`, `MariaDB`, `SQLite`, or `H2`)
     - **Host, Port, Database Name, Username & Password** (using a dedicated **read-only** database user is strongly recommended for analytics/inspection).
   - Click **Test Connection** to verify network reachability and credentials, then click **Save**.

---

## Execution Guidelines

1. **Discover Connections First**: If you do not know which database connections are available, call the `getDatabaseConnectionsList` tool. This lists the connection names and a note explaining what each database contains. Choose the connection name that is relevant to the user's request.
2. **Schema Inspection**: Always inspect the schema using the `getDatabaseSchema` tool, passing the correct `connectionName`, before writing any SQL queries. This ensures you write valid queries for the target table names and columns.
3. **Specify Connection Name**: Every query or schema call requires the `connectionName` parameter. Do not make assumptions about the active database name.
4. **Read-Only Focus**: Prefer read-only SQL queries (`SELECT`) where possible to prevent accidental data modification.
5. **Paging and Filtering**: When query results could be large, make sure to add `LIMIT` or filter clauses to fetch only necessary records. Although execution outputs are capped to 100 rows by the tool to avoid context window flooding, you should still practice query hygiene.
6. **Driver Dialect**: Adapt your SQL queries to the target driver type (visible in the connections list) to handle dialect differences.
