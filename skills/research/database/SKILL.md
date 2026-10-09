---
name: DatabaseQuerySkill
description: Guidelines and tool references for listing database connections, inspecting database schemas, and executing SQL queries against user connections by name.
tools: [getDatabaseConnectionsList, getDatabaseSchema, executeDatabaseQuery]
---

# Database Querying Skill

This skill allows the agent to discover configured database connections and execute schema inspections and SQL queries against them (supporting PostgreSQL, MySQL, MariaDB, SQLite, or H2).

## Execution Guidelines

1. **Discover Connections First**: If you do not know which database connections are available, call the `getDatabaseConnectionsList` tool. This lists the connection names and a note explaining what each database contains. Choose the connection name that is relevant to the user's request.
2. **Schema Inspection**: Always inspect the schema using the `getDatabaseSchema` tool, passing the correct `connectionName`, before writing any SQL queries. This ensures you write valid queries for the target table names and columns.
3. **Specify Connection Name**: Every query or schema call requires the `connectionName` parameter. Do not make assumptions about the active database name.
4. **Read-Only Focus**: Prefer read-only SQL queries (`SELECT`) where possible to prevent accidental data modification.
5. **Paging and Filtering**: When query results could be large, make sure to add `LIMIT` or filter clauses to fetch only necessary records. Although execution outputs are capped to 100 rows by the tool to avoid context window flooding, you should still practice query hygiene.
6. **Driver Dialect**: Adapt your SQL queries to the target driver type (visible in the connections list) to handle dialect differences.
