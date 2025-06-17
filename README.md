# 🎬 CineVault: End-to-End Movie Metadata Pipeline (1920–Present)

## 📖 Project Overview
CineVault is a comprehensive data engineering pipeline designed to extract, transform, and analyze movie metadata from Wikipedia for all Hindi films released from 1920 to the present day. The pipeline automates data collection, enrichment, and analytics using modern cloud and orchestration tools.

---

## 🔧 Tech Stack

| Area              | Technology Used                                                                 |
|-------------------|----------------------------------------------------------------------------------|
| Web Scraping      | Wikipedia API, BeautifulSoup (Python)                                           |
| Workflow Orchestration | Apache Airflow, Celery Workers                                                |
| Containers        | Docker, Docker Compose                                                           |
| Staging Database  | PostgreSQL (temporary data storage)                                              |
| Cloud Storage & DW| Snowflake (Staging & Final Schemas)                                              |
| ETL Processing    | Pentaho Data Integration (PDI)                                                   |
| Analytics         | Power BI, Snowflake Worksheets (SQL-based dashboards)                            |
| Scripting         | Python (Data cleaning, validation, uploading)                                    |

---

## 🛠️ Pipeline Architecture
![diagram-export-12-06-2025-00_50_36](https://github.com/user-attachments/assets/4577cec3-cea0-4ebd-9661-63787cf28578)
1. **Extraction Phase**
   - Scrapes metadata (title, cast, runtime, genre, director, release date) from Wikipedia.
   - Uses Wikipedia API and BeautifulSoup for web parsing.
   - Data is temporarily stored in **PostgreSQL**.

2. **Orchestration & Task Management**
   - Managed using **Apache Airflow** with **Celery** backend for scalable task distribution.
   - Runs inside Docker containers for environment consistency.

3. **Transformation & Load**
   - Data is formatted and validated via Python and uploaded to:
     - **Snowflake Stage** (raw format)
     - **Snowflake Temp Table** (initial cleaned layer)

4. **ETL & Final Schema**
   - **Pentaho ETL** processes clean and enrich data.
   - Final structured data is loaded into a separate Snowflake schema for analytics.

5. **Analytics Layer**
   - Dashboards built using **Power BI** and **Snowflake Worksheets**
   - Visual insights into trends like genre evolution, director impact, film length trends, etc.

---

## 📊 Sample Analytics Use Cases

- Genre trends over decades
- Film length evolution across generations
- Most frequent cast/director collaborations
- Distribution of films by genre and director
