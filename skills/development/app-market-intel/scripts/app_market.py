#!/usr/bin/env python3
"""
App Market Intelligence CLI for Nadia (@Product Manager).
Queries Apple App Store / iTunes Search API and AppGoat API (via nadia.prop.appgoat.apiKey).
"""

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.parse
import urllib.request

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup"
USER_AGENT = "Nadia-Agent-AppMarketIntel/1.0"


def load_nadia_property(prop_key: str, env_fallback: str = "") -> str:
    props_file = Path.home() / ".nadia" / "nadia.properties"
    if props_file.exists():
        try:
            for raw_line in props_file.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == prop_key:
                    val = v.strip().replace("\\:", ":")
                    if val:
                        return val
        except Exception:
            pass
    return os.environ.get(env_fallback, "") if env_fallback else ""


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def format_app_item(r: dict) -> dict:
    return {
        "trackId": r.get("trackId"),
        "trackName": r.get("trackName"),
        "bundleId": r.get("bundleId"),
        "sellerName": r.get("sellerName"),
        "primaryGenreName": r.get("primaryGenreName"),
        "genres": r.get("genres", []),
        "price": r.get("price"),
        "formattedPrice": r.get("formattedPrice"),
        "averageUserRating": r.get("averageUserRating"),
        "userRatingCount": r.get("userRatingCount"),
        "version": r.get("version"),
        "currentVersionReleaseDate": r.get("currentVersionReleaseDate"),
        "description": (r.get("description") or "")[:400],
        "releaseNotes": (r.get("releaseNotes") or "")[:300],
        "trackViewUrl": r.get("trackViewUrl"),
    }


def cmd_search(args):
    params = {
        "term": args.query,
        "country": args.country.lower(),
        "entity": args.entity,
        "limit": str(args.limit),
    }
    url = f"{ITUNES_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        apps = [format_app_item(r) for r in data.get("results", [])]
        print(json.dumps({"query": args.query, "count": len(apps), "apps": apps}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"App market search failed: {exc}"}))
        sys.exit(1)


def cmd_lookup(args):
    params = {"id": args.app_id.strip(), "country": args.country.lower()}
    url = f"{ITUNES_LOOKUP_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        results = data.get("results", [])
        if not results:
            print(json.dumps({"appId": args.app_id, "found": False}))
            return
        print(json.dumps(format_app_item(results[0]), indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"App lookup failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Search and inspect mobile/desktop apps for market teardowns.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_s = sub.add_parser("search", help="Search apps or games by keyword")
    p_s.add_argument("--query", required=True, help="Search keywords")
    p_s.add_argument("--country", default="us", help="Two-letter store country code")
    p_s.add_argument("--entity", choices=["software", "iPadSoftware", "macSoftware"], default="software")
    p_s.add_argument("--limit", type=int, default=10, help="Max results")
    p_s.set_defaults(func=cmd_search)

    p_l = sub.add_parser("lookup", help="Look up an app by store ID")
    p_l.add_argument("--app-id", required=True, help="Numeric App Store trackId")
    p_l.add_argument("--country", default="us", help="Two-letter store country code")
    p_l.set_defaults(func=cmd_lookup)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

