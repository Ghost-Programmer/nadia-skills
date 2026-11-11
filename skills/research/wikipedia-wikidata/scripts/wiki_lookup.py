#!/usr/bin/env python3
"""
Wikipedia & Wikidata Knowledge Graph CLI for Nadia.
Keyless access to Wikimedia REST and MediaWiki Action APIs.
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request

WIKI_REST_BASE = "https://en.wikipedia.org/api/rest_v1"
WIKI_ACTION_URL = "https://en.wikipedia.org/w/api.php"
WIKIDATA_API_URL = "https://www.wikidata.org/w/api.php"
USER_AGENT = "Nadia-Agent-WikipediaWikidata/1.0 (https://github.com/Ghost-Programmer/nadia-skills)"


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def cmd_summary(args):
    encoded = urllib.parse.quote(args.title.strip().replace(" ", "_"))
    url = f"{WIKI_REST_BASE}/page/summary/{encoded}"
    try:
        data = http_get_json(url)
        print(
            json.dumps(
                {
                    "title": data.get("title"),
                    "description": data.get("description"),
                    "extract": data.get("extract"),
                    "wikibase_item": data.get("wikibase_item"),
                    "coordinates": data.get("coordinates"),
                    "url": (data.get("content_urls") or {}).get("desktop", {}).get("page"),
                    "timestamp": data.get("timestamp"),
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"Wikipedia summary lookup failed for '{args.title}': {exc}"}))
        sys.exit(1)


def cmd_search(args):
    params = {
        "action": "query",
        "list": "search",
        "srsearch": args.query,
        "srlimit": str(args.limit),
        "format": "json",
    }
    url = f"{WIKI_ACTION_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        items = data.get("query", {}).get("search", [])
        results = []
        for item in items:
            title = item.get("title", "")
            results.append(
                {
                    "title": title,
                    "pageid": item.get("pageid"),
                    "snippet": item.get("snippet", "").replace('<span class="searchmatch">', "").replace("</span>", ""),
                    "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}",
                }
            )
        print(json.dumps({"query": args.query, "count": len(results), "results": results}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"Wikipedia search failed: {exc}"}))
        sys.exit(1)


def cmd_wikidata(args):
    params = {
        "action": "wbsearchentities",
        "search": args.query,
        "language": "en",
        "limit": str(args.limit),
        "format": "json",
    }
    url = f"{WIKIDATA_API_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        entities = []
        for e in data.get("search", []):
            entities.append(
                {
                    "id": e.get("id"),
                    "label": e.get("label"),
                    "description": e.get("description"),
                    "concepturi": e.get("concepturi"),
                }
            )
        print(json.dumps({"query": args.query, "count": len(entities), "entities": entities}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"Wikidata entity search failed: {exc}"}))
        sys.exit(1)


def cmd_onthisday(args):
    url = f"{WIKI_REST_BASE}/feed/onthisday/events/{args.month:02d}/{args.day:02d}"
    try:
        data = http_get_json(url)
        events = []
        for ev in data.get("events", [])[: args.limit]:
            events.append({"year": ev.get("year"), "text": ev.get("text")})
        print(json.dumps({"month": args.month, "day": args.day, "count": len(events), "events": events}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"Wikipedia On This Day lookup failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query Wikipedia and Wikidata.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sum = sub.add_parser("summary", help="Fetch summary for a Wikipedia page title")
    p_sum.add_argument("--title", required=True, help="Wikipedia page title")
    p_sum.set_defaults(func=cmd_summary)

    p_s = sub.add_parser("search", help="Search Wikipedia articles")
    p_s.add_argument("--query", required=True, help="Search query")
    p_s.add_argument("--limit", type=int, default=10, help="Max results")
    p_s.set_defaults(func=cmd_search)

    p_wd = sub.add_parser("wikidata", help="Search Wikidata knowledge-graph entities")
    p_wd.add_argument("--query", required=True, help="Entity search query")
    p_wd.add_argument("--limit", type=int, default=10, help="Max results")
    p_wd.set_defaults(func=cmd_wikidata)

    p_otd = sub.add_parser("onthisday", help="Fetch historical events on a given month/day")
    p_otd.add_argument("--month", type=int, required=True, help="Month (1-12)")
    p_otd.add_argument("--day", type=int, required=True, help="Day (1-31)")
    p_otd.add_argument("--limit", type=int, default=10, help="Max events")
    p_otd.set_defaults(func=cmd_onthisday)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

