select sector, 'IPO' as outcome, {{ count_by_outcome('IPO') }} as count
from {{ ref('stg_startups') }}
group by sector

union all

select sector, 'Acquisition' as outcome, {{ count_by_outcome('Acquisition') }} as count
from {{ ref('stg_startups') }}
group by sector

union all

select sector, 'Failure' as outcome, {{ count_by_outcome('Failure') }} as count
from {{ ref('stg_startups') }}
group by sector