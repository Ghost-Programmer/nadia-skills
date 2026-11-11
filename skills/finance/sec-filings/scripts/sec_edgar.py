#!/usr/bin/env python3
"""
SEC EDGAR Corporate Filings & XBRL Facts CLI for Nadia.
Uses official data.sec.gov submissions and XBRL companyfacts endpoints.
Reads nadia.prop.sec.userAgent from ~/.nadia/nadia.properties.
"""

import argparse
import json
import os
from pathlib import Path
import sys
import urllib.request

SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
SEC_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"


def load_nadia_property(prop_key: str, default_val: str = "") -> str:
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
    return os.environ.get("SEC_USER_AGENT", default_val)


def get_sec_headers() -> dict:
    ua = load_nadia_property("nadia.prop.sec.userAgent", "MillerSoftwareSolutionsNadia/1.0 (support@nadia.ai)")
    return {"User-Agent": ua, "Accept": "application/json"}


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers=get_sec_headers())
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


def resolve_ticker_to_cik(ticker: str) -> tuple:
    clean = ticker.strip().upper()
    if clean.isdigit():
        return clean.zfill(10), clean
    data = http_get_json(SEC_TICKERS_URL)
    for entry in data.values():
        if str(entry.get("ticker", "")).upper() == clean:
            cik_str = str(entry.get("cik_str", "")).zfill(10)
            return cik_str, entry.get("title", clean)
    raise ValueError(f"Ticker '{ticker}' not found in SEC EDGAR registry.")


def cmd_filings(args):
    try:
        cik, company_title = resolve_ticker_to_cik(args.ticker)
        sub = http_get_json(SEC_SUBMISSIONS_URL.format(cik=cik))
        recent = sub.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        filing_dates = recent.get("filingDate", [])
        report_dates = recent.get("reportDate", [])
        accessions = recent.get("accessionNumber", [])
        primary_docs = recent.get("primaryDocument", [])
        descriptions = recent.get("primaryDocDescription", [])

        allowed_forms = (
            {f.strip().upper() for f in args.form.split(",") if f.strip()} if args.form else set()
        )
        cik_int = str(int(cik))
        results = []
        for idx, form in enumerate(forms):
            if allowed_forms and form.upper() not in allowed_forms:
                continue
            acc_raw = accessions[idx] if idx < len(accessions) else ""
            acc_no_dash = acc_raw.replace("-", "")
            doc_name = primary_docs[idx] if idx < len(primary_docs) else ""
            doc_url = (
                f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{acc_no_dash}/{doc_name}"
                if acc_no_dash and doc_name
                else ""
            )
            results.append(
                {
                    "form": form,
                    "filingDate": filing_dates[idx] if idx < len(filing_dates) else "",
                    "reportDate": report_dates[idx] if idx < len(report_dates) else "",
                    "accessionNumber": acc_raw,
                    "description": descriptions[idx] if idx < len(descriptions) else "",
                    "documentUrl": doc_url,
                }
            )
            if len(results) >= args.limit:
                break

        print(
            json.dumps(
                {
                    "ticker": args.ticker.upper(),
                    "cik": cik,
                    "company": sub.get("name") or company_title,
                    "sicDescription": sub.get("sicDescription"),
                    "count": len(results),
                    "filings": results,
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"SEC EDGAR filings lookup failed: {exc}"}))
        sys.exit(1)


def cmd_facts(args):
    try:
        cik, company_title = resolve_ticker_to_cik(args.ticker)
        facts_data = http_get_json(SEC_FACTS_URL.format(cik=cik))
        us_gaap = facts_data.get("facts", {}).get("us-gaap", {})
        concept = args.concept.strip()
        if concept not in us_gaap:
            matches = [k for k in us_gaap.keys() if concept.lower() in k.lower()]
            if matches:
                concept = matches[0]
            else:
                print(
                    json.dumps(
                        {
                            "error": f"Concept '{args.concept}' not found for {args.ticker}.",
                            "sampleConcepts": list(us_gaap.keys())[:25],
                        },
                        indent=2,
                    )
                )
                sys.exit(1)

        concept_obj = us_gaap[concept]
        units_map = concept_obj.get("units", {})
        unit_key = next(iter(units_map.keys()), "")
        entries = units_map.get(unit_key, [])
        filtered = [e for e in entries if e.get("form") in ("10-K", "10-Q")][-args.limit :]
        print(
            json.dumps(
                {
                    "ticker": args.ticker.upper(),
                    "cik": cik,
                    "company": facts_data.get("entityName") or company_title,
                    "concept": concept,
                    "label": concept_obj.get("label"),
                    "unit": unit_key,
                    "facts": list(reversed(filtered)),
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"SEC XBRL facts lookup failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Query SEC EDGAR filings and XBRL facts.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_f = sub.add_parser("filings", help="List recent SEC filings for a ticker or CIK")
    p_f.add_argument("--ticker", required=True, help="Stock ticker symbol or 10-digit CIK (e.g. AAPL, NVDA)")
    p_f.add_argument("--form", default="", help="Comma-separated form filter (e.g. 10-K,10-Q,8-K,4)")
    p_f.add_argument("--limit", type=int, default=15, help="Max filings to return")
    p_f.set_defaults(func=cmd_filings)

    p_x = sub.add_parser("facts", help="Fetch XBRL US-GAAP financial facts for a ticker")
    p_x.add_argument("--ticker", required=True, help="Stock ticker symbol or CIK")
    p_x.add_argument("--concept", default="Revenues", help="US-GAAP concept (e.g. Revenues, NetIncomeLoss, Assets)")
    p_x.add_argument("--limit", type=int, default=8, help="Max periods to return")
    p_x.set_defaults(func=cmd_facts)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

