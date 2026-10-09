---
name: WordPressSkill
description: Guidelines and CLI commands for managing WordPress content, media, menus, comments, settings, plugins, and custom fields using the standalone wordpress_api.py script.
tools: [executeSessionCommand]
---

# WordPress REST API Skill (Python CLI)

This skill instructs the agent on how to manage WordPress websites by running the pre-existing standalone Python CLI script `wordpress_api.py` located in the skill directory `./skills/wordpress/scripts/`.

All execution commands require passing direct connection parameters (`--url`, `--username`, and `--password`). Obtain these credentials directly from the user's prompt instructions or conversation context.

## Execution Pattern

Call the `executeSessionCommand` tool to run the CLI script. Specify the target connection parameters directly.

### Basic Syntax

```bash
python ../skills/wordpress/scripts/wordpress_api.py --url "<site_url>" --password "<password>" --method <GET|POST|PUT|DELETE> --endpoint "<relative_path>"
```

### Options

- `--url`: WordPress site base URL (e.g. `https://example.com`).
- `--password`: WordPress Application Key/Password (e.g. `xxxx xxxx xxxx xxxx xxxx xxxx`).
- `--method`: HTTP request method (defaults to `GET`).
- `--endpoint`: Target REST API path relative to `/wp-json/` (e.g. `/wp/v2/posts`).
- `--params`: Query parameters as a JSON string.
- `--body`: Post body fields as a JSON string.

## Examples

### 1. Listing Posts (Drafts)

```bash
python ../skills/wordpress/scripts/wordpress_api.py --url "https://example.com" --password "abcd efgh ijkl mnop qrst uvwx" --method GET --endpoint "/wp-json/wp/v2/posts" --params "{\"status\": \"draft\", \"per_page\": 3}"
```

### 2. Creating a New Post

```bash
python ../skills/wordpress/scripts/wordpress_api.py --url "https://example.com" --password "abcd efgh ijkl mnop qrst uvwx" --method POST --endpoint "/wp-json/wp/v2/posts" --body "{\"title\": \"My Draft\", \"content\": \"Created via Python CLI.\", \"status\": \"draft\"}"
```

## Core REST API Endpoints Cheat Sheet

When invoking endpoints:

- **Posts/Pages Listing**: `GET /wp-json/wp/v2/posts` or `GET /wp-json/wp/v2/pages` (e.g. filter by `?status=draft` or `?per_page=5`).
- **Post/Page Creation**: `POST /wp-json/wp/v2/posts` or `POST /wp-json/wp/v2/pages`.
- **Media Library Listing**: `GET /wp-json/wp/v2/media`
- **Menu Management**: `GET` / `POST /wp-json/wp/v2/menus`
- **Comments Moderation**: `POST /wp-json/wp/v2/comments/<id>`
- **Plugin Management**: `GET /wp-json/wp/v2/plugins`
- **WooCommerce Products**: `GET /wp-json/wc/v3/products`

## Post and Page Status Options

When querying or creating posts and pages, the following `status` values are supported:

- `publish`: The post or page is published and publicly visible.
- `future`: The post is scheduled to be published in the future.
- `draft`: The post is a draft.
- `pending`: The post is pending review.
- `private`: The post is private (visible only to authorized roles).
- `trash`: The post has been sent to the trash.
- `any`: Used as a query filter to retrieve posts/pages of any status.
