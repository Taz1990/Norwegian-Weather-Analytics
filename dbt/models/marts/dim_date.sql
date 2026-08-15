{{ config(materialized='table') }}

select distinct
    date,
    extract(year from date)      as year,
    extract(month from date)     as month,
    extract(day from date)       as day,
    to_char(date, 'Day')         as day_name,
    extract(dow from date)       as day_of_week
from {{ ref('stg_weather_gold') }}
