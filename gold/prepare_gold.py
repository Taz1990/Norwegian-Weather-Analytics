import os
import json
import logging
from datetime import datetime

# Base directory of THIS script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
SILVER_DIR = os.path.join(BASE_DIR, "..", "silver", "clean_weather")
GOLD_OUTPUT = os.path.join(BASE_DIR, "weather_gold.json")
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")

# Logging
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "gold.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def enrich_record(city, record):
    timestamp_obj = datetime.fromisoformat(
        record["timestamp"].replace("Z", "+00:00"))

    return {
        "city": city,
        "timestamp": record["timestamp"],
        "date": timestamp_obj.date().isoformat(),
        "hour": timestamp_obj.hour,
        "day_of_week": timestamp_obj.strftime("%A"),
        "month": timestamp_obj.month,
        "temperature": record["temperature"],
        "wind_speed": record["wind_speed"],
        "humidity": record["humidity"]
    }


def main():
    gold_rows = []

    for file in os.listdir(SILVER_DIR):
        if file.endswith(".json"):
            city = file.replace(".json", "")
            path = os.path.join(SILVER_DIR, file)

            with open(path, "r") as f:
                records = json.load(f)

            for r in records:
                gold_rows.append(enrich_record(city, r))

            logging.info(f"Processed {city}")

    with open(GOLD_OUTPUT, "w") as f:
        json.dump(gold_rows, f, indent=2)

    logging.info(f"Gold layer created → {GOLD_OUTPUT}")


if __name__ == "__main__":
    main()
