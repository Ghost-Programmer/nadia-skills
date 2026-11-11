#!/usr/bin/env python3
"""
USGS Earthquakes & Water Hazards CLI for Nadia.
Queries USGS Earthquake Hazards API (GeoJSON) and USGS Water Services Instantaneous Values API.
"""

import argparse
import datetime
import json
import sys
import urllib.parse
import urllib.request

USGS_QUAKES_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
USGS_WATER_URL = "https://waterservices.usgs.gov/nwis/iv/"
USER_AGENT = "Nadia-Agent-USGSHazards/1.0"


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def cmd_quakes(args):
    now = datetime.datetime.now(datetime.timezone.utc)
    start = now - datetime.timedelta(days=args.days)
    params = {
        "format": "geojson",
        "starttime": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "minmagnitude": str(args.min_magnitude),
        "orderby": "time",
        "limit": str(args.limit),
    }
    if args.lat is not None and args.lon is not None:
        params["latitude"] = str(args.lat)
        params["longitude"] = str(args.lon)
        params["maxradiuskm"] = str(args.radius_km)

    url = f"{USGS_QUAKES_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        features = data.get("features", [])
        events = []
        for feat in features:
            props = feat.get("properties", {})
            geom = feat.get("geometry", {})
            coords = geom.get("coordinates", [None, None, None])
            epoch_ms = props.get("time")
            iso_time = (
                datetime.datetime.fromtimestamp(epoch_ms / 1000.0, tz=datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S UTC"
                )
                if epoch_ms
                else ""
            )
            events.append(
                {
                    "id": feat.get("id"),
                    "magnitude": props.get("mag"),
                    "place": props.get("place"),
                    "time_utc": iso_time,
                    "longitude": coords[0] if len(coords) > 0 else None,
                    "latitude": coords[1] if len(coords) > 1 else None,
                    "depth_km": coords[2] if len(coords) > 2 else None,
                    "tsunami": bool(props.get("tsunami")),
                    "alert": props.get("alert"),
                    "url": props.get("url"),
                }
            )
        print(
            json.dumps(
                {
                    "count": len(events),
                    "min_magnitude": args.min_magnitude,
                    "days": args.days,
                    "earthquakes": events,
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"USGS Earthquake query failed: {exc}"}))
        sys.exit(1)


def cmd_water(args):
    params = {
        "format": "json",
        "parameterCd": "00060,00065",
        "siteStatus": "active",
    }
    if args.site:
        params["sites"] = args.site
    elif args.state:
        params["stateCd"] = args.state.upper()
    else:
        print(json.dumps({"error": "Provide either --state (e.g. CO) or --site (USGS site number)."}))
        sys.exit(1)

    url = f"{USGS_WATER_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        time_series = data.get("value", {}).get("timeSeries", [])
        stations = []
        for ts in time_series[: args.limit]:
            source = ts.get("sourceInfo", {})
            variable = ts.get("variable", {})
            values = ts.get("values", [{}])[0].get("value", [])
            latest = values[-1] if values else {}
            geo = source.get("geoLocation", {}).get("geogLocation", {})
            stations.append(
                {
                    "siteName": source.get("siteName"),
                    "siteCode": (source.get("siteCode") or [{}])[0].get("value"),
                    "latitude": geo.get("latitude"),
                    "longitude": geo.get("longitude"),
                    "variable": variable.get("variableName"),
                    "unit": variable.get("unit", {}).get("unitCode"),
                    "value": latest.get("value"),
                    "dateTime": latest.get("dateTime"),
                }
            )
        print(json.dumps({"count": len(stations), "stations": stations}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"USGS Water Services query failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query USGS Earthquakes and Water Services.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_q = sub.add_parser("quakes", help="Query recent earthquakes from USGS")
    p_q.add_argument("--min-magnitude", type=float, default=4.5, help="Minimum Richter magnitude")
    p_q.add_argument("--days", type=int, default=7, help="Lookback window in days (max 30)")
    p_q.add_argument("--lat", type=float, default=None, help="Center latitude for radius search")
    p_q.add_argument("--lon", type=float, default=None, help="Center longitude for radius search")
    p_q.add_argument("--radius-km", type=float, default=500.0, help="Search radius in km")
    p_q.add_argument("--limit", type=int, default=20, help="Maximum earthquakes to return")
    p_q.set_defaults(func=cmd_quakes)

    p_w = sub.add_parser("water", help="Query USGS real-time stream/river water gauges")
    p_w.add_argument("--state", default="", help="Two-letter US state code (e.g., CO, CA, WA)")
    p_w.add_argument("--site", default="", help="Specific USGS site code (e.g., 09380000)")
    p_w.add_argument("--limit", type=int, default=15, help="Maximum gauge readings to return")
    p_w.set_defaults(func=cmd_water)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

