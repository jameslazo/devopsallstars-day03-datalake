import boto3
import json
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Based on https://github.com/alahl1/NBADataLake repo by Alicia Ahl

# Set variables loaded from .env
api_key = os.getenv("SPORTS_DATA_API_KEY")
nba_endpoint = os.getenv("NBA_ENDPOINT")
prefix = os.getenv("DEVOPS_PREFIX")
rawdata_bucket_name = prefix + os.getenv("RAWDATA_BUCKET_NAME")

# Initialize s3 client
s3 = boto3.client("s3")

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

def upload_data_to_s3(data):
    """Upload NBA data to the S3 bucket."""
    try:
        # Define S3 object key
        file_key = "raw-data/nba_player_data.json"

        # Upload JSON data to S3
        s3.put_object(
            Bucket=rawdata_bucket_name,
            Key=file_key
        )
        print(f"Uploaded data to S3: {file_key}")
    except Exception as e:
        print(f"Error uploading data to S3: {e}")


def lambda_handler(event, context):
    print("Setting up data lake for NBA sports analytics...")
    nba_data = fetch_nba_data()
    if nba_data:  # Only proceed if data was fetched successfully
        upload_data_to_s3(nba_data)
    print("Data lake setup complete.")