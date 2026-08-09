import os
import json
import psycopg2
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL credentials
POSTGRES_USER = os.getenv("PGUSER")
POSTGRES_PASSWORD = os.getenv("PGPASSWORD")
POSTGRES_DB = os.getenv("PGDATABASE")
POSTGRES_PORT = os.getenv("PGPORT")
POSTGRES_HOST = os.getenv("PGHOST")

# Blob Storage
BLOB_CONN = os.getenv("AZURE_BLOB_CONNECTION_STRING")
blob_service = BlobServiceClient.from_connection_string(BLOB_CONN)
silver_container = blob_service.get_container_client("silver-weather-data")


def get_latest_silver_blob(city: str):
    """Find the latest cleaned Silver JSON for a city."""
    blobs = silver_container.list_blobs(name_starts_with=f"{city}/")
    latest_blob = None

    for blob in blobs:
        latest_blob = blob  # last blob in iteration = latest timestamp

    return latest_blob


def load_gold_record(record: dict):
    """Insert a single cleaned record into Azure PostgreSQL."""
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
        port=POSTGRES_PORT,
        sslmode="require"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_gold (
            city TEXT,
            timestamp TEXT,
            date DATE,
            hour INTEGER,
            day_of_week TEXT,
            month INTEGER,
            temperature FLOAT,
            wind_speed FLOAT,
            humidity FLOAT
        );
    """)

    # Convert timestamp → date, hour, day_of_week, month
    ts = datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00"))
    date = ts.date()
    hour = ts.hour
    day_of_week = ts.strftime("%A")
    month = ts.month

    cur.execute("""
        INSERT INTO weather_gold (
            city, timestamp, date, hour, day_of_week, month,
            temperature, wind_speed, humidity
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        record["city"],
        record["timestamp"],
        date,
        hour,
        day_of_week,
        month,
        record["temperature"],
        record["wind_speed"],
        record["humidity"]
    ))

    conn.commit()
    cur.close()
    conn.close()


def load_gold_for_all_cities():
    cities = ["oslo", "bergen", "trondheim",
              "stavanger", "tromso", "kristiansand"]

    for city in cities:
        blob = get_latest_silver_blob(city)

        if blob is None:
            print(f"No Silver data found for {city}")
            continue

        print(f"Loading Gold from Silver blob: {blob.name}")

        silver_data = silver_container.download_blob(blob.name).readall()
        record = json.loads(silver_data)

        load_gold_record(record)

    print("Loaded all Silver → Gold records into Azure PostgreSQL!")


if __name__ == "__main__":
    load_gold_for_all_cities()
