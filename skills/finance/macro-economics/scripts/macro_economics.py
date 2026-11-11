#!/usr/bin/env python3
"""
Macroeconomics CLI for Nadia.
Queries Federal Reserve Economic Data (FRED) API and US Bureau of Labor Statistics (BLS) API.
Reads nadia.prop.fred.apiKey from ~/.nadia/nadia.properties.
"""

import argparse
import csv
import io
import json
import os
from pathlib import Path
import sys
import urllib.parse
import urllib.request

FRED_API_BASE = "https://api.stlouisfed.org/fred"
FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
BLS_API_URL = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
USER_AGENT = "Nadia-Agent-MacroEconomics/1.0"

CORE_SERIES = {
    "FEDFUNDS": "Federal Funds Effective Rate (%)",
    "CPIAUCSL": "Consumer Price Index for All Urban Consumers (CPI)",
    "UNRATE": "Civilian Unemployment Rate (%)",
    "DGS10": "10-Year Treasury Constant Maturity Rate (%)",
    "T10Y2Y": "10-Year Minus 2-Year Treasury Yield Spread (%)",
    "GDPC1": "Real Gross Domestic Product (Billions of Chained 2017 Dollars)",
}


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


def fetch_fred_csv_fallback(series_id: str, limit: int) -> list:
    url = f"{FRED_CSV_URL}?id={urllib.parse.quote(series_id.upper())}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        text = resp.read().decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for row in reader:
        date_val = row.get("DATE") or row.get("observation_date")
        val = row.get(series_id.upper())
        if date_val and val and val != ".":
            rows.append({"date": date_val, "value": val})
    return rows[-limit:]


def cmd_series(args):
    api_key = load_nadia_property("nadia.prop.fred.apiKey", "FRED_API_KEY")
    series_id = args.id.strip().upper()
    try:
        if api_key:
            params = {
                "series_id": series_id,
                "api_key": api_key,
                "file_type": "json",
                "sort_order": "desc",
                "limit": str(args.limit),
            }
            url = f"{FRED_API_BASE}/series/observations?{urllib.parse.urlencode(params)}"
            data = http_get_json(url)
            obs = [
                {"date": o.get("date"), "value": o.get("value")}
                for o in data.get("observations", [])
                if o.get("value") not in (None, ".")
            ]
        else:
            obs = list(reversed(fetch_fred_csv_fallback(series_id, args.limit)))
        print(
            json.dumps(
                {
                    "series_id": series_id,
                    "description": CORE_SERIES.get(series_id, ""),
                    "count": len(obs),
                    "observations": obs,
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"FRED series lookup failed for '{series_id}': {exc}"}))
        sys.exit(1)


def cmd_search(args):
    api_key = load_nadia_property("nadia.prop.fred.apiKey", "FRED_API_KEY")
    if not api_key:
        print(
            json.dumps(
                {
                    "error": "nadia.prop.fred.apiKey is not set in ~/.nadia/nadia.properties.",
                    "core_series_available": CORE_SERIES,
                },
                indent=2,
            )
        )
        sys.exit(1)
    params = {
        "search_text": args.query,
        "api_key": api_key,
        "file_type": "json",
        "limit": str(args.limit),
    }
    url = f"{FRED_API_BASE}/series/search?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        items = []
        for s in data.get("seriess", [])[: args.limit]:
            items.append(
                {
                    "id": s.get("id"),
                    "title": s.get("title"),
                    "frequency": s.get("frequency"),
                    "units": s.get("units"),
                    "seasonal_adjustment": s.get("seasonal_adjustment"),
                    "last_updated": s.get("last_updated"),
                }
            )
        print(json.dumps({"query": args.query, "count": len(items), "series": items}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"FRED search failed: {exc}"}))
        sys.exit(1)


def cmd_snapshot(args):
    snapshot = []
    for sid, label in CORE_SERIES.items():
        try:
            rows = fetch_fred_csv_fallback(sid, 2)
            latest = rows[-1] if rows else {}
            prev = rows[-2] if len(rows) > 1 else {}
            snapshot.append(
                {
                    "series_id": sid,
                    "title": label,
                    "latest_date": latest.get("date"),
                    "latest_value": latest.get("value"),
                    "previous_date": prev.get("date"),
                    "previous_value": prev.get("value"),
                }
            )
        except Exception as exc:
            snapshot.append({"series_id": sid, "title": label, "error": str(exc)})
    print(json.dumps({"indicators": snapshot}, indent=2))


def cmd_bls(args):
    series_list = [s.strip() for s in args.series.split(",") if s.strip()]
    payload = json.dumps(
        {
            "seriesid": series_list,
            "startyear": str(args.start_year),
            "endyear": str(args.end_year),
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        BLS_API_URL,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        results = []
        for s in data.get("Results", {}).get("series", []):
            results.append(
                {
                    "seriesID": s.get("seriesID"),
                    "data": s.get("data", [])[:12],
                }
            )
        print(json.dumps({"status": data.get("status"), "series": results}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"BLS query failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query FRED and BLS macroeconomic indicators.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ser = sub.add_parser("series", help="Fetch observations for a FRED series ID")
    p_ser.add_argument("--id", required=True, help="FRED series ID (e.g., FEDFUNDS, CPIAUCSL, UNRATE)")
    p_ser.add_argument("--limit", type=int, default=12, help="Number of recent observations")
    p_ser.set_defaults(func=cmd_series)

    p_search = sub.add_parser("search", help="Search FRED series catalog")
    p_search.add_argument("--query", required=True, help="Search keywords")
    p_search.add_argument("--limit", type=int, default=10, help="Max results")
    p_search.set_defaults(func=cmd_search)

    p_snap = sub.add_parser("snapshot", help="Fetch snapshot of core US macroeconomic indicators")
    p_snap.set_defaults(func=cmd_snapshot)

    p_bls = sub.add_parser("bls", help="Fetch US Bureau of Labor Statistics time series")
    p_bls.add_argument("--series", required=True, help="Comma-separated BLS series IDs (e.g., CUUR0000SA0)")
    p_bls.add_argument("--start-year", type=int, default=2024, help="Start year")
    p_bls.add_argument("--end-year", type=int, default=2026, help="End year")
    p_bls.set_defaults(func=cmd_bls)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

