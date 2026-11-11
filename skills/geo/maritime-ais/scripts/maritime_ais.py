#!/usr/bin/env python3
"""
Maritime AIS Vessel Tracking CLI for Nadia.
Supports AIS Trail API (via nadia.prop.aistrail.apiKey) and open Digitraffic Marine AIS GeoJSON endpoints.
"""

import argparse
import gzip
import json
import os
from pathlib import Path
import sys
import urllib.parse
import urllib.request

DIGITRAFFIC_LOCATIONS_URL = "https://meri.digitraffic.fi/api/ais/v1/locations"
USER_AGENT = "Nadia-Agent-MaritimeAIS/1.0"


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


def http_get_json(url: str, extra_headers: dict = None) -> dict:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "Digitraffic-User": "NadiaCognitiveAgent/1.0",
    }
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as resp:
        raw = resp.read()
        if resp.info().get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        return json.loads(raw.decode("utf-8"))


def cmd_vessel(args):
    mmsi = args.mmsi.strip()
    url = f"{DIGITRAFFIC_LOCATIONS_URL}/{urllib.parse.quote(mmsi)}"
    try:
        data = http_get_json(url)
        features = data.get("features", [])
        if not features:
            print(json.dumps({"mmsi": mmsi, "found": False}))
            return
        feat = features[0]
        geom = feat.get("geometry", {})
        coords = geom.get("coordinates", [None, None])
        props = feat.get("properties", {})
        print(
            json.dumps(
                {
                    "mmsi": feat.get("mmsi") or mmsi,
                    "longitude": coords[0] if len(coords) > 0 else None,
                    "latitude": coords[1] if len(coords) > 1 else None,
                    "sog_knots": props.get("sog"),
                    "cog_degrees": props.get("cog"),
                    "heading": props.get("heading"),
                    "navStat": props.get("navStat"),
                    "timestampExternal": props.get("timestampExternal"),
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"AIS vessel lookup failed for MMSI '{mmsi}': {exc}"}))
        sys.exit(1)


def cmd_bbox(args):
    params = {
        "from": "0",
        "minLat": str(args.min_lat),
        "maxLat": str(args.max_lat),
        "minLon": str(args.min_lon),
        "maxLon": str(args.max_lon),
    }
    url = f"{DIGITRAFFIC_LOCATIONS_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        features = data.get("features", [])
        vessels = []
        for feat in features[: args.limit]:
            coords = (feat.get("geometry") or {}).get("coordinates", [None, None])
            props = feat.get("properties", {})
            vessels.append(
                {
                    "mmsi": feat.get("mmsi") or props.get("mmsi"),
                    "longitude": coords[0] if len(coords) > 0 else None,
                    "latitude": coords[1] if len(coords) > 1 else None,
                    "sog_knots": props.get("sog"),
                    "cog_degrees": props.get("cog"),
                    "heading": props.get("heading"),
                    "navStat": props.get("navStat"),
                }
            )
        print(
            json.dumps(
                {
                    "bbox": {
                        "min_lat": args.min_lat,
                        "max_lat": args.max_lat,
                        "min_lon": args.min_lon,
                        "max_lon": args.max_lon,
                    },
                    "count": len(vessels),
                    "vessels": vessels,
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"AIS bounding box scan failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query Maritime AIS vessel positions.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_v = sub.add_parser("vessel", help="Look up vessel position by 9-digit MMSI")
    p_v.add_argument("--mmsi", required=True, help="9-digit MMSI number")
    p_v.set_defaults(func=cmd_vessel)

    p_b = sub.add_parser("bbox", help="Scan vessels inside a geographic bounding box")
    p_b.add_argument("--min-lat", type=float, required=True, help="Minimum latitude")
    p_b.add_argument("--max-lat", type=float, required=True, help="Maximum latitude")
    p_b.add_argument("--min-lon", type=float, required=True, help="Minimum longitude")
    p_b.add_argument("--max-lon", type=float, required=True, help="Maximum longitude")
    p_b.add_argument("--limit", type=int, default=15, help="Max vessels to return")
    p_b.set_defaults(func=cmd_bbox)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

