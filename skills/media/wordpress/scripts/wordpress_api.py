import sys
import json
import argparse
import urllib3
import requests
from requests.auth import HTTPBasicAuth

# Suppress SSL certificate warning outputs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    parser = argparse.ArgumentParser(description="WordPress REST API Standalone CLI")
    parser.add_argument("--url", required=True, help="WordPress site base URL")
    parser.add_argument("--password", required=True, help="WordPress Application Key/Password")
    parser.add_argument("--method", default="GET", help="HTTP method (GET, POST, PUT, DELETE)")
    parser.add_argument("--endpoint", required=True, help="REST API endpoint (e.g., /wp-json/wp/v2/posts)")
    parser.add_argument("--params", help="Query parameters as a JSON object string")
    parser.add_argument("--body", help="Request body data as a JSON object/array string")

    args = parser.parse_args()

    site_url = args.url.rstrip('/')
    password = args.password

    # Build final URL
    endpoint = args.endpoint
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint
    if not endpoint.startswith('/wp-json/'):
        endpoint = '/wp-json' + endpoint

    full_url = site_url + endpoint

    # Setup parameters
    params_dict = None
    if args.params:
        try:
            params_dict = json.loads(args.params)
        except Exception as e:
            print(json.dumps({"error": f"Failed to parse query params JSON: {e}"}))
            sys.exit(1)

    # Setup body JSON data
    body_obj = None
    if args.body:
        try:
            body_obj = json.loads(args.body)
        except Exception as e:
            print(json.dumps({"error": f"Failed to parse body JSON: {e}"}))
            sys.exit(1)

    # Create auth object
    auth = HTTPBasicAuth('agent_service_account', password)

    try:
        response = requests.request(
            method=args.method.upper(),
            url=full_url,
            auth=auth,
            params=params_dict,
            json=body_obj,
            verify=False  # Disable SSL verification for local sandboxes
        )

        sys.stderr.write(f"[WordPress CLI] Response Status: {response.status_code}\n")
        sys.stderr.flush()

        try:
            # Output response text directly. If it is JSON, print it, otherwise print text.
            parsed_json = response.json()
            print(json.dumps(parsed_json))
        except ValueError:
            print(response.text)

        if response.status_code >= 400:
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"Request Exception: {e}"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Connection Error: {e}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
