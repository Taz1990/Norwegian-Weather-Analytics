import os
import json
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

# Blob connection
BLOB_CONN = os.getenv("AZURE_BLOB_CONNECTION_STRING")
blob_service = BlobServiceClient.from_connection_string(BLOB_CONN)

raw_container = blob_service.get_container_client("raw-weather-data")
silver_container = blob_service.get_container_client("silver-weather-data")


def clean_weather_json(raw_weather_json: dict) -> dict:
    """
    Clean raw weather JSON and return a normalized Silver JSON.
    Adjust this based on your actual API fields.
    """

    return {
        "city": raw_weather_json.get("city"),
        "temperature": float(raw_weather_json.get("temperature", 0)),
        "humidity": int(raw_weather_json.get("humidity", 0)),
        "wind_speed": float(raw_weather_json.get("wind_speed", 0)),
        "timestamp": raw_weather_json.get("timestamp"),
        "cleaned_at": datetime.now(timezone.utc).isoformat()
    }


def process_city_raw_to_silver(city: str):
    """
    Read raw JSON from Blob, clean it, and upload Silver JSON.
    """

    # Find latest raw blob for the city
    blobs = raw_container.list_blobs(name_starts_with=f"{city}/")
    latest_blob = None

    for blob in blobs:
        latest_blob = blob  # last blob in iteration = latest timestamp

    if latest_blob is None:
        print(f"No raw data found for {city}")
        return

    print(f"Processing raw blob: {latest_blob.name}")

    # Download raw JSON
    raw_data = raw_container.download_blob(latest_blob.name).readall()
    raw_json = json.loads(raw_data)

    # Clean JSON
    silver_json = clean_weather_json(raw_json)

    # Build Silver folder structure
    now = datetime.now(timezone.utc)
    year = now.year
    month = f"{now.month:02}"
    day = f"{now.day:02}"
    filename = f"{city}_clean_{now.strftime('%Y%m%d_%H%M')}.json"

    silver_path = f"{city}/{year}/{month}/{day}/{filename}"

    # Upload cleaned JSON
    silver_container.upload_blob(
        name=silver_path,
        data=json.dumps(silver_json),
        overwrite=True
    )

    print(f"Uploaded Silver JSON: {silver_path}")
    return silver_path


def process_all_cities_to_silver():
    cities = ["oslo", "bergen", "trondheim",
              "stavanger", "tromso", "kristiansand"]

    for city in cities:
        process_city_raw_to_silver(city)


if __name__ == "__main__":
    process_all_cities_to_silver()
