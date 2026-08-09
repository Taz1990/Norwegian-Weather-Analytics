import os
import json
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure Blob connection string from .env
BLOB_CONN = os.getenv("AZURE_BLOB_CONNECTION_STRING")

# Initialize Blob client
blob_service = BlobServiceClient.from_connection_string(BLOB_CONN)
container = blob_service.get_container_client("raw-weather-data")


def upload_raw_weather(city: str, raw_weather_json: dict):
    """
    Upload raw weather JSON to Azure Blob Storage using a clean folder structure:
    raw-weather/city/YYYY/MM/DD/city_YYYYMMDD_HHMM.json
    """

    # Current timestamp
    now = datetime.now(timezone.utc)

    # Build folder structure
    year = now.year
    month = f"{now.month:02}"
    day = f"{now.day:02}"
    timestamp = now.strftime("%Y%m%d_%H%M")

    # File name
    filename = f"{city}_{timestamp}.json"

    # Full blob path (this creates folders automatically)
    blob_path = f"{city}/{year}/{month}/{day}/{filename}"

    # Upload JSON to Blob Storage
    container.upload_blob(
        name=blob_path,
        data=json.dumps(raw_weather_json),
        overwrite=True
    )

    print(f"Uploaded to Blob Storage: {blob_path}")
    return blob_path


# Example usage
if __name__ == "__main__":
    sample_weather = {
        "city": "oslo",
        "temperature": 18.5,
        "humidity": 60,
        "wind_speed": 4.2,
        "timestamp": "2026-08-09T09:00:00Z"
    }

    upload_raw_weather("oslo", sample_weather)
