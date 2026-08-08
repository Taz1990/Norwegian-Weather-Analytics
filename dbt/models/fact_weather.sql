{{ config(materialized='table') }}

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
from {{ ref('stg_weather_gold') }}
