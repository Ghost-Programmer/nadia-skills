#!/usr/bin/env python3
"""
UI Design Assets, SVG Icons & Color Palettes CLI for Nadia (@UI Designer).
Queries Iconify API, Colormind Palette API, and DummyImage URLs.
Keyless (no API keys required).
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request

ICONIFY_SEARCH_URL = "https://api.iconify.design/search"
ICONIFY_BASE_URL = "https://api.iconify.design"
COLORMIND_URL = "http://colormind.io/api/"
USER_AGENT = "Nadia-Agent-DesignAssets/1.0"


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8")


def cmd_icons(args):
    params = {"query": args.query, "limit": str(args.limit)}
    if args.prefix:
        params["prefix"] = args.prefix
    url = f"{ICONIFY_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    try:
        data = http_get_json(url)
        icons = data.get("icons", [])
        results = [
            {
                "icon": ic,
                "svg_url": f"{ICONIFY_BASE_URL}/{ic.replace(':', '/')}.svg",
            }
            for ic in icons
        ]
        print(json.dumps({"query": args.query, "count": len(results), "icons": results}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"Iconify search failed: {exc}"}))
        sys.exit(1)


def cmd_svg(args):
    icon = args.icon.strip()
    if ":" not in icon:
        print(json.dumps({"error": "Icon identifier must be in 'prefix:name' format (e.g., mdi:home)."}))
        sys.exit(1)
    prefix, name = icon.split(":", 1)
    url = f"{ICONIFY_BASE_URL}/{urllib.parse.quote(prefix)}/{urllib.parse.quote(name)}.svg"
    try:
        svg_text = http_get_text(url)
        print(json.dumps({"icon": icon, "svg_url": url, "svg": svg_text}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"SVG fetch failed for '{icon}': {exc}"}))
        sys.exit(1)


def cmd_palette(args):
    payload = json.dumps({"model": "ui"}).encode("utf-8")
    req = urllib.request.Request(
        COLORMIND_URL,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        method="POST",
    )
    roles = ["light_shade", "light_accent", "main_brand", "dark_accent", "dark_shade"]
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        rgb_list = data.get("result", [])
        palette = []
        for idx, rgb in enumerate(rgb_list):
            hex_code = "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
            palette.append(
                {
                    "role": roles[idx] if idx < len(roles) else f"color_{idx + 1}",
                    "hex": hex_code,
                    "rgb": rgb,
                }
            )
        print(json.dumps({"model": "ui", "palette": palette}, indent=2))
    except Exception as exc:
        print(json.dumps({"error": f"Colormind palette generation failed: {exc}"}))
        sys.exit(1)


def cmd_placeholder(args):
    bg = args.bg.lstrip("#")
    fg = args.fg.lstrip("#")
    text_param = f"&text={urllib.parse.quote(args.text)}" if args.text else ""
    url = f"https://dummyimage.com/{args.width}x{args.height}/{bg}/{fg}.png{text_param}"
    print(
        json.dumps(
            {
                "width": args.width,
                "height": args.height,
                "background_hex": f"#{bg}",
                "foreground_hex": f"#{fg}",
                "text": args.text,
                "url": url,
            },
            indent=2,
        )
    )


def main():
    parser = argparse.ArgumentParser(description="Search SVG icons, generate UI color palettes, and build placeholders.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ic = sub.add_parser("icons", help="Search open-source SVG icons via Iconify")
    p_ic.add_argument("--query", required=True, help="Icon keyword (e.g., chart, settings, user)")
    p_ic.add_argument("--prefix", default="", help="Optional icon set prefix (e.g., mdi, lucide, tabler)")
    p_ic.add_argument("--limit", type=int, default=15, help="Max icons to return")
    p_ic.set_defaults(func=cmd_icons)

    p_svg = sub.add_parser("svg", help="Fetch raw SVG markup for an icon (prefix:name)")
    p_svg.add_argument("--icon", required=True, help="Icon ID (e.g., mdi:rocket-launch)")
    p_svg.set_defaults(func=cmd_svg)

    p_pal = sub.add_parser("palette", help="Generate a 5-color UI palette via Colormind")
    p_pal.set_defaults(func=cmd_palette)

    p_ph = sub.add_parser("placeholder", help="Generate a DummyImage placeholder graphic URL")
    p_ph.add_argument("--width", type=int, default=600, help="Width in px")
    p_ph.add_argument("--height", type=int, default=400, help="Height in px")
    p_ph.add_argument("--bg", default="1e293b", help="Background hex color")
    p_ph.add_argument("--fg", default="f8fafc", help="Foreground text hex color")
    p_ph.add_argument("--text", default="", help="Overlay text")
    p_ph.set_defaults(func=cmd_placeholder)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

