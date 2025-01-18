# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import json
import urllib.parse
import boto3
from datetime import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv()

transform_bucket_name = os.getenv("DEVOPS_PREFIX") + os.getenv("TRANSFORMED_BUCKET")

# S3 trigger for Lambda functions | https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html

print('Loading function')

today = dt.today().strftime("%Y-%m-%d")


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    s3 = boto3.client('s3')
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        
        # Convert data to line-delimited JSON format
        print("Converting data to line-delimited JSON format...")
        file_content = data['Body'].read().decode('utf-8')
        json_data = json.loads(file_content)
        line_delimited_data = "\n".join([json.dumps(record) for record in json_data])
        print(line_delimited_data)

        # Define S3 object key
        file_key = f"{today}/nba_player_data.jsonl"

        # Upload JSON data to S3
        s3.put_object(
            Bucket=transform_bucket_name,
            Key=file_key,
            Body=line_delimited_data
        )
        return {"statusCode": 200, "body": f"Uploaded data to S3: {file_key} in line-delimited JSON format."}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": 'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket)}
        # raise e
              
