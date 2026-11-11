#!/usr/bin/env python3
"""
Parcel & Shipment Tracker CLI for Nadia (@Personal Assistant).
Queries WhereParcel v2 REST API using nadia.prop.whereparcel.apiKey.
"""

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.request

WHEREPARCEL_URL = "https://api.whereparcel.com/v2/track"
USER_AGENT = "Nadia-Agent-ParcelTracker/1.0"


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


def cmd_track(args):
    api_key = load_nadia_property("nadia.prop.whereparcel.apiKey", "WHEREPARCEL_API_KEY")
    if not api_key:
        print(
            json.dumps(
                {"error": "Missing required property nadia.prop.whereparcel.apiKey in ~/.nadia/nadia.properties"}
            )
        )
        sys.exit(1)

    payload = json.dumps(
        {
            "carrier": args.carrier.strip(),
            "trackingNumber": args.tracking_number.strip(),
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        WHEREPARCEL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        print(json.dumps(data, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"WhereParcel tracking request failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Track parcels via WhereParcel API.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_t = sub.add_parser("track", help="Track a package by carrier and tracking number")
    p_t.add_argument("--carrier", required=True, help="Carrier code (e.g. us.usps, us.ups, us.fedex, de.dhl)")
    p_t.add_argument("--tracking-number", required=True, help="Carrier tracking number")
    p_t.set_defaults(func=cmd_track)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

