import boto3
import json
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Based on https://github.com/alahl1/NBADataLake

def fetch_nba_data():
    """Fetch NBA player data from sportsdata.io."""
    try:
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        response = requests.get(nba_endpoint, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        print("Fetched NBA data successfully.")
        return response.json()  # Return JSON response
    except Exception as e:
        print(f"Error fetching NBA data: {e}")
        return []


def convert_to_line_delimited_json(data):
    """Convert data to line-delimited JSON format."""
    print("Converting data to line-delimited JSON format...")
    return "\n".join([json.dumps(record) for record in data])


def upload_data_to_s3(data):
    """Upload NBA data to the S3 bucket."""
    try:
        # Convert data to line-delimited JSON
        line_delimited_data = convert_to_line_delimited_json(data)

        # Define S3 object key
        file_key = "raw-data/nba_player_data.jsonl"

        # Upload JSON data to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=line_delimited_data
        )
        print(f"Uploaded data to S3: {file_key}")
    except Exception as e:
        print(f"Error uploading data to S3: {e}")


def main():
    print("Setting up data lake for NBA sports analytics...")
    create_s3_bucket()
    time.sleep(5)  # Ensure bucket creation propagates
    create_glue_database()
    nba_data = fetch_nba_data()
    if nba_data:  # Only proceed if data was fetched successfully
        upload_data_to_s3(nba_data)
    create_glue_table()
    configure_athena()
    print("Data lake setup complete.")

if __name__ == "__main__":
    main()