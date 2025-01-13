# day03-datalake
Day 3 of the #DevOpsAllStarsChallenge presented by [Alicia Ahl](https://www.youtube.com/watch?v=RAkMac2QgjM) with reference [this repository](https://github.com/alahl1/NBADataLake)
## Requirements
API Call
- Fetch data with API key

ETL
- Extract data from API call in JSON format
- Transform data to line-delimited JSON
- Load data to S3 bucket
  - `Depends on` S3 bucket

Provision resources:
- S3 bucket
- Glue table
- Configure Athena output location