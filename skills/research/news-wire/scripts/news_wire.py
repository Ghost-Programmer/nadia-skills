#!/usr/bin/env python3
"""
Breaking News & Tech Wire CLI for Nadia.
Supports keyless HackerNews (Firebase + Algolia Search) and optional
nadia.prop.newsdata.apiKey / nadia.prop.gnews.apiKey from ~/.nadia/nadia.properties.
"""

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.parse
import urllib.request

HN_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
HN_ALGOLIA_URL = "https://hn.algolia.com/api/v1/search"
NEWSDATA_URL = "https://newsdata.io/api/1/latest"
GNEWS_SEARCH_URL = "https://gnews.io/api/v4/search"
GNEWS_HEADLINES_URL = "https://gnews.io/api/v4/top-headlines"
USER_AGENT = "Nadia-Agent-NewsWire/1.0"


def load_nadia_property(prop_key: str) -> str:
    props_file = Path.home() / ".nadia" / "nadia.properties"
    if props_file.exists():
        try:
            for raw_line in props_file.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == prop_key:
                    return v.strip().replace("\\:", ":")
        except Exception:
            pass
    env_key = prop_key.replace("nadia.prop.", "").replace(".", "_").replace("-", "_").upper()
    return os.environ.get(env_key, "")


def http_get_json(url: str) -> object:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_hn_top(limit: int) -> list:
    story_ids = http_get_json(HN_TOP_URL) or []
    stories = []
    for sid in story_ids[:limit]:
        try:
            item = http_get_json(HN_ITEM_URL.format(id=sid)) or {}
            stories.append(
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "url": item.get("url") or f"https://news.ycombinator.com/item?id={sid}",
                    "score": item.get("score"),
                    "by": item.get("by"),
                    "comments": item.get("descendants", 0),
                    "source": "HackerNews",
                }
            )
        except Exception:
            continue
    return stories


def cmd_hn_top(args):
    try:
        stories = fetch_hn_top(args.limit)
        print(json.dumps({"provider": "HackerNews", "count": len(stories), "stories": stories}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"HackerNews top stories query failed: {exc}"}))
        sys.exit(1)


def cmd_search(args):
    newsdata_key = load_nadia_property("nadia.prop.newsdata.apiKey")
    gnews_key = load_nadia_property("nadia.prop.gnews.apiKey")
    articles = []

    if gnews_key:
        try:
            params = {"q": args.query, "lang": "en", "max": str(args.limit), "apikey": gnews_key}
            data = http_get_json(f"{GNEWS_SEARCH_URL}?{urllib.parse.urlencode(params)}")
            for a in data.get("articles", []):
                articles.append(
                    {
                        "title": a.get("title"),
                        "description": a.get("description"),
                        "url": a.get("url"),
                        "publishedAt": a.get("publishedAt"),
                        "source": (a.get("source") or {}).get("name", "GNews"),
                    }
                )
        except Exception:
            pass

    if not articles and newsdata_key:
        try:
            params = {"q": args.query, "language": "en", "apikey": newsdata_key}
            data = http_get_json(f"{NEWSDATA_URL}?{urllib.parse.urlencode(params)}")
            for a in (data.get("results") or [])[: args.limit]:
                articles.append(
                    {
                        "title": a.get("title"),
                        "description": a.get("description"),
                        "url": a.get("link"),
                        "publishedAt": a.get("pubDate"),
                        "source": a.get("source_id", "NewsData"),
                    }
                )
        except Exception:
            pass

    # Always include keyless Algolia HackerNews search results if no API key articles or to supplement
    if len(articles) < args.limit:
        try:
            params = {"query": args.query, "tags": "story", "hitsPerPage": str(args.limit)}
            data = http_get_json(f"{HN_ALGOLIA_URL}?{urllib.parse.urlencode(params)}")
            for h in data.get("hits", []):
                articles.append(
                    {
                        "title": h.get("title"),
                        "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                        "publishedAt": h.get("created_at"),
                        "points": h.get("points"),
                        "author": h.get("author"),
                        "source": "HackerNews (Algolia)",
                    }
                )
        except Exception as exc:
            if not articles:
                print(json.dumps({"error": f"News search failed: {exc}"}))
                sys.exit(1)

    print(
        json.dumps(
            {
                "query": args.query,
                "count": len(articles[: args.limit]),
                "articles": articles[: args.limit],
            },
            indent=2,
        )
    )


def cmd_headlines(args):
    newsdata_key = load_nadia_property("nadia.prop.newsdata.apiKey")
    gnews_key = load_nadia_property("nadia.prop.gnews.apiKey")

    if gnews_key:
        try:
            params = {
                "category": args.category,
                "country": args.country,
                "lang": "en",
                "max": str(args.limit),
                "apikey": gnews_key,
            }
            data = http_get_json(f"{GNEWS_HEADLINES_URL}?{urllib.parse.urlencode(params)}")
            articles = [
                {
                    "title": a.get("title"),
                    "description": a.get("description"),
                    "url": a.get("url"),
                    "publishedAt": a.get("publishedAt"),
                    "source": (a.get("source") or {}).get("name", "GNews"),
                }
                for a in data.get("articles", [])
            ]
            print(json.dumps({"provider": "GNews", "count": len(articles), "headlines": articles}, indent=2))
            return
        except Exception:
            pass

    if newsdata_key:
        try:
            params = {
                "category": args.category,
                "country": args.country,
                "language": "en",
                "apikey": newsdata_key,
            }
            data = http_get_json(f"{NEWSDATA_URL}?{urllib.parse.urlencode(params)}")
            articles = [
                {
                    "title": a.get("title"),
                    "description": a.get("description"),
                    "url": a.get("link"),
                    "publishedAt": a.get("pubDate"),
                    "source": a.get("source_id", "NewsData"),
                }
                for a in (data.get("results") or [])[: args.limit]
            ]
            print(json.dumps({"provider": "NewsData.io", "count": len(articles), "headlines": articles}, indent=2))
            return
        except Exception:
            pass

    # Fallback to keyless HackerNews top stories
    stories = fetch_hn_top(args.limit)
    print(
        json.dumps(
            {
                "provider": "HackerNews (Keyless Fallback - configure nadia.prop.newsdata.apiKey or nadia.prop.gnews.apiKey for global news wires)",
                "count": len(stories),
                "headlines": stories,
            },
            indent=2,
        )
    )


def main():
    parser = argparse.ArgumentParser(description="Breaking News & Tech Wire CLI.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_hn = sub.add_parser("hn-top", help="Fetch top stories from HackerNews (keyless)")
    p_hn.add_argument("--limit", type=int, default=15, help="Max stories to return")
    p_hn.set_defaults(func=cmd_hn_top)

    p_s = sub.add_parser("search", help="Search news and tech stories by keyword")
    p_s.add_argument("--query", required=True, help="Search query")
    p_s.add_argument("--limit", type=int, default=10, help="Max results")
    p_s.set_defaults(func=cmd_search)

    p_h = sub.add_parser("headlines", help="Fetch top breaking headlines")
    p_h.add_argument("--category", default="technology", help="Category (technology, business, world, science)")
    p_h.add_argument("--country", default="us", help="Two-letter country code")
    p_h.add_argument("--limit", type=int, default=10, help="Max headlines")
    p_h.set_defaults(func=cmd_headlines)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

