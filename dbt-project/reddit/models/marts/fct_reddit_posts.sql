with posts as (
    -- Берем подготовленные данные постов из staging
    select * from {{ ref('stg_reddit_posts') }}
),

comment_counts as (
    -- Агрегируем комментарии: считаем количество для каждого поста
    select
        post_id,
        count(comment_id) as total_comments
    from {{ ref('stg_reddit_comments') }}
    group by post_id
),

final as (
    -- Объединяем посты с количеством комментариев
    select
        p.*,
        -- Если комментариев нет, ставим 0 вместо NULL
        coalesce(c.total_comments, 0) as total_comments
    from posts p
    left join comment_counts c
        on p.post_id = c.post_id
)

select * from final

