with posts as (
    select * from {{ ref('stg_reddit_posts') }}
),

daily_stats as (
    select
        -- Округляем время до дня
        date_trunc('day', created_utc) as activity_date,
        subreddit,
        stock_ticker,
        -- Считаем количество постов за этот день
        count(post_id) as posts_count,
        -- Считаем суммарный охват (score)
        sum(score) as total_posts_score,
        -- Считаем средний рейтинг поста в этот день
        avg(score) as avg_post_score,
        -- Вытаскиваем самого активного автора дня в сабреддите (опционально)
        max(author) as random_active_author 
    from posts
    group by 1, 2, 3
)

select * from daily_stats