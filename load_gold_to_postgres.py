import json
import psycopg2
import os

# Load environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER", "${POSTGRES_USER}")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "${POSTGRES_PASSWORD}")
POSTGRES_DB = os.getenv("POSTGRES_DB", "${POSTGRES_DB}")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Path to your Gold JSON file
GOLD_FILE = "gold/weather_gold.json"


def load_gold():
    # Connect to PostgreSQL running in Docker
    conn = psycopg2.connect(
        host="localhost",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
        port=POSTGRES_PORT
    )
    cur = conn.cursor()

    # Create table if not exists
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

    # Load JSON file
    with open(GOLD_FILE, "r") as f:
        records = json.load(f)

    # Insert records
    for r in records:
        cur.execute("""
            INSERT INTO weather_gold (
                city, timestamp, date, hour, day_of_week, month,
                temperature, wind_speed, humidity
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            r["city"],
            r["timestamp"],
            r["date"],
            r["hour"],
            r["day_of_week"],
            r["month"],
            r["temperature"],
            r["wind_speed"],
            r["humidity"]
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("Loaded Gold JSON into PostgreSQL successfully!")


if __name__ == "__main__":
    load_gold()
