# Startup Success Analysis (dbt Project)

## Overview
This project transforms raw startup data into a multi-layered analytical model to identify success patterns across industries. It categorizes companies by scale and financial maturity to provide deeper insights into market outcomes.

## Analytical Layers
- **Staging (`stg_startups`)**: Standardizes raw data and ensures data types consistency.
- **Intermediate (`int_startups_categorized`)**: The core logic layer where startups are segmented:
    - **Team Size Categorization**: Small (<5), Medium (<20), or Large.
    - **Revenue Stages**: Classification from 'Pre-revenue' to 'Mature' (10M+).
- **Marts (`mart_startups`)**: Final business-ready table used for BI reporting and success rate analysis.

## Data Quality & Testing
- **Validation**: Strict `not_null` constraints on `sector` and `outcome`.
- **Integrity**: `accepted_values` test ensures startup outcomes strictly follow industry standards: `IPO`, `Acquisition`, or `Failure`.

## Key Business Metrics
- Success rate by Sector and Team Category.
- Distribution of successful exits (IPO/Acquisition) across Revenue Stages.