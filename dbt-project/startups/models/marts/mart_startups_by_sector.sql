select
    sector,
    count(*) as total_startups,
    {{ count_by_outcome('IPO') }} as cnt_ipo,
    {{ count_by_outcome('Acquisition') }} as cnt_acquisition,
    {{ count_by_outcome('Failure') }} as cnt_failed
from {{ ref('stg_startups') }}
group by sector