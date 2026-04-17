select
    funding_rounds,
    founder_experience_years,
    team_size,
    market_size_billion,
    product_traction_users,
    burn_rate_million,
    revenue_million,
    investor_type,
    sector,
    founder_background,
    outcome,
    created_at
from {{ source('public', 'startup_succes') }}