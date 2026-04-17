# Reddit Sentiment & Activity Analysis (dbt Project)

## Overview
This project processes raw data from Reddit to track subreddit activity and stock-related discussions. It features a robust data quality framework to detect discrepancies between external API metrics and internal row counts.

## Key Features
- **Data Integration**: Unifies posts and comments into a consolidated fact table.
- **Advanced Data Quality**: 
    - **Drift Detection**: Custom test using `dbt_utils` to monitor the difference between API-reported `num_comments` and actual database records.
    - **Temporal Integrity**: Automated checks ensuring all activity dates are within valid ranges (no future dates).
- **Time-Series Marts**: Daily aggregation layer designed for high-performance Tableau dashboards.

## Analytical Layers
- **Staging**: Normalizes raw Reddit JSON-like structures into clean relational views.
- **Marts (`fct_reddit_posts`)**: Joins posts with calculated comment metrics.
- **Marts (`fct_reddit_daily_activity`)**: Aggregates metrics (scores, post counts) by day and subreddit.

## Tech Stack
- **dbt Core** (Jinja/SQL)
- **PostgreSQL**
- **dbt_utils** (Data validation macros)