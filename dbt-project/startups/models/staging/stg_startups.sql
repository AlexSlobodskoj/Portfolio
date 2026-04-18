select
    funding_rounds,
    founder_experience_years,
    team_size,
    market_size_billion,
    product_traction_users,
    burn_rate_million,
    revenue_million,
    case 
        when lower(investor_type) = 'vc' THEN 'tier1_vc' 
        else lower(investor_type) 
    END AS investor_type,
    case
        when lower(sector) = 'fintech' then 'Fintech'
        when lower(sector) = 'healthtech' then 'Health'
        else sector
    end as sector,
    founder_background,
    outcome,
    created_at
from {{ source('public', 'startup_succes') }}