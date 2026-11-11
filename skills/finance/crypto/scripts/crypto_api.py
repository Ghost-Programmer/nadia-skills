#!/usr/bin/env python3
"""
CoinGecko Cryptocurrency Market CLI for Nadia.
Supports keyless public access and optional nadia.prop.coingecko.apiKey from ~/.nadia/nadia.properties.
"""

import argparse
import datetime
import json
import os
from pathlib import Path
import sys
import urllib.parse
import urllib.request

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
USER_AGENT = "Nadia-Agent-CryptoSkill/1.0"


def load_nadia_property(prop_key: str) -> str:
    props_file = Path.home() / ".nadia" / "nadia.properties"
    if not props_file.exists():
        return os.environ.get("COINGECKO_API_KEY", "")
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
    return os.environ.get("COINGECKO_API_KEY", "")


def http_get_json(endpoint: str, params: dict = None) -> dict:
    url = f"{COINGECKO_BASE_URL}{endpoint}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    api_key = load_nadia_property("nadia.prop.coingecko.apiKey")
    if api_key:
        headers["x-cg-demo-api-key"] = api_key
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def cmd_markets(args):
    params = {
        "vs_currency": args.currency.lower(),
        "order": "market_cap_desc",
        "per_page": str(args.limit),
        "page": "1",
        "sparkline": "false",
    }
    if args.ids:
        params["ids"] = args.ids.lower()

    try:
        items = http_get_json("/coins/markets", params)
        coins = []
        for c in items:
            coins.append(
                {
                    "id": c.get("id"),
                    "symbol": (c.get("symbol") or "").upper(),
                    "name": c.get("name"),
                    "market_cap_rank": c.get("market_cap_rank"),
                    "current_price": c.get("current_price"),
                    "price_change_percentage_24h": c.get("price_change_percentage_24h"),
                    "high_24h": c.get("high_24h"),
                    "low_24h": c.get("low_24h"),
                    "market_cap": c.get("market_cap"),
                    "total_volume": c.get("total_volume"),
                    "last_updated": c.get("last_updated"),
                }
            )
        print(json.dumps({"currency": args.currency.upper(), "count": len(coins), "coins": coins}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"CoinGecko markets query failed: {exc}"}))
        sys.exit(1)


def cmd_search(args):
    try:
        data = http_get_json("/search", {"query": args.query})
        coins = [
            {
                "id": c.get("id"),
                "name": c.get("name"),
                "symbol": c.get("symbol"),
                "market_cap_rank": c.get("market_cap_rank"),
            }
            for c in (data.get("coins") or [])[: args.limit]
        ]
        print(json.dumps({"query": args.query, "results": coins}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"CoinGecko search failed: {exc}"}))
        sys.exit(1)


def cmd_trending(args):
    try:
        data = http_get_json("/search/trending")
        trending = []
        for entry in data.get("coins") or []:
            item = entry.get("item", {})
            trending.append(
                {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "symbol": item.get("symbol"),
                    "market_cap_rank": item.get("market_cap_rank"),
                    "score": item.get("score"),
                }
            )
        print(json.dumps({"trending_coins": trending}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"CoinGecko trending query failed: {exc}"}))
        sys.exit(1)


def cmd_history(args):
    try:
        data = http_get_json(
            f"/coins/{urllib.parse.quote(args.id.lower())}/market_chart",
            {"vs_currency": args.currency.lower(), "days": str(args.days), "interval": "daily"},
        )
        points = []
        for ts_ms, price in data.get("prices", []):
            dt = datetime.datetime.fromtimestamp(ts_ms / 1000.0, tz=datetime.timezone.utc).strftime("%Y-%m-%d")
            points.append({"date": dt, "price": round(price, 6)})
        print(
            json.dumps(
                {"id": args.id.lower(), "currency": args.currency.upper(), "days": args.days, "history": points},
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"CoinGecko history query failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query CoinGecko cryptocurrency data.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_m = sub.add_parser("markets", help="Get top crypto prices and market caps")
    p_m.add_argument("--ids", default="", help="Comma-separated coin IDs (e.g. bitcoin,ethereum,solana)")
    p_m.add_argument("--currency", default="usd", help="Target quote currency (default: usd)")
    p_m.add_argument("--limit", type=int, default=15, help="Number of coins to return")
    p_m.set_defaults(func=cmd_markets)

    p_s = sub.add_parser("search", help="Search coin ID by name or symbol")
    p_s.add_argument("--query", required=True, help="Search query")
    p_s.add_argument("--limit", type=int, default=10, help="Max results")
    p_s.set_defaults(func=cmd_search)

    p_t = sub.add_parser("trending", help="Get top trending coins in the last 24h")
    p_t.set_defaults(func=cmd_trending)

    p_h = sub.add_parser("history", help="Get daily historical prices for a coin")
    p_h.add_argument("--id", required=True, help="CoinGecko coin ID (e.g. bitcoin)")
    p_h.add_argument("--days", type=int, default=14, help="Number of days of history")
    p_h.add_argument("--currency", default="usd", help="Quote currency")
    p_h.set_defaults(func=cmd_history)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

