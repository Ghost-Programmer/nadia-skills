#!/usr/bin/env python3
"""
Academic Literature & Preprints CLI for Nadia.
Queries arXiv Atom API, Europe PMC REST API, Crossref Works API, and Open Library Search API.
Keyless (no API keys required).
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ARXIV_API_URL = "http://export.arxiv.org/api/query"
EUROPE_PMC_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CROSSREF_URL = "https://api.crossref.org/works"
OPENLIBRARY_URL = "https://openlibrary.org/search.json"
USER_AGENT = "Nadia-Agent-AcademicPapers/1.0 (mailto:support@nadia.ai)"


def http_get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read().decode("utf-8", errors="replace")


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def cmd_arxiv(args):
    params = {
        "search_query": f"all:{args.query}",
        "start": "0",
        "max_results": str(args.limit),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"
    try:
        xml_text = http_get_text(url)
        root = ET.fromstring(xml_text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []
        for entry in root.findall("atom:entry", ns):
            title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip().replace("\n", " ")
            summary = (entry.findtext("atom:summary", default="", namespaces=ns) or "").strip().replace("\n", " ")
            published = entry.findtext("atom:published", default="", namespaces=ns)
            entry_id = entry.findtext("atom:id", default="", namespaces=ns)
            authors = [
                a.findtext("atom:name", default="", namespaces=ns)
                for a in entry.findall("atom:author", ns)
            ]
            papers.append(
                {
                    "id": entry_id,
                    "title": title,
                    "authors": authors,
                    "published": published,
                    "summary": summary[:500],
                    "pdf_url": entry_id.replace("/abs/", "/pdf/") if "/abs/" in entry_id else entry_id,
                }
            )
        print(json.dumps({"source": "arXiv", "query": args.query, "count": len(papers), "papers": papers}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"arXiv query failed: {exc}"}))
        sys.exit(1)


def cmd_europepmc(args):
    params = {
        "query": args.query,
        "format": "json",
        "pageSize": str(args.limit),
        "resultType": "core",
    }
    url = f"{EUROPE_PMC_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        results = data.get("resultList", {}).get("result", [])
        papers = []
        for r in results:
            papers.append(
                {
                    "id": r.get("id"),
                    "source": r.get("source"),
                    "pmid": r.get("pmid"),
                    "pmcid": r.get("pmcid"),
                    "doi": r.get("doi"),
                    "title": r.get("title"),
                    "authorString": r.get("authorString"),
                    "journalTitle": (r.get("journalInfo") or {}).get("journal", {}).get("title"),
                    "pubYear": r.get("pubYear"),
                    "citedByCount": r.get("citedByCount"),
                    "isOpenAccess": r.get("isOpenAccess"),
                    "abstractText": (r.get("abstractText") or "")[:500],
                }
            )
        print(
            json.dumps(
                {
                    "source": "Europe PMC",
                    "query": args.query,
                    "hitCount": data.get("hitCount"),
                    "count": len(papers),
                    "papers": papers,
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"Europe PMC query failed: {exc}"}))
        sys.exit(1)


def cmd_crossref(args):
    try:
        if args.doi:
            url = f"{CROSSREF_URL}/{urllib.parse.quote(args.doi.strip())}"
            data = http_get_json(url)
            items = [data.get("message", {})]
        else:
            params = {"query": args.query, "rows": str(args.limit)}
            url = f"{CROSSREF_URL}?{urllib.parse.urlencode(params)}"
            data = http_get_json(url)
            items = data.get("message", {}).get("items", [])

        works = []
        for w in items:
            authors = [
                f"{a.get('given', '')} {a.get('family', '')}".strip()
                for a in (w.get("author") or [])[:8]
            ]
            works.append(
                {
                    "doi": w.get("DOI"),
                    "title": (w.get("title") or [""])[0],
                    "authors": authors,
                    "containerTitle": (w.get("container-title") or [""])[0],
                    "type": w.get("type"),
                    "isReferencedByCount": w.get("is-referenced-by-count"),
                    "url": w.get("URL"),
                }
            )
        print(json.dumps({"source": "Crossref", "count": len(works), "works": works}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"Crossref query failed: {exc}"}))
        sys.exit(1)


def cmd_books(args):
    params = {"q": args.query, "limit": str(args.limit)}
    url = f"{OPENLIBRARY_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        books = []
        for doc in data.get("docs", [])[: args.limit]:
            books.append(
                {
                    "title": doc.get("title"),
                    "author_name": doc.get("author_name", []),
                    "first_publish_year": doc.get("first_publish_year"),
                    "edition_count": doc.get("edition_count"),
                    "isbn": (doc.get("isbn") or [])[:3],
                    "key": doc.get("key"),
                    "url": f"https://openlibrary.org{doc.get('key', '')}",
                }
            )
        print(json.dumps({"source": "Open Library", "count": len(books), "books": books}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"Open Library search failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Search arXiv, Europe PMC, Crossref, and Open Library.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ax = sub.add_parser("arxiv", help="Search arXiv preprints")
    p_ax.add_argument("--query", required=True, help="Search query")
    p_ax.add_argument("--limit", type=int, default=10, help="Max results")
    p_ax.set_defaults(func=cmd_arxiv)

    p_ep = sub.add_parser("europepmc", help="Search Europe PMC biomedical & life sciences papers")
    p_ep.add_argument("--query", required=True, help="Search query")
    p_ep.add_argument("--limit", type=int, default=10, help="Max results")
    p_ep.set_defaults(func=cmd_europepmc)

    p_cr = sub.add_parser("crossref", help="Search Crossref works or look up a DOI")
    p_cr.add_argument("--query", default="", help="Search query")
    p_cr.add_argument("--doi", default="", help="Specific DOI to resolve")
    p_cr.add_argument("--limit", type=int, default=10, help="Max results")
    p_cr.set_defaults(func=cmd_crossref)

    p_bk = sub.add_parser("books", help="Search books on Open Library")
    p_bk.add_argument("--query", required=True, help="Book title or author query")
    p_bk.add_argument("--limit", type=int, default=10, help="Max results")
    p_bk.set_defaults(func=cmd_books)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

