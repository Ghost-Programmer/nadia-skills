#!/usr/bin/env python3
"""
Air Quality Index (AQI) CLI for Nadia.
Queries US EPA AirNow API and World Air Quality Index (AQICN) API.
Reads nadia.prop.airnow.apiKey and nadia.prop.aqicn.apiKey from ~/.nadia/nadia.properties.
"""

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.parse
import urllib.request

AIRNOW_URL = "https://www.airnowapi.org/aq/observation/latLong/current/"
AQICN_BASE_URL = "https://api.waqi.info/feed"
USER_AGENT = "Nadia-Agent-AirQuality/1.0"


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


def aqi_category(aqi_val) -> str:
    try:
        v = int(aqi_val)
    except Exception:
        return "Unknown"
    if v <= 50:
        return "Good (Green)"
    if v <= 100:
        return "Moderate (Yellow)"
    if v <= 150:
        return "Unhealthy for Sensitive Groups (Orange)"
    if v <= 200:
        return "Unhealthy (Red)"
    if v <= 300:
        return "Very Unhealthy (Purple)"
    return "Hazardous (Maroon)"


def cmd_aqicn(args):
    token = load_nadia_property("nadia.prop.aqicn.apiKey", "AQICN_API_KEY")
    if not token:
        print(json.dumps({"error": "Missing required property nadia.prop.aqicn.apiKey in ~/.nadia/nadia.properties"}))
        sys.exit(1)

    if args.lat is not None and args.lon is not None:
        target = f"geo:{args.lat};{args.lon}"
    elif args.city:
        target = urllib.parse.quote(args.city.strip())
    else:
        print(json.dumps({"error": "Provide either --city or both --lat and --lon."}))
        sys.exit(1)

    url = f"{AQICN_BASE_URL}/{target}/?token={urllib.parse.quote(token)}"
    try:
        res = http_get_json(url)
        if res.get("status") != "ok":
            print(json.dumps({"error": res.get("data", "AQICN lookup failed")}))
            sys.exit(1)
        d = res.get("data", {})
        city_info = d.get("city", {})
        iaqi = {k: v.get("v") for k, v in (d.get("iaqi") or {}).items() if isinstance(v, dict)}
        out = {
            "station": city_info.get("name"),
            "geo": city_info.get("geo"),
            "aqi": d.get("aqi"),
            "category": aqi_category(d.get("aqi")),
            "dominant_pollutant": d.get("dominentpol"),
            "pollutants": iaqi,
            "time": (d.get("time") or {}).get("iso"),
        }
        print(json.dumps(out, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"AQICN request failed: {exc}"}))
        sys.exit(1)


def cmd_airnow(args):
    api_key = load_nadia_property("nadia.prop.airnow.apiKey", "AIRNOW_API_KEY")
    if not api_key:
        print(json.dumps({"error": "Missing required property nadia.prop.airnow.apiKey in ~/.nadia/nadia.properties"}))
        sys.exit(1)

    params = {
        "format": "application/json",
        "latitude": str(args.lat),
        "longitude": str(args.lon),
        "distance": str(args.distance_miles),
        "API_KEY": api_key,
    }
    url = f"{AIRNOW_URL}?{urllib.parse.urlencode(params)}"
    try:
        items = http_get_json(url)
        readings = []
        for item in items:
            readings.append(
                {
                    "reportingArea": item.get("ReportingArea"),
                    "stateCode": item.get("StateCode"),
                    "latitude": item.get("Latitude"),
                    "longitude": item.get("Longitude"),
                    "parameterName": item.get("ParameterName"),
                    "aqi": item.get("AQI"),
                    "category": (item.get("Category") or {}).get("Name"),
                    "dateObserved": item.get("DateObserved"),
                    "hourObserved": item.get("HourObserved"),
                }
            )
        print(json.dumps({"count": len(readings), "observations": readings}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"AirNow request failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query AirNow and AQICN air quality metrics.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_aqi = sub.add_parser("aqicn", help="Query World Air Quality Index (AQICN) by city or coordinates")
    p_aqi.add_argument("--city", default="", help="City name (e.g. Denver, Tokyo, London)")
    p_aqi.add_argument("--lat", type=float, default=None, help="Latitude")
    p_aqi.add_argument("--lon", type=float, default=None, help="Longitude")
    p_aqi.set_defaults(func=cmd_aqicn)

    p_an = sub.add_parser("airnow", help="Query US EPA AirNow observations by coordinates")
    p_an.add_argument("--lat", type=float, required=True, help="Latitude")
    p_an.add_argument("--lon", type=float, required=True, help="Longitude")
    p_an.add_argument("--distance-miles", type=int, default=25, help="Search radius in miles")
    p_an.set_defaults(func=cmd_airnow)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

