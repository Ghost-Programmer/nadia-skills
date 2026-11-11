#!/usr/bin/env python3
"""
Cybersecurity Threat Intelligence CLI for Nadia.
Integrates AbuseIPDB, Shodan, and VirusTotal v3 APIs using nadia.prop.* keys.
"""

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.parse
import urllib.request

ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"
SHODAN_HOST_URL = "https://api.shodan.io/shodan/host"
VIRUSTOTAL_BASE_URL = "https://www.virustotal.com/api/v3"
USER_AGENT = "Nadia-Agent-ThreatIntel/1.0"


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


def cmd_abuseipdb(args):
    api_key = load_nadia_property("nadia.prop.abuseipdb.apiKey", "ABUSEIPDB_API_KEY")
    if not api_key:
        print(json.dumps({"error": "Missing required property nadia.prop.abuseipdb.apiKey in ~/.nadia/nadia.properties"}))
        sys.exit(1)
    params = {"ipAddress": args.ip.strip(), "maxAgeInDays": str(args.days)}
    url = f"{ABUSEIPDB_URL}?{urllib.parse.urlencode(params)}"
    try:
        res = http_get_json(url, {"Key": api_key})
        d = res.get("data", {})
        print(
            json.dumps(
                {
                    "ipAddress": d.get("ipAddress"),
                    "abuseConfidenceScore": d.get("abuseConfidenceScore"),
                    "countryCode": d.get("countryCode"),
                    "usageType": d.get("usageType"),
                    "isp": d.get("isp"),
                    "domain": d.get("domain"),
                    "totalReports": d.get("totalReports"),
                    "lastReportedAt": d.get("lastReportedAt"),
                    "isWhitelisted": d.get("isWhitelisted"),
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"AbuseIPDB lookup failed: {exc}"}))
        sys.exit(1)


def cmd_shodan(args):
    api_key = load_nadia_property("nadia.prop.shodan.apiKey", "SHODAN_API_KEY")
    if not api_key:
        print(json.dumps({"error": "Missing required property nadia.prop.shodan.apiKey in ~/.nadia/nadia.properties"}))
        sys.exit(1)
    url = f"{SHODAN_HOST_URL}/{urllib.parse.quote(args.ip.strip())}?key={urllib.parse.quote(api_key)}"
    try:
        d = http_get_json(url)
        print(
            json.dumps(
                {
                    "ip_str": d.get("ip_str"),
                    "org": d.get("org"),
                    "isp": d.get("isp"),
                    "asn": d.get("asn"),
                    "country_name": d.get("country_name"),
                    "hostnames": d.get("hostnames", []),
                    "ports": d.get("ports", []),
                    "vulns": d.get("vulns", []),
                    "last_update": d.get("last_update"),
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"Shodan host lookup failed: {exc}"}))
        sys.exit(1)


def cmd_virustotal(args):
    api_key = load_nadia_property("nadia.prop.virustotal.apiKey", "VIRUSTOTAL_API_KEY")
    if not api_key:
        print(json.dumps({"error": "Missing required property nadia.prop.virustotal.apiKey in ~/.nadia/nadia.properties"}))
        sys.exit(1)
    url = f"{VIRUSTOTAL_BASE_URL}/{urllib.parse.quote(args.type.strip())}/{urllib.parse.quote(args.target.strip())}"
    try:
        res = http_get_json(url, {"x-apikey": api_key})
        attrs = (res.get("data") or {}).get("attributes", {})
        print(
            json.dumps(
                {
                    "target": args.target,
                    "type": args.type,
                    "reputation": attrs.get("reputation"),
                    "last_analysis_stats": attrs.get("last_analysis_stats"),
                    "categories": attrs.get("categories"),
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"VirusTotal lookup failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query AbuseIPDB, Shodan, and VirusTotal threat intelligence.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ab = sub.add_parser("abuseipdb", help="Check IP abuse reputation on AbuseIPDB")
    p_ab.add_argument("--ip", required=True, help="IPv4 or IPv6 address")
    p_ab.add_argument("--days", type=int, default=90, help="Lookback window in days")
    p_ab.set_defaults(func=cmd_abuseipdb)

    p_sh = sub.add_parser("shodan", help="Inspect external IP ports and vulnerabilities on Shodan")
    p_sh.add_argument("--ip", required=True, help="IPv4 address")
    p_sh.set_defaults(func=cmd_shodan)

    p_vt = sub.add_parser("virustotal", help="Check IP, domain, or SHA-256 hash on VirusTotal")
    p_vt.add_argument("--type", choices=["ip_addresses", "domains", "files"], default="domains")
    p_vt.add_argument("--target", required=True, help="Domain name, IP address, or SHA-256 hash")
    p_vt.set_defaults(func=cmd_virustotal)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

