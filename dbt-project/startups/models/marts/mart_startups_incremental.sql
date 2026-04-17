{{ config(
    materialized='incremental',
    unique_key='row_number'
) }}

{% if is_incremental() %}

with source as (
    select
        *,
        row_number() over () as row_number
    from {{ ref('stg_startups') }}
    where created_at > (select max(created_at) from {{ this }})
)

{% else %}

with source as (
    select
        *,
        row_number() over () as row_number
    from {{ ref('stg_startups') }}
)

{% endif %}

select * from source