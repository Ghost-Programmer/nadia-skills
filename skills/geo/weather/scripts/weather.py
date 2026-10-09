import sys
import os
import json
import urllib.request
import urllib.parse
import argparse

# Add location skill directory to path to reuse the geocoding service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'location', 'scripts')))

try:
    import geocoding
except ImportError as e:
    print(json.dumps({"error": f"Failed to import geocoding service: {str(e)}"}))
    sys.exit(1)

def get_weather_for_address(address, forecast_days=1):
    # Resolve location coordinates and country using geocoding service
    geo_res = geocoding.geocode_address(address)
    if "error" in geo_res:
        return geo_res

    lat = geo_res.get("lat")
    lon = geo_res.get("lon")
    display_name = geo_res.get("display_name", address)
    
    address_details = geo_res.get("address", {})
    country_code = address_details.get("country_code", "").lower()

    # Determine whether to use Fahrenheit or Celsius
    # Countries that use Fahrenheit: US, Liberia (lr), Myanmar (mm), Bahamas (bs), Belize (bz), Cayman Islands (ky), Palau (pw)
    f_countries = {"us", "lr", "mm", "bs", "bz", "ky", "pw"}
    use_fahrenheit = country_code in f_countries
    temp_unit = "fahrenheit" if use_fahrenheit else "celsius"
    unit_symbol = "°F" if use_fahrenheit else "°C"
    
    # Precipitation units: inch for US/etc, mm elsewhere
    precip_unit = "inch" if use_fahrenheit else "mm"
    precip_symbol = " in" if use_fahrenheit else " mm"

    # Query api.open-meteo.com for current conditions and hourly forecast
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,precipitation,wind_speed_10m,wind_direction_10m,is_day,weather_code"
        f"&hourly=temperature_2m,precipitation,weather_code"
        f"&temperature_unit={temp_unit}&precipitation_unit={precip_unit}&forecast_days={forecast_days}"
    )
    
    headers = {"User-Agent": "NadiaAgent/1.0 (jeff@gemini)"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            weather_data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}

    current = weather_data.get("current", {})
    hourly = weather_data.get("hourly", {})
    
    # Format hourly forecast
    hourly_records = []
    if hourly:
        times = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        precips = hourly.get("precipitation", [])
        w_codes = hourly.get("weather_code", [])
        
        for i in range(len(times)):
            hourly_records.append({
                "time": times[i],
                "temperature": f"{temps[i]}{unit_symbol}" if i < len(temps) else None,
                "precipitation": f"{precips[i]}{precip_symbol}" if i < len(precips) else None,
                "weathercode": w_codes[i] if i < len(w_codes) else None
            })

    return {
        "location": display_name,
        "latitude": lat,
        "longitude": lon,
        "country_code": country_code,
        "temperature_unit": temp_unit,
        "api_url": url,
        "current": {
            "time": current.get("time"),
            "temperature": f"{current.get('temperature_2m')}{unit_symbol}",
            "precipitation": f"{current.get('precipitation')}{precip_symbol}",
            "windspeed": f"{current.get('wind_speed_10m')} km/h",
            "winddirection": f"{current.get('wind_direction_10m')}°",
            "is_day": current.get("is_day"),
            "weathercode": current.get("weather_code")
        },
        "hourly": hourly_records
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch weather details for an address using Nominatim geocoding and Open-Meteo API.")
    parser.add_argument("--address", required=True, help="Address or location name to query weather for.")
    parser.add_argument("--days", type=int, default=1, choices=range(1, 17), help="Number of forecast days (1-16, default 1).")
    args = parser.parse_args()

    result = get_weather_for_address(args.address, forecast_days=args.days)
    print(json.dumps(result, indent=2))
