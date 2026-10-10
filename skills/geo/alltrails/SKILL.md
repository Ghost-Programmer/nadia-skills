---
name: AllTrailsSkill
description: Guidelines for searching trails, looking up hiking routes, difficulty levels, elevation gains, reviews, and trail conditions using the AllTrails MCP Client.
tools: []
---

# AllTrails MCP Skill

This skill provides instructions for the agent when users query outdoor trails, hiking paths, backpacking routes, trail difficulty, elevation profiles, trail reviews, and current route conditions.

## Setup Instructions

- **AllTrails MCP Server Connection**:
  - Configure the AllTrails MCP server endpoint in `application.yml` or `mcp_config.json` (defaults to `https://www.alltrails.com/mcp` or local MCP sidecar).
  - Outbound internet access to AllTrails endpoints.
- **Optional API Credentials**:
  - Set `ALLTRAILS_API_KEY` or MCP bearer token if using authenticated premium features.

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
