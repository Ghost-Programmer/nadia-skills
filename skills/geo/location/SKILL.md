---
name: LocationSkill
description: Guidelines and Python CLI references for geocoding addresses, reverse geocoding, resolving place IDs, structured administrative queries, Plus Codes, boundary mapping, and IP geolocation.
tools: [run_command]
---

# Location & Geocoding Skill

This skill provides the capability to resolve addresses to coordinates (geocoding), resolve coordinates to addresses (reverse geocoding), translate unique place IDs, execute structured location matching, decode Open Location Code (OLC) Plus Codes, get landmark context descriptors, and determine map rendering boundaries.

These services are implemented as a self-contained, zero-dependency Python script located at `./skills/location/scripts/geocoding.py`.

## Setup Instructions

- **Python Runtime**:
  - Python 3.10+ installed and on system `PATH`.
  - Self-contained script using Python standard libraries (optional: `urllib.request` / `json`).
- **Script Location**:
  - Ensure `./skills/location/scripts/geocoding.py` (or `./skills/geo/location/scripts/geocoding.py`) exists and is executable.
- **Network & API Keys**:
  - Outbound internet access to OpenStreetMap / Nominatim / IP geolocation APIs.
  - Optional: Set `GEOCODING_API_KEY` or `IPINFO_TOKEN` if using private geocoding providers.

---

## Execution Guidelines

To run geocoding tasks, run the Python utility script using the `run_command` tool.

### 1. Geocode Freeform Address (`geocode_address`)
Converts freeform human-readable address queries to coordinates and metadata.
```bash
python ../skills/location/scripts/geocoding.py geocode_address --address "[address_query]" [--bounds "[left,top,right,bottom]"] [--region "[country_code_bias]"] [--language "[locale]"]
```

### 2. Reverse Geocode Coordinates (`reverse_geocode`)
Resolves latitude and longitude coordinates into structured street addresses and administrative zones.
```bash
python ../skills/location/scripts/geocoding.py reverse_geocode --lat [latitude] --lon [longitude] [--result_type "[street_address|locality|postal_code]"] [--language "[locale]"]
```

### 3. Geocode by Place ID (`geocode_by_place_id`)
Retrieves detailed coordinates and boundaries directly using a unique place ID.
```bash
python ../skills/location/scripts/geocoding.py geocode_by_place_id --place_id "[place_id]" [--language "[locale]"]
```

### 4. Structured Geocoding (`geocode_structured_address`)
Performs strict matching using individual address components to avoid misinterpretation.
```bash
python ../skills/location/scripts/geocoding.py geocode_structured_address --country "[country_code]" [--street_number "[number]"] [--route "[street_name]"] [--locality "[city]"] [--administrative_area "[state]"] [--postal_code "[zip]"]
```

### 5. Decode Plus Codes (`resolve_plus_code`)
Decodes global or compound Open Location Codes (Plus Codes) to coordinates.
```bash
python ../skills/location/scripts/geocoding.py resolve_plus_code --plus_code "[plus_code]" [--reference_location "[lat,lon]"]
```
*Note: Compound/short codes (e.g. `87C4VXMQ+6V`) require the `--reference_location` parameter.*

### 6. Landmark Proximity Context (`get_address_descriptors`)
Provides contextual, human-friendly spatial descriptions (e.g. landmarks and relative road positions) around a point.
```bash
python ../skills/location/scripts/geocoding.py get_address_descriptors --lat [latitude] --lon [longitude] [--max_landmarks [integer]]
```

### 7. Geographic Bounds (`get_location_bounds`)
Extracts recommended map rendering northeast/southwest coordinate pairs for a city, region, or area.
```bash
python ../skills/location/scripts/geocoding.py get_location_bounds --location_name "[location]" [--region "[country_code]"]
```

### 8. IP Geolocation (`get_ip_location`)
Locates the user by querying the network IP geolocation database.
```bash
python ../skills/location/scripts/geocoding.py get_ip_location
```
