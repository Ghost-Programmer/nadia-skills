#!/usr/bin/env python3
"""
Lexicon, Dictionary & Literary Reference CLI for Nadia (@Journalist).
Queries Free Dictionary API (dictionaryapi.dev) and PoetryDB (poetrydb.org).
Keyless (no API keys required).
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request

DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"
POETRYDB_BASE_URL = "https://poetrydb.org"
USER_AGENT = "Nadia-Agent-Lexicon/1.0"


def http_get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def cmd_define(args):
    word = urllib.parse.quote(args.word.strip().lower())
    url = f"{DICTIONARY_API_URL}/{word}"
    try:
        entries = http_get_json(url)
        if not isinstance(entries, list) or not entries:
            print(json.dumps({"word": args.word, "found": False}))
            return
        entry = entries[0]
        meanings = []
        for m in entry.get("meanings", []):
            defs = [
                {
                    "definition": d.get("definition"),
                    "example": d.get("example"),
                }
                for d in m.get("definitions", [])[:4]
            ]
            meanings.append(
                {
                    "partOfSpeech": m.get("partOfSpeech"),
                    "definitions": defs,
                    "synonyms": m.get("synonyms", [])[:10],
                    "antonyms": m.get("antonyms", [])[:10],
                }
            )
        print(
            json.dumps(
                {
                    "word": entry.get("word"),
                    "phonetic": entry.get("phonetic"),
                    "origin": entry.get("origin"),
                    "meanings": meanings,
                },
                indent=2,
            )
        )
    except Exception as exc:
        print(json.dumps({"error": f"Dictionary lookup failed for '{args.word}': {exc}"}))
        sys.exit(1)


def cmd_poetry(args):
    if args.author:
        url = f"{POETRYDB_BASE_URL}/author/{urllib.parse.quote(args.author.strip())}"
    elif args.title:
        url = f"{POETRYDB_BASE_URL}/title/{urllib.parse.quote(args.title.strip())}"
    else:
        print(json.dumps({"error": "Provide either --author or --title."}))
        sys.exit(1)
    try:
        items = http_get_json(url)
        if not isinstance(items, list):
            print(json.dumps({"found": False, "response": items}))
            return
        poems = []
        for p in items[: args.limit]:
            poems.append(
                {
                    "title": p.get("title"),
                    "author": p.get("author"),
                    "linecount": p.get("linecount"),
                    "lines": (p.get("lines") or [])[:24],
                }
            )
        print(json.dumps({"count": len(poems), "poems": poems}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"PoetryDB lookup failed: {exc}"}))
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Look up word definitions, synonyms, and literary verse.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_def = sub.add_parser("define", help="Look up word definitions, phonetics, and synonyms")
    p_def.add_argument("--word", required=True, help="English word to define")
    p_def.set_defaults(func=cmd_define)

    p_po = sub.add_parser("poetry", help="Search classic poetry by author or title")
    p_po.add_argument("--author", default="", help="Poet name (e.g. Emily Dickinson, Shakespeare)")
    p_po.add_argument("--title", default="", help="Poem title keyword")
    p_po.add_argument("--limit", type=int, default=5, help="Max poems to return")
    p_po.set_defaults(func=cmd_poetry)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

