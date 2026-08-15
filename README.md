# Norwegian-Weather-Analytics  
End-to-End ELT Data Engineering Project - Local Development with Docker & PostgreSQL → Azure → Microsoft Fabric → dbt → Power BI

## Overview:  
An end-to-end ELT data engineering pipeline that collects weather data from the MET Norway API, processes it through a Bronze → Silver → Gold architecture and delivers analytics through Power BI.  
The project was developed locally first using Docker and PostgreSQL, then extended to a cloud environment using Azure Blob, Microsoft Fabric, dbt and Azure PostgreSQL.

## Goal:   
The aim of this project is to demonstrate my core data engineering skills using a realistic data source and a production-style workflow: extraction, loading, transformation, orchestration, warehousing and visualization. 
<img width="942" height="452" alt="docker for weth analytics" src="https://github.com/user-attachments/assets/48783670-9b58-442f-b21f-587583d064bb" />  
<img width="544" height="249" alt="azure step-3" src="https://github.com/user-attachments/assets/bc3f3865-13cb-4cbc-a383-800b725993af" />  
<img width="956" height="446" alt="azure blob" src="https://github.com/user-attachments/assets/0f661298-d34c-4568-bf62-ded4c5e5263b" />  
<img width="956" height="470" alt="Fabric pipe 1" src="https://github.com/user-attachments/assets/bfb0a42f-4a86-4af1-a0ad-fb6050f6e68b" />  
<img width="381" height="205" alt="weather dsh power bi" src="https://github.com/user-attachments/assets/043ddb0c-9e46-4f1c-b249-967edcaf2756" />  

## Key Features:    
- Real-time Weather Data Ingestion - Extracts weather data from the MET Norway API using Python.
- Medallion Data Architecture - Implements a BRONZE → SILVER → GOLD architecture for structured data processing.
- Local-to-Cloud Pipeline - Developed and validated locally with Docker/PostgreSQL before migrating the pipeline to Azure      and Microsoft Fabric.
- Cloud Data Engineering - Uses Azure Blob Storage, Microsoft Fabric Lakehouse and Azure PostgreSQL for cloud-based storage    and orchestration.
- dbt Data Modeling & Testing - Builds analytical models using dbt with documentation, lineage and data quality tests.
- Automated Orchestration - Uses Microsoft Fabric Pipelines to automate the end-to-end data workflow.
- Interactive Analytics - Delivers weather trends, city comparisons and key metrics through Power BI dashboards.  

## ELT Architecture:  

                               MET Norway API
                                      │
                                      ▼
                              Python Ingestion     
                                      │
                                      ▼
                    ┌─────────────────────────────────┐
                    │       LOCAL DEVELOPMENT         │
                    │     Docker + PostgreSQL         │
                    │    BRONZE → SILVER → GOLD       │
                    └────────────────┬────────────────┘
                                     │
                                     ▼
                    ┌─────────────────────────────────┐
                    │       Azure Blob Storage        │
                    │       BRONZE & SILVER Data      │        
                    └────────────────┬────────────────┘
                                     │
                                     ▼
                    ┌─────────────────────────────────┐
                    │       Azure PostgreSQL DB       │
                    │            Gold Data            │        
                    └────────────────┬────────────────┘
                                     │
                                     ▼
              ┌─────────────────────────────────────────────┐
              │          MICROSOFT FABRIC LAKEHOUSE         │
              │              Fabric Pipeline                │
              │              (Orchestration)                │
              └──────────────────────┬──────────────────────┘
                                     │
                                     ▼
                           ┌─────────────────────┐
                           │         dbt         │
                           │ Staging Models      │
                           │ Dimension Models    │
                           │ Fact Models         │
                           │ Data Quality Tests  │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │ Azure PostgreSQL    │
                           │ Analytics Warehouse │
                           │ dim_city            │
                           │ dim_date            │
                           │ fact_weather        │
                           │ stg_weather_gold    │
                           └──────────┬──────────┘
                                      │ 
                                      ▼
                           ┌─────────────────────┐
                           │      Power BI       │
                           │ Temperature Trends  │
                           │ Humidity Analysis   │
                           │ Wind Analysis       │
                           │ City Comparison     │
                           └─────────────────────┘  

## Architecture Overview:    

**Local Development Phase:**   
- Docker container used to run PostgreSQL locally  
- Python scripts created for:  
  - Data ingestion  
  - BRONZE cleaning    
  - SILVER normalization
  - GOLD aggregation  
- BRONZE/SILVER/GOLD schemas designed and validated  
- dbt project created locally:    
  - dbt_project.yml  
  - profiles.yml  
  - staging + dimension + fact models  
  - dbt documentation + lineage graph generated locally   

**Cloud Migration Phase:**  
- RAW + SILVER data uploaded to Azure Blob Storage  
- GOLD data stored in Azure PostgreSQL Flexible Server  
- Fabric Lakehouse used for RAW/BRONZE/SILVER/GOLD layers  
- Fabric Pipelines used for full ELT orchestration  
- dbt models executed in cloud environment  
- Power BI connected to Azure PostgreSQL for analytics  

## ELT Pipeline (Local → Cloud):  
**1. BRONZE Layer**  
- API ingestion  
- Stored locally inside Docker based PostgreSQL DB  
- Basic cleaning   
- JSON flattening  
- Uploaded to Azure blob  

**2. SILVER Layer**  
- Normalized schema  
- Timestamp conversion  
- Missing value handling  
- Stored in Azure Blob  

**3. GOLD Layer**  
- Daily aggregations  
- Trend calculations  
- Stored in Azure PostgreSQL (final warehouse) 

## dbt Modeling:    
dbt was first developed locally, then migrated to Azure.    

**Models Created:**  
- stg_weather_gold  
- dim_city  
- dim_date  
- fact_weather  

**dbt Features Used:**
- dbt documentation site  
- dbt lineage graph  
- dbt tests (unique, not null)  
- dbt sources + schema.yml  

## Fabric Orchestration:

- Copy Bronze and Silver data from Azure Blob  
- Transform Silver → Gold and load Gold data into Azure PostgreSQL  
- Execute dbt models for dimensional modeling  
- Store final tables in Azure PostgreSQL  
- End‑to‑end scheduling and automation   

This creates a production‑style cloud pipeline.  

                 Microsoft Fabric Pipeline
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
           BRONZE       SILVER          GOLD
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    Azure PostgreSQL
                           │
                           ▼
                         dbt
                           │
                           ▼
                       Power BI

## Technology Stack:

- **Data Source**      - MET Norway API  
- **Programming**      - Python  
- **Query Language**   -	SQL  
- **Containerization** -	Docker  
- **Local Database**   -	PostgreSQL   
- **Lakehouse**        - Microsoft Fabric  
- **Orchestration**	   - Microsoft Fabric Pipelines  
- **Cloud Storage**    - Azure Blob Storage   
- **Data Warehouse**   - Azure PostgreSQL
- **Cloud Platform**   -	Microsoft Azure   
- **Transformation**   -	dbt  
- **Visualization**	   - Power BI

## Skills Demonstrated:

This project demonstrates my practical experience with:
- End-to-end ELT pipeline development  
- REST API data ingestion  
- Python data processing  
- SQL data transformation 
- Bronze → Silver → Gold architecture  
- Dimensional data modeling  
- dbt transformations and testing  
- Cloud data storage and warehousing  
- Microsoft Fabric orchestration  
- Azure cloud services  
- Docker-based development  
- Power BI analytics  

## Project Outcome:  

The final result is a complete weather analytics platform that demonstrates the full journey from raw API data to business-ready analytics. This project combines local development, cloud data engineering, transformation, orchestration, warehousing and visualization into a single end-to-end portfolio project.
 
## Author:  

Taz Ahmed  

MSc Computational Engineering (UiS) | Aspiring Data Engineer  

Core interests: Data Engineering • Cloud Data Platforms • ELT • Analytics • Machine Learning  


