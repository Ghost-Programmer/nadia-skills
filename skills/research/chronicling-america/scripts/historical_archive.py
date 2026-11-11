#!/usr/bin/env python3
"""
Library of Congress (Chronicling America) & Internet Archive CLI for Nadia.
Provides keyless search over digitized historic US newspapers (1770-1963),
Internet Archive historical/genealogy texts, and Wayback Machine snapshots.
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request

LOC_CHRONAM_URL = "https://www.loc.gov/collections/chronicling-america/"
ARCHIVE_SEARCH_URL = "https://archive.org/advancedsearch.php"
WAYBACK_URL = "https://archive.org/wayback/available"
USER_AGENT = "Nadia-Agent-HistoricalArchive/1.0"


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


def cmd_newspapers(args):
    q_parts = [args.query]
    if args.state:
        q_parts.append(args.state)
    params = {
        "fo": "json",
        "q": " ".join(q_parts),
        "c": str(args.limit),
    }
    if args.start_year and args.end_year:
        params["dates"] = f"{args.start_year}/{args.end_year}"
    elif args.start_year:
        params["dates"] = f"{args.start_year}/1963"

    url = f"{LOC_CHRONAM_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        results = []
        for item in (data.get("results") or [])[: args.limit]:
            results.append(
                {
                    "title": item.get("title"),
                    "date": item.get("date"),
                    "location": item.get("location", []),
                    "partof_title": item.get("partof_title", []),
                    "description": (
                        item.get("description", [""])[0][:350]
                        if isinstance(item.get("description"), list) and item.get("description")
                        else ""
                    ),
                    "url": item.get("url") or item.get("id"),
                }
            )
        print(
            json.dumps(
                {
                    "query": args.query,
                    "state": args.state,
                    "count": len(results),
                    "newspapers": results,
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"Library of Congress Chronicling America search failed: {exc}"}))
        sys.exit(1)


def cmd_archive(args):
    params = [
        ("q", args.query),
        ("fl[]", "identifier"),
        ("fl[]", "title"),
        ("fl[]", "creator"),
        ("fl[]", "date"),
        ("fl[]", "mediatype"),
        ("fl[]", "description"),
        ("rows", str(args.limit)),
        ("page", "1"),
        ("output", "json"),
    ]
    url = f"{ARCHIVE_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        docs = data.get("response", {}).get("docs", [])
        items = []
        for d in docs:
            ident = d.get("identifier", "")
            desc = d.get("description", "")
            if isinstance(desc, list):
                desc = " ".join(str(x) for x in desc)
            items.append(
                {
                    "identifier": ident,
                    "title": d.get("title"),
                    "creator": d.get("creator"),
                    "date": d.get("date"),
                    "mediatype": d.get("mediatype"),
                    "description": str(desc)[:350],
                    "url": f"https://archive.org/details/{ident}" if ident else "",
                }
            )
        print(
            json.dumps(
                {
                    "query": args.query,
                    "numFound": data.get("response", {}).get("numFound", len(items)),
                    "count": len(items),
                    "items": items,
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"Internet Archive search failed: {exc}"}))
        sys.exit(1)


def cmd_wayback(args):
    params = {"url": args.url}
    if args.timestamp:
        params["timestamp"] = args.timestamp
    url = f"{WAYBACK_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        closest = data.get("archived_snapshots", {}).get("closest", {})
        print(
            json.dumps(
                {
                    "url": args.url,
                    "available": bool(closest.get("available")),
                    "snapshot_url": closest.get("url"),
                    "timestamp": closest.get("timestamp"),
                    "status": closest.get("status"),
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"Wayback Machine lookup failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Search Chronicling America & Internet Archive.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_n = sub.add_parser("newspapers", help="Search Library of Congress Chronicling America newspapers")
    p_n.add_argument("--query", required=True, help="Search terms (surname, person, event, or place)")
    p_n.add_argument("--state", default="", help="Optional US state filter (e.g. Ohio, Virginia)")
    p_n.add_argument("--start-year", type=int, default=0, help="Optional start year (1770-1963)")
    p_n.add_argument("--end-year", type=int, default=0, help="Optional end year (1770-1963)")
    p_n.add_argument("--limit", type=int, default=10, help="Max results to return")
    p_n.set_defaults(func=cmd_newspapers)

    p_a = sub.add_parser("archive", help="Search Internet Archive books, genealogy records, and texts")
    p_a.add_argument("--query", required=True, help="Search query")
    p_a.add_argument("--limit", type=int, default=10, help="Max items to return")
    p_a.set_defaults(func=cmd_archive)

    p_w = sub.add_parser("wayback", help="Check Wayback Machine snapshot availability for a URL")
    p_w.add_argument("--url", required=True, help="Target URL")
    p_w.add_argument("--timestamp", default="", help="Optional YYYYMMDDhhmmss timestamp")
    p_w.set_defaults(func=cmd_wayback)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

