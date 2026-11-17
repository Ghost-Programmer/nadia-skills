---
name: alltrails
description: Guidelines for searching trails, looking up hiking routes, difficulty levels, elevation gains, reviews, and trail conditions using the AllTrails MCP Client.
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "1.1"
  category: geo
  display-name: AllTrailsSkill
tools: []
---

# AllTrails MCP Skill

This skill provides instructions for the agent when users query outdoor trails, hiking paths, backpacking routes, trail difficulty, elevation profiles, trail reviews, and current route conditions.

---

## Setup Instructions

### External App & Integration Setup

1. **Configure AllTrails MCP Server in Nadia**:
   - Open **⚙️ System Settings ➔ MCP Servers** in Nadia (persisted in `~/.nadia/mcp_config.json`).
   - Add a new MCP server named `alltrails`:
     - **Transport**: `http` (Streamable HTTP) pointing to `https://www.alltrails.com/mcp` (or `stdio` if running a local AllTrails MCP adapter).
     - **Authentication (Optional)**: If using authenticated AllTrails Plus/Peak features, store your token in **⚙️ System Settings ➔ Properties** (e.g., `nadia.prop.alltrails.token`) and add header `Authorization=Bearer ${nadia.prop.alltrails.token}` in the MCP server configuration.
   - Click **Test & Discover Tools** and **Save** so `mcp_alltrails_*` tools are bridged into Nadia's `ToolRegistry`.

---

## Model Context Protocol (MCP) Integration

AllTrails is integrated dynamically as a Spring AI MCP Client connected to `https://www.alltrails.com/mcp`.
All available MCP tools from the AllTrails MCP server are automatically discovered, registered in the `ToolRegistry`, and made available to the agent during execution.

## Execution Guidelines

1. **Trail Discovery & Searching**:
   - When users ask to find trails near a specific city, state, national park, or geographic coordinate, utilize the discovered AllTrails search tools.
   - Filter by user criteria such as difficulty (Easy, Moderate, Hard), route type (Loop, Out & Back, Point to Point), activity (Hiking, Trail Running, Mountain Biking), or length.

2. **Trail Information & Details**:
   - For specific trails, retrieve key details:
     - Distance and estimated completion time.
     - Elevation gain / profile.
     - Route description and highlights (e.g. waterfalls, summit views, dog-friendly, kid-friendly).
     - Recent trail conditions, seasonal closures, or advisory notices.

3. **Output Presentation**:
   - Present trail recommendations clearly using markdown headers, bullet points, and tables.
   - Include relevant metrics (miles/km, elevation gain, difficulty rating, and trail links/coords).
