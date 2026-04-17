select
    post_id,
    subreddit,
    stock_ticker,
    title,
    body,
    author,
    created_utc,
    score,
    upvote_ratio,
    num_comments,
    url,
    permalink
from {{ source('raw_data', 'reddit_posts') }}