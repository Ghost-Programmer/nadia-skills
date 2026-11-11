#!/usr/bin/env python3
"""
Worldwide Public & Bank Holidays CLI for Nadia (@Personal Assistant).
Queries Nager.Date v3 REST API (keyless).
"""

import argparse
import datetime
import json
import sys
import urllib.parse
import urllib.request

NAGER_BASE_URL = "https://date.nager.at/api/v3"
USER_AGENT = "Nadia-Agent-PublicHolidays/1.0"


def http_get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def cmd_upcoming(args):
    country = urllib.parse.quote(args.country.strip().upper())
    url = f"{NAGER_BASE_URL}/NextPublicHolidays/{country}"
    try:
        items = http_get_json(url)
        holidays = [
            {
                "date": h.get("date"),
                "name": h.get("name"),
                "localName": h.get("localName"),
                "countryCode": h.get("countryCode"),
                "global": h.get("global"),
                "types": h.get("types", []),
            }
            for h in items
        ]
        print(json.dumps({"country": country, "count": len(holidays), "upcomingHolidays": holidays}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"Nager.Date upcoming holidays lookup failed: {exc}"}))
        sys.exit(1)


def cmd_year(args):
    country = urllib.parse.quote(args.country.strip().upper())
    url = f"{NAGER_BASE_URL}/PublicHolidays/{args.year}/{country}"
    try:
        items = http_get_json(url)
        holidays = [
            {
                "date": h.get("date"),
                "name": h.get("name"),
                "localName": h.get("localName"),
                "global": h.get("global"),
                "counties": h.get("counties"),
                "types": h.get("types", []),
            }
            for h in items
        ]
        print(
            json.dumps(
                {"country": country, "year": args.year, "count": len(holidays), "holidays": holidays},
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"Nager.Date year holidays lookup failed: {exc}"}))
        sys.exit(1)


def cmd_weekends(args):
    country = urllib.parse.quote(args.country.strip().upper())
    url = f"{NAGER_BASE_URL}/LongWeekend/{args.year}/{country}"
    try:
        items = http_get_json(url)
        print(
            json.dumps(
                {"country": country, "year": args.year, "count": len(items), "longWeekends": items},
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"Nager.Date long weekends lookup failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query worldwide public holidays and long weekends via Nager.Date.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_up = sub.add_parser("upcoming", help="Get upcoming public holidays for a country")
    p_up.add_argument("--country", default="US", help="ISO-3166 alpha-2 country code (e.g. US, GB, CA, DE)")
    p_up.set_defaults(func=cmd_upcoming)

    p_yr = sub.add_parser("year", help="Get all public holidays in a given year")
    p_yr.add_argument("--country", default="US", help="ISO-3166 alpha-2 country code")
    p_yr.add_argument("--year", type=int, default=datetime.datetime.now().year, help="Target year")
    p_yr.set_defaults(func=cmd_year)

    p_wk = sub.add_parser("weekends", help="Get long weekends for a year and country")
    p_wk.add_argument("--country", default="US", help="ISO-3166 alpha-2 country code")
    p_wk.add_argument("--year", type=int, default=datetime.datetime.now().year, help="Target year")
    p_wk.set_defaults(func=cmd_weekends)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

