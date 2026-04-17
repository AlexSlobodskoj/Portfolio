with source as (
    select * from {{ ref('stg_startups') }}
)

select
    *,
    case
        when team_size < 5 then 'Small'
        when team_size < 20 then 'Medium'
        else 'Large'
    end as team_category,
    case
        when revenue_million = 0 then 'Pre-revenue'
        when revenue_million < 1 then 'Early revenue'
        when revenue_million < 10 then 'Growing'
        else 'Mature'
    end as revenue_stage
from source