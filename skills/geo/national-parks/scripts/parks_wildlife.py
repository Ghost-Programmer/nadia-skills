#!/usr/bin/env python3
"""
US National Park Service (NPS) & iNaturalist Biodiversity CLI for Nadia.
Reads nadia.prop.nps.apiKey from ~/.nadia/nadia.properties.
"""

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.parse
import urllib.request

NPS_BASE_URL = "https://developer.nps.gov/api/v1"
INATURALIST_URL = "https://api.inaturalist.org/v1/observations"
USER_AGENT = "Nadia-Agent-NationalParks/1.0"


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


def http_get_json(url: str, headers: dict = None) -> dict:
    req_headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, headers=req_headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_nps_key() -> str:
    key = load_nadia_property("nadia.prop.nps.apiKey", "NPS_API_KEY")
    if not key:
        print(json.dumps({"error": "Missing required property nadia.prop.nps.apiKey in ~/.nadia/nadia.properties"}))
        sys.exit(1)
    return key


def cmd_parks(args):
    api_key = get_nps_key()
    params = {"limit": str(args.limit)}
    if args.state:
        params["stateCode"] = args.state.upper()
    if args.query:
        params["q"] = args.query
    if args.park_code:
        params["parkCode"] = args.park_code.lower()

    url = f"{NPS_BASE_URL}/parks?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url, {"X-Api-Key": api_key})
        parks = []
        for p in data.get("data", []):
            parks.append(
                {
                    "parkCode": p.get("parkCode"),
                    "fullName": p.get("fullName"),
                    "states": p.get("states"),
                    "designation": p.get("designation"),
                    "latitude": p.get("latitude"),
                    "longitude": p.get("longitude"),
                    "description": p.get("description"),
                    "weatherInfo": p.get("weatherInfo"),
                    "url": p.get("url"),
                }
            )
        print(json.dumps({"count": len(parks), "parks": parks}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"NPS parks query failed: {exc}"}))
        sys.exit(1)


def cmd_alerts(args):
    api_key = get_nps_key()
    params = {"parkCode": args.park_code.lower(), "limit": str(args.limit)}
    url = f"{NPS_BASE_URL}/alerts?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url, {"X-Api-Key": api_key})
        alerts = []
        for a in data.get("data", []):
            alerts.append(
                {
                    "title": a.get("title"),
                    "category": a.get("category"),
                    "description": a.get("description"),
                    "parkCode": a.get("parkCode"),
                    "lastIndexedDate": a.get("lastIndexedDate"),
                    "url": a.get("url"),
                }
            )
        print(json.dumps({"parkCode": args.park_code, "count": len(alerts), "alerts": alerts}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"NPS alerts query failed: {exc}"}))
        sys.exit(1)


def cmd_campgrounds(args):
    api_key = get_nps_key()
    params = {"parkCode": args.park_code.lower(), "limit": str(args.limit)}
    url = f"{NPS_BASE_URL}/campgrounds?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url, {"X-Api-Key": api_key})
        camps = []
        for c in data.get("data", []):
            camps.append(
                {
                    "name": c.get("name"),
                    "parkCode": c.get("parkCode"),
                    "latitude": c.get("latitude"),
                    "longitude": c.get("longitude"),
                    "description": c.get("description"),
                    "reservationInfo": c.get("reservationInfo"),
                    "reservationUrl": c.get("reservationUrl"),
                    "totalSites": c.get("campsites", {}).get("totalSites"),
                }
            )
        print(json.dumps({"parkCode": args.park_code, "count": len(camps), "campgrounds": camps}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"NPS campgrounds query failed: {exc}"}))
        sys.exit(1)


def cmd_wildlife(args):
    params = {
        "lat": str(args.lat),
        "lng": str(args.lon),
        "radius": str(args.radius_km),
        "per_page": str(args.limit),
        "quality_grade": "research",
        "order": "desc",
        "order_by": "observed_on",
    }
    url = f"{INATURALIST_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        obs = []
        for r in data.get("results", []):
            taxon = r.get("taxon") or {}
            obs.append(
                {
                    "scientificName": taxon.get("name"),
                    "commonName": taxon.get("preferred_common_name"),
                    "iconicTaxon": taxon.get("iconic_taxon_name"),
                    "observedOn": r.get("observed_on"),
                    "placeGuess": r.get("place_guess"),
                    "location": r.get("location"),
                    "uri": r.get("uri"),
                }
            )
        print(json.dumps({"count": len(obs), "observations": obs}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"iNaturalist query failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query NPS National Parks and iNaturalist observations.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_parks = sub.add_parser("parks", help="Search US National Parks")
    p_parks.add_argument("--state", default="", help="Two-letter US state code (e.g., UT, CA, WY)")
    p_parks.add_argument("--query", default="", help="Search query")
    p_parks.add_argument("--park-code", default="", help="4-letter NPS park code (e.g. yose, zion)")
    p_parks.add_argument("--limit", type=int, default=10, help="Max results")
    p_parks.set_defaults(func=cmd_parks)

    p_alerts = sub.add_parser("alerts", help="Fetch active alerts and closures for a park")
    p_alerts.add_argument("--park-code", required=True, help="4-letter NPS park code (e.g. yose, grca)")
    p_alerts.add_argument("--limit", type=int, default=15, help="Max alerts")
    p_alerts.set_defaults(func=cmd_alerts)

    p_camp = sub.add_parser("campgrounds", help="Fetch campgrounds for a National Park")
    p_camp.add_argument("--park-code", required=True, help="4-letter NPS park code")
    p_camp.add_argument("--limit", type=int, default=15, help="Max campgrounds")
    p_camp.set_defaults(func=cmd_campgrounds)

    p_wild = sub.add_parser("wildlife", help="Query iNaturalist wildlife/plant sightings near coordinates")
    p_wild.add_argument("--lat", type=float, required=True, help="Latitude")
    p_wild.add_argument("--lon", type=float, required=True, help="Longitude")
    p_wild.add_argument("--radius-km", type=float, default=25.0, help="Search radius in km")
    p_wild.add_argument("--limit", type=int, default=15, help="Max sightings")
    p_wild.set_defaults(func=cmd_wildlife)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

