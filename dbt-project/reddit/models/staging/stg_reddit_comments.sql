select
    comment_id,
    post_id,
    subreddit,
    stock_ticker,
    body,
    author,
    created_utc,
    score,
    permalink
from {{ source('raw_data', 'reddit_comments') }}