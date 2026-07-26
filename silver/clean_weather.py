import os
import json
import logging

# ---------------------------------------------------------
# Base directory of THIS script (silver folder)
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------
# Correct absolute paths (always inside project root)
# ---------------------------------------------------------
BRONZE_DIR = os.path.join(BASE_DIR, "..", "bronze", "raw_weather")
SILVER_OUTPUT_DIR = os.path.join(BASE_DIR, "clean_weather")
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")

# ---------------------------------------------------------
# Logging setup (silver.log)
# ---------------------------------------------------------
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "silver.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------------------------------------
# Function: Clean one city's raw JSON files
# ---------------------------------------------------------


def clean_city(city_name):
    city_folder = os.path.join(BRONZE_DIR, city_name)
    cleaned_rows = []

    # Loop through all raw JSON files for this city
    for file in os.listdir(city_folder):
        if file.endswith(".json"):
            file_path = os.path.join(city_folder, file)

            with open(file_path, "r") as f:
                raw_data = json.load(f)

            # Flatten each timeseries entry
            for entry in raw_data["properties"]["timeseries"]:
                details = entry["data"]["instant"]["details"]

                cleaned_rows.append({
                    "timestamp": entry["time"],
                    "temperature": details.get("air_temperature"),
                    "wind_speed": details.get("wind_speed"),
                    "humidity": details.get("relative_humidity")
                })

    logging.info(f"Cleaned {city_name}: {len(cleaned_rows)} rows")
    return cleaned_rows

# ---------------------------------------------------------
# Main: Loop through all cities and save clean JSON
# ---------------------------------------------------------


def main():
    os.makedirs(SILVER_OUTPUT_DIR, exist_ok=True)

    # Loop through each city folder inside bronze/raw_weather
    for city_name in os.listdir(BRONZE_DIR):
        city_path = os.path.join(BRONZE_DIR, city_name)

        if os.path.isdir(city_path):
            cleaned_data = clean_city(city_name)

            output_file = os.path.join(SILVER_OUTPUT_DIR, f"{city_name}.json")
            with open(output_file, "w") as f:
                json.dump(cleaned_data, f, indent=2)

            logging.info(f"Saved Silver JSON for {city_name} → {output_file}")

    logging.info("Silver layer completed successfully.")


# ---------------------------------------------------------
# Run script
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
