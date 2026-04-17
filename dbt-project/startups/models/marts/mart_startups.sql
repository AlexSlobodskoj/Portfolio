select
    funding_rounds,
    founder_experience_years,
    team_size,
    team_category,
    market_size_billion,
    product_traction_users,
    burn_rate_million,
    revenue_million,
    revenue_stage,
    investor_type,
    sector,
    founder_background,
    outcome,
    case
        when outcome = 'IPO' or outcome = 'Acquisition' then true
        else false
    end as is_successful
from {{ ref('int_startups_enriched') }}