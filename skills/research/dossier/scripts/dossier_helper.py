import argparse
import hashlib
import json
import sys
import urllib.request
import urllib.parse

def md5_hex(text: str) -> str:
    if not text:
        return ""
    normalized = text.strip().lower()
    return hashlib.md5(normalized.encode('utf-8')).hexdigest()

def get_gravatar_email_url(email: str) -> str:
    if not email or not email.strip():
        return ""
    return f"https://en.gravatar.com/{md5_hex(email)}"

def get_gravatar_username_url(username: str) -> str:
    if not username or not username.strip():
        return ""
    return f"https://gravatar.com/{username.strip()}"

def generate_profile_urls(username: str, email: str = None) -> dict:
    u = username.strip() if username else ""
    e = email.strip() if email else ""
    
    profiles = {}
    if u:
        profiles["github"] = f"https://github.com/{u}"
        profiles["linkedin"] = f"https://www.linkedin.com/in/{u}"
        profiles["x"] = f"https://x.com/{u}"
        profiles["facebook"] = f"https://www.facebook.com/{u}/"
        profiles["gravatar_user"] = get_gravatar_username_url(u)
    
    if e:
        profiles["gravatar_email"] = get_gravatar_email_url(e)
        profiles["gravatar_avatar"] = f"https://www.gravatar.com/avatar/{md5_hex(e)}?d=identicon&s=256"
        
    return profiles

def fetch_gravatar_profile(identifier: str, is_email: bool = False):
    """Fetches public JSON profile from Gravatar if available."""
    try:
        if is_email:
            hash_val = md5_hex(identifier)
            url = f"https://en.gravatar.com/{hash_val}.json"
        else:
            url = f"https://gravatar.com/{identifier.strip()}.json"
            
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data.get("entry", [{}])[0]
    except Exception:
        return None
    return None

def main():
    parser = argparse.ArgumentParser(description="Dossier identity and social footprint helper CLI")
    parser.add_argument("--username", help="Primary username or social handle")
    parser.add_argument("--email", help="Target email address")
    parser.add_argument("--name", help="Full name of the individual")
    parser.add_argument("--company", help="Affiliated company or organization")
    parser.add_argument("--fetch-gravatar", action="store_true", help="Attempt to fetch public Gravatar profile JSON")
    
    args = parser.parse_args()
    
    if not (args.username or args.email or args.name):
        parser.print_help()
        sys.exit(1)
        
    result = {
        "name": args.name or "",
        "username": args.username or "",
        "email": args.email or "",
        "company": args.company or "",
        "urls": generate_profile_urls(args.username, args.email),
        "search_queries": []
    }
    
    # Generate high-signal search queries
    if args.name:
        result["search_queries"].append(f'"{args.name}"')
        if args.company:
            result["search_queries"].append(f'"{args.name}" "{args.company}"')
        if args.username:
            result["search_queries"].append(f'"{args.name}" "{args.username}"')
    if args.email:
        result["search_queries"].append(f'"{args.email}"')
    if args.username:
        result["search_queries"].append(f'"{args.username}" site:github.com OR site:linkedin.com OR site:x.com')
        
    if args.fetch_gravatar:
        gravatar_info = None
        if args.email:
            gravatar_info = fetch_gravatar_profile(args.email, is_email=True)
        if not gravatar_info and args.username:
            gravatar_info = fetch_gravatar_profile(args.username, is_email=False)
        result["gravatar_profile"] = gravatar_info
        
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
