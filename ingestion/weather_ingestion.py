import requests
import json
import os
import logging
from datetime import datetime, timezone

# Base directory of THIS script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct absolute paths
BRONZE_DIR = os.path.join(BASE_DIR, "..", "bronze", "raw_weather")
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")

# Logging setup
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "ingestion.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

CITIES = [
    {"name": "oslo", "lat": 59.9139, "lon": 10.7522},
    {"name": "bergen", "lat": 60.3913, "lon": 5.3221},
    {"name": "trondheim", "lat": 63.4305, "lon": 10.3951},
    {"name": "stavanger", "lat": 58.9700, "lon": 5.7331},
    {"name": "tromso", "lat": 69.6492, "lon": 18.9553},
    {"name": "kristiansand", "lat": 58.1467, "lon": 7.9956},
]

API_URL = "https://api.met.no/weatherapi/locationforecast/2.0/compact"
USER_AGENT = "weather-pipeline/1.0 (contact: 5tazahmed5@gmail.com)"


def fetch_weather(city):
    headers = {"User-Agent": USER_AGENT}
    params = {"lat": city["lat"], "lon": city["lon"]}

    logging.info(f"Fetching weather for {city['name']}")

    try:
        response = requests.get(API_URL, headers=headers,
                                params=params, timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching {city['name']}: {e}")
        return None


def save_raw(city_name, data):
    city_folder = os.path.join(BRONZE_DIR, city_name)
    os.makedirs(city_folder, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
    file_path = os.path.join(city_folder, f"{timestamp}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    logging.info(f"Saved raw data for {city_name} → {file_path}")


def main():
    os.makedirs(BRONZE_DIR, exist_ok=True)

    for city in CITIES:
        data = fetch_weather(city)
        if data:
            save_raw(city["name"], data)

    logging.info("Bronze ingestion completed.")


if __name__ == "__main__":
    main()
