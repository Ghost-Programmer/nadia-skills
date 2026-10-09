import sys
import json
import urllib.request
import urllib.parse
import argparse

USER_AGENT = "NadiaAgent/1.0 (jeff@gemini)"

def query_nominatim(url, language=None):
    headers = {"User-Agent": USER_AGENT}
    if language:
        headers["Accept-Language"] = language
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(json.dumps({"error": f"HTTP query failed: {str(e)}"}))
        sys.exit(1)

def geocode_address(address, bounds=None, region=None, language=None):
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(address)}&format=json&addressdetails=1"
    if bounds:
        url += f"&viewbox={urllib.parse.quote(bounds)}&bounded=1"
    if region:
        url += f"&countrycodes={urllib.parse.quote(region)}"
    
    results = query_nominatim(url, language)
    if isinstance(results, list) and len(results) > 0:
        return results[0]
    return {"error": f"No results found for address: {address}"}

def reverse_geocode(latitude, longitude, result_type=None, location_type=None, language=None):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&addressdetails=1"
    if result_type:
        zoom = 18
        if result_type == "locality":
            zoom = 10
        elif result_type == "postal_code":
            zoom = 15
        url += f"&zoom={zoom}"
        
    return query_nominatim(url, language)

def geocode_by_place_id(place_id, language=None):
    url = f"https://nominatim.openstreetmap.org/details?place_id={urllib.parse.quote(place_id)}&format=json"
    return query_nominatim(url, language)

def geocode_structured_address(street_number=None, route=None, locality=None, administrative_area=None, postal_code=None, country=None):
    url = "https://nominatim.openstreetmap.org/search?format=json&addressdetails=1"
    if street_number and route:
        url += f"&street={urllib.parse.quote(f'{street_number} {route}')}"
    elif route:
        url += f"&street={urllib.parse.quote(route)}"
    if locality:
        url += f"&city={urllib.parse.quote(locality)}"
    if administrative_area:
        url += f"&state={urllib.parse.quote(administrative_area)}"
    if postal_code:
        url += f"&postalcode={urllib.parse.quote(postal_code)}"
    if country:
        url += f"&country={urllib.parse.quote(country)}"
        
    results = query_nominatim(url)
    if isinstance(results, list) and len(results) > 0:
        return results[0]
    return {"error": "No results found for structured search."}

def resolve_plus_code(plus_code, reference_location=None):
    # Try local decode via openlocationcode if installed
    try:
        import openlocationcode
        # check if it is compound code (short code)
        if openlocationcode.isShort(plus_code):
            if reference_location:
                parts = reference_location.split(",")
                ref_lat = float(parts[0])
                ref_lon = float(parts[1])
                plus_code = openlocationcode.recoverNearest(plus_code, ref_lat, ref_lon)
            else:
                return {"error": "Reference location (lat,lon) is required for compound Plus Code"}
        
        area = openlocationcode.decode(plus_code)
        return {
            "global_code": plus_code,
            "center_latitude": area.latitudeCenter,
            "center_longitude": area.longitudeCenter,
            "southwest_latitude": area.latitudeLo,
            "southwest_longitude": area.longitudeLo,
            "northeast_latitude": area.latitudeHi,
            "northeast_longitude": area.longitudeHi
        }
    except ImportError:
        # Fallback to geocode search via Nominatim
        return geocode_address(plus_code)

def get_address_descriptors(latitude, longitude, max_landmarks=None):
    res = reverse_geocode(latitude, longitude)
    if "error" in res:
        return res
    
    display_name = res.get("display_name", "")
    address = res.get("address", {})
    
    road = address.get("road", "")
    suburb = address.get("suburb", "")
    city = address.get("city", "")
    county = address.get("county", "")
    state = address.get("state", "")
    country = address.get("country", "")
    
    return {
        "resolved_address": display_name,
        "road": road,
        "neighborhood": suburb,
        "locality": city,
        "administrative_area": county or state,
        "country": country,
        "landmarks": [
            {"name": road if road else "Main Road", "type": "road_intersection", "proximity": "near"},
            {"name": suburb if suburb else (city if city else state), "type": "general_area", "proximity": "within"}
        ]
    }

def get_location_bounds(location_name, region=None):
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(location_name)}&format=json&limit=1"
    if region:
        url += f"&countrycodes={urllib.parse.quote(region)}"
        
    results = query_nominatim(url)
    if isinstance(results, list) and len(results) > 0:
        first = results[0]
        bbox = first.get("boundingbox", [])
        if len(bbox) == 4:
            return {
                "northeast": {"latitude": float(bbox[1]), "longitude": float(bbox[3])},
                "southwest": {"latitude": float(bbox[0]), "longitude": float(bbox[2])}
            }
    return {"error": f"No bounds found for location: {location_name}"}

def get_ip_location():
    req = urllib.request.Request("http://ip-api.com/json/", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            if res.get("status") == "success":
                return {
                    "city": res.get("city"),
                    "region": res.get("regionName"),
                    "country": res.get("country"),
                    "zip": res.get("zip"),
                    "latitude": res.get("lat"),
                    "longitude": res.get("lon")
                }
            return {"error": res.get("message", "IP resolution failed")}
    except Exception as e:
        return {"error": f"IP location request failed: {str(e)}"}

def main():
    parser = argparse.ArgumentParser(description="Nadia Geocoding and Location Tools CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # geocode_address
    p_geo = subparsers.add_parser("geocode_address")
    p_geo.add_argument("--address", required=True)
    p_geo.add_argument("--bounds")
    p_geo.add_argument("--region")
    p_geo.add_argument("--language")
    
    # reverse_geocode
    p_rev = subparsers.add_parser("reverse_geocode")
    p_rev.add_argument("--lat", type=float, required=True)
    p_rev.add_argument("--lon", type=float, required=True)
    p_rev.add_argument("--result_type")
    p_rev.add_argument("--location_type")
    p_rev.add_argument("--language")
    
    # geocode_by_place_id
    p_pid = subparsers.add_parser("geocode_by_place_id")
    p_pid.add_argument("--place_id", required=True)
    p_pid.add_argument("--language")
    
    # geocode_structured_address
    p_str = subparsers.add_parser("geocode_structured_address")
    p_str.add_argument("--street_number")
    p_str.add_argument("--route")
    p_str.add_argument("--locality")
    p_str.add_argument("--administrative_area")
    p_str.add_argument("--postal_code")
    p_str.add_argument("--country", required=True)
    
    # resolve_plus_code
    p_plus = subparsers.add_parser("resolve_plus_code")
    p_plus.add_argument("--plus_code", required=True)
    p_plus.add_argument("--reference_location")
    
    # get_address_descriptors
    p_desc = subparsers.add_parser("get_address_descriptors")
    p_desc.add_argument("--lat", type=float, required=True)
    p_desc.add_argument("--lon", type=float, required=True)
    p_desc.add_argument("--max_landmarks", type=int)
    
    # get_location_bounds
    p_bounds = subparsers.add_parser("get_location_bounds")
    p_bounds.add_argument("--location_name", required=True)
    p_bounds.add_argument("--region")
    
    # get_ip_location
    subparsers.add_parser("get_ip_location")
    
    args = parser.parse_args()
    
    if args.command == "geocode_address":
        res = geocode_address(args.address, args.bounds, args.region, args.language)
    elif args.command == "reverse_geocode":
        res = reverse_geocode(args.lat, args.lon, args.result_type, args.location_type, args.language)
    elif args.command == "geocode_by_place_id":
        res = geocode_by_place_id(args.place_id, args.language)
    elif args.command == "geocode_structured_address":
        res = geocode_structured_address(args.street_number, args.route, args.locality, args.administrative_area, args.postal_code, args.country)
    elif args.command == "resolve_plus_code":
        res = resolve_plus_code(args.plus_code, args.reference_location)
    elif args.command == "get_address_descriptors":
        res = get_address_descriptors(args.lat, args.lon, args.max_landmarks)
    elif args.command == "get_location_bounds":
        res = get_location_bounds(args.location_name, args.region)
    elif args.command == "get_ip_location":
        res = get_ip_location()
        
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
