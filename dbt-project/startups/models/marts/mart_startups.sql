select
    s.funding_rounds,
    s.founder_experience_years,
    s.team_size,
    s.team_category,
    s.market_size_billion,
    s.product_traction_users,
    s.burn_rate_million,
    s.revenue_million,
    s.revenue_stage,
    s.investor_type,
    i.investor_type_name,
    s.sector,
    s.founder_background,
    s.outcome,
    case
        when s.outcome in ('IPO', 'Acquisition') then true
        else false
    end as is_successful
from {{ ref('int_startups_enriched') }} s
left join {{ ref('investor_types') }} i
    on s.investor_type = i.investor_type