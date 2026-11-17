---
name: wordpress
description: Guidelines for managing WordPress content, posts, pages, media, menus, comments, taxonomies, SEO metadata, and plugins via Model Context Protocol (MCP) servers (primary) or the standalone wordpress_api.py CLI script (fallback).
license: Apache-2.0
compatibility: Compatible with agentskills.io open standard and Nadia Cognitive Agent Platform.
metadata:
  author: Miller Software Solutions LLC
  version: "2.1"
  category: media
  display-name: WordPressSkill
allowed-tools: listMcpServers, listMcpServerTools, callMcpServerTool, listMcpServerResources, readMcpServerResource, getWordpressSitesList, executeSessionCommand
tools: [listMcpServers, listMcpServerTools, callMcpServerTool, listMcpServerResources, readMcpServerResource, getWordpressSitesList, executeSessionCommand]
---

# WordPress CMS Skill (MCP Primary & REST CLI Fallback)

This skill instructs the agent on how to inspect, draft, publish, and manage WordPress websites using **Model Context Protocol (MCP)** as the primary integration path, with the standalone Python CLI script (`wordpress_api.py`) as a fallback for legacy non-MCP sites.

---

## Setup Instructions

### External App & Integration Setup

1. **Primary Path — WordPress Model Context Protocol (MCP) Server**:
   - Install and activate an MCP server plugin on your WordPress site (for example, **Easy MCP AI**, which exposes Streamable HTTP at `https://<your-site>/wp-json/easy-mcp-ai/v1/mcp`).
   - In Nadia, open **⚙️ System Settings ➔ MCP Servers** (stored in `~/.nadia/mcp_config.json`):
     1. Set **Name** to `wordpress` and **Transport** to `http`.
     2. Enter your WordPress MCP endpoint URL.
     3. Authenticate via **OAuth 2.0 PKCE** or add an `Authorization=Bearer ${nadia.prop.wordpress.token}` header (saving `nadia.prop.wordpress.token` in **⚙️ System Settings ➔ Properties**).
     4. Click **Test & Discover Tools** and **Save** so `mcp_wordpress_*` tools register in Nadia.
2. **Fallback Path — WordPress REST API & Application Password (`wordpress_api.py`)**:
   - Install **Python 3.10+** and required HTTP client libraries:
     ```bash
     pip install requests urllib3
     ```
   - In your WordPress Admin Dashboard, navigate to **Users ➔ Profile ➔ Application Passwords**, enter `Nadia AI`, click **Add New Application Password**, and copy the generated 24-character password for use with `wordpress_api.py` (`~/.nadia/skills/media/wordpress/scripts/wordpress_api.py`).

---

## 1. Primary Path: WordPress via Model Context Protocol (MCP)

Nadia connects directly to WordPress MCP servers (such as Easy MCP AI at `https://www.mymiller.name/wordpress/wp-json/easy-mcp-ai/v1/mcp`, configured under the server name `wordpress`) using Streamable HTTP with OAuth 2.0 PKCE or Bearer API Key authentication.

### 1.1 Discovering WordPress MCP Tools
1. **Direct Bridged Tools (`mcp_wordpress_*`)**:
   - Check your `Available Tools` list for tools prefixed with `mcp_wordpress_` (e.g., `mcp_wordpress_create_post`, `mcp_wordpress_update_post`, `mcp_wordpress_get_posts`, etc.). You can invoke these tools directly.
2. **Dynamic MCP Inspection (`listMcpServers` & `listMcpServerTools`)**:
   - Call `listMcpServers()` to check all configured MCP servers and confirm the `wordpress` server is enabled.
   - Call `listMcpServerTools(serverName: "wordpress")` to discover all tools exposed by the WordPress MCP server along with their exact input JSON schemas.
   - Call `listMcpServerResources(serverName: "wordpress")` and `readMcpServerResource(serverName: "wordpress", uri: "...")` to read any site resources exposed via MCP.

### 1.2 Executing WordPress Actions via MCP
Invoke either the bridged `mcp_wordpress_<toolName>` tool directly or call `callMcpServerTool`:

```json
{
  "tool_calls": [
    {
      "function": "callMcpServerTool",
      "parameters": {
        "serverName": "wordpress",
        "toolName": "<tool_name_from_listMcpServerTools>",
        "jsonArguments": "{\"title\": \"Breaking Story Headline\", \"content\": \"<p>Article HTML body...</p>\", \"status\": \"draft\"}"
      }
    }
  ]
}
```

### 1.3 Editorial Best Practices with WordPress MCP
- **Avoid Duplicate Posts on Living Stories**: Before creating a post for a developing story, search existing posts/drafts via MCP to check if a post already exists. If it does, update the existing post by ID.
- **Categories, Tags & SEO Metadata**: Query existing categories and tags via MCP before assigning taxonomy IDs, and populate slug, excerpt, and SEO metadata fields when supported by the server's MCP tools.
- **Default to Draft Unless Instructed**: Unless the user explicitly requests immediate publication (`status: "publish"`), create new articles with `status: "draft"` and return the draft preview link and Post ID.

---

## 2. Fallback Path: Standalone Python REST CLI (`wordpress_api.py`)

If a target WordPress site is not configured as an MCP server, check `getWordpressSitesList()` or run the standalone Python CLI script `wordpress_api.py` via `executeSessionCommand`.

### Basic Syntax

```bash
python ../skills/media/wordpress/scripts/wordpress_api.py --url "<site_url>" --password "<password>" --method <GET|POST|PUT|DELETE> --endpoint "<relative_path>"
```

### Options

- `--url`: WordPress site base URL (e.g. `https://example.com`).
- `--password`: WordPress Application Key/Password.
- `--method`: HTTP request method (`GET`, `POST`, `PUT`, `DELETE`).
- `--endpoint`: Target REST API path relative to `/wp-json/` (e.g. `/wp/v2/posts`).
- `--params`: Query parameters as a JSON string.
- `--body`: Post body fields as a JSON string.

## Post and Page Status Options

- `publish`: Published and publicly visible.
- `future`: Scheduled to be published in the future.
- `draft`: Saved as a draft.
- `pending`: Pending editorial review.
- `private`: Privately visible only to authorized roles.
- `trash`: Sent to trash.
