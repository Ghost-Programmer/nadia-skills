#!/usr/bin/env python3
"""
Foreign Exchange (Forex) & Currency Conversion CLI for Nadia.
Uses the open, keyless @fawazahmed0/currency-api with automatic CDN failover.
"""

import argparse
import json
import sys
import urllib.request

USER_AGENT = "Nadia-Agent-ForexSkill/1.0"


def fetch_with_failover(path: str, date_str: str = "latest") -> dict:
    urls = [
        f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date_str}/v1/{path}",
        f"https://{date_str}.currency-api.pages.dev/v1/{path}",
    ]
    last_err = None
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:
            last_err = exc
    raise RuntimeError(f"All currency-api endpoints failed: {last_err}")


def cmd_convert(args):
    base = args.from_curr.strip().lower()
    targets = [t.strip().lower() for t in args.to_curr.split(",") if t.strip()]
    date_str = args.date.strip() if args.date else "latest"
    try:
        data = fetch_with_failover(f"currencies/{base}.json", date_str)
        rates_map = data.get(base, {})
        conversions = []
        for t in targets:
            rate = rates_map.get(t)
            if rate is not None:
                conversions.append(
                    {
                        "from": base.upper(),
                        "to": t.upper(),
                        "rate": round(float(rate), 6),
                        "amount": args.amount,
                        "converted": round(float(args.amount) * float(rate), 4),
                    }
                )
            else:
                conversions.append({"from": base.upper(), "to": t.upper(), "error": "Unsupported target currency"})
        print(
            json.dumps(
                {
                    "date": data.get("date", date_str),
                    "base": base.upper(),
                    "amount": args.amount,
                    "conversions": conversions,
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"Forex conversion failed: {exc}"}))
        sys.exit(1)


def cmd_rates(args):
    base = args.base.strip().lower()
    targets = [t.strip().lower() for t in args.targets.split(",") if t.strip()]
    try:
        data = fetch_with_failover(f"currencies/{base}.json", "latest")
        rates_map = data.get(base, {})
        selected = {}
        for t in targets:
            if t in rates_map:
                selected[t.upper()] = round(float(rates_map[t]), 6)
        print(json.dumps({"date": data.get("date"), "base": base.upper(), "rates": selected}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"Forex rates query failed: {exc}"}))
        sys.exit(1)


def cmd_currencies(args):
    query = (args.search or "").strip().lower()
    try:
        data = fetch_with_failover("currencies.json", "latest")
        matched = {}
        for code, name in data.items():
            if not query or query in code.lower() or query in str(name).lower():
                matched[code.upper()] = name
        print(json.dumps({"count": len(matched), "currencies": matched}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"Currency catalog query failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Foreign Exchange & Currency Conversion CLI.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_c = sub.add_parser("convert", help="Convert an amount between currencies")
    p_c.add_argument("--from", dest="from_curr", required=True, help="Base currency code (e.g. USD)")
    p_c.add_argument("--to", dest="to_curr", required=True, help="Comma-separated target currency codes (e.g. EUR,GBP,JPY)")
    p_c.add_argument("--amount", type=float, default=1.0, help="Amount in base currency")
    p_c.add_argument("--date", default="latest", help="Optional date in YYYY-MM-DD format (default: latest)")
    p_c.set_defaults(func=cmd_convert)

    p_r = sub.add_parser("rates", help="Get exchange rates for a base currency")
    p_r.add_argument("--base", default="USD", help="Base currency code (default: USD)")
    p_r.add_argument(
        "--targets",
        default="EUR,GBP,JPY,CAD,AUD,CHF,CNY,INR,MXN,BRL",
        help="Comma-separated target currency codes",
    )
    p_r.set_defaults(func=cmd_rates)

    p_l = sub.add_parser("currencies", help="Search supported currency codes and names")
    p_l.add_argument("--search", default="", help="Substring filter by code or currency name")
    p_l.set_defaults(func=cmd_currencies)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

