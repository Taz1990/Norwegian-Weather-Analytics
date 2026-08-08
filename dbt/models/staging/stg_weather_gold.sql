{{ config(materialized='view') }}

select
    city,
    timestamp,
    date,
    hour,
    day_of_week,
    month,
    temperature,
    wind_speed,
    humidity
from {{ source('weather', 'weather_gold') }}
