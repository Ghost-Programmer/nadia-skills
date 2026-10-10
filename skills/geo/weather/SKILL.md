---
name: WeatherSkill
description: Guidelines and Python CLI references for fetching current weather forecasts for a location, automatically resolving coordinates via the location service and selecting Fahrenheit or Celsius based on country rules. Retrieves current precipitation and hourly forecasts.
tools: [run_command]
---

# Weather Forecast Skill (Python CLI)

This skill instructs the agent on how to retrieve the current weather and hourly forecasts for any location using the `api.open-meteo.com` forecast API and the geocoding location service.

The weather service is implemented as a Python script located at `./skills/weather/scripts/weather.py`. It integrates with the geocoding service at `./skills/location/scripts/geocoding.py` to resolve address queries into coordinates and look up the country code to dynamically select Fahrenheit (°F) or Celsius (°C).

## Setup Instructions

- **Python Runtime & Dependencies**:
  - Python 3.10+ installed and on system `PATH`.
  - Install required Python package:
    ```bash
    pip install requests
    ```
- **Script Location**:
  - Weather script located at `./skills/weather/scripts/weather.py` (or `./skills/geo/weather/scripts/weather.py`).
- **Network & API Access**:
  - Open-Meteo public API (`https://api.open-meteo.com`) requires no API key.
  - Outbound internet access on port 80/443.

---

## Temperature and Precipitation Unit Determination

- **Fahrenheit (°F) and Inches (in)**: Used automatically for locations in the United States (`us`), Liberia (`lr`), Myanmar (`mm`), Bahamas (`bs`), Belize (`bz`), Cayman Islands (`ky`), and Palau (`pw`).
- **Celsius (°C) and Millimeters (mm)**: Used for all other countries by default.

## Execution Pattern

Call the `run_command` tool to run the weather Python script.

### Basic Syntax

```bash
python ../skills/weather/scripts/weather.py --address "[location_name]" [--days [forecast_days]]
```

### Options

- `--address`: Location name, ZIP code, or coordinates (required).
- `--days`: Number of forecast days to retrieve for the hourly breakdown (1 to 16, default: 1).

### Example

Query the weather for New York for 1 day:

```bash
python ../skills/weather/scripts/weather.py --address "New York" --days 1
```

Response JSON structure returned:

```json
{
  "location": "New York, United States",
  "latitude": "40.7127281",
  "longitude": "-74.0060152",
  "country_code": "us",
  "temperature_unit": "fahrenheit",
  "api_url": "https://api.open-meteo.com/v1/forecast?latitude=40.712728&longitude=-74.006015&current=temperature_2m,precipitation,wind_speed_10m,wind_direction_10m,is_day,weather_code&hourly=temperature_2m,precipitation,weather_code&temperature_unit=fahrenheit&precipitation_unit=inch&forecast_days=1",
  "current": {
    "time": "2026-08-21T13:15",
    "temperature": "65.2°F",
    "precipitation": "0.0 in",
    "windspeed": "15.5 km/h",
    "winddirection": "3°",
    "is_day": 1,
    "weathercode": 3
  },
  "hourly": [
    {
      "time": "2026-08-21T00:00",
      "temperature": "19.0°F",
      "precipitation": "0.14 in",
      "weathercode": 3
    },
    ...
  ]
}
```
