{{ config(materialized='table') }}

select distinct
    city
from {{ ref('stg_weather_gold') }}
