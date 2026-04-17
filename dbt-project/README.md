# Data Transformation Portfolio (dbt Projects)

Welcome to my dbt (data build tool) portfolio. This repository contains end-to-end data transformation pipelines that turn raw data into clean, business-ready analytics layers using modern data engineering practices.

## Projects in this Repository

### 1. [Reddit Activity Monitor](./reddit)
**Objective**: Build a scalable model for social media monitoring and data audit.
- **Highlight**: Implemented automated data drift testing to compare API metadata with actual database counts.
- **Key Outcome**: Business-ready fact tables for time-series analysis in Tableau.

### 2. [Startup Success Analysis](./startups)
**Objective**: Analyze market outcomes for startups based on team size and revenue stages.
- **Highlight**: Developed an intermediate transformation layer for custom business logic and startup segmentation.
- **Key Outcome**: Categorization of success rates (IPO vs Acquisition) across different industries.

## Data Engineering Principles Applied
- **Medallion Architecture**: Clear separation between Staging and Marts layers.
- **Defensive Modeling**: Integration of generic and custom dbt tests to ensure 100% data integrity.
- **Documentation**: All models are fully documented and visible via `dbt docs`.
- **Modularity**: Extensive use of Common Table Expressions (CTEs) and `ref()` functions for maintainable SQL.