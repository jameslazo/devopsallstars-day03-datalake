# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import json
import urllib.parse
import boto3
import os
from datetime import datetime as dt

transform_bucket_name = os.getenv("DEVOPS_PREFIX") + os.getenv("TRANSFORM_BUCKET_NAME")

# S3 trigger for Lambda functions | https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html

print('Loading function')

s3 = boto3.client('s3')

today = dt.today().strftime("%Y-%m-%d")


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        
        # Convert data to line-delimited JSON format
        print("Converting data to line-delimited JSON format...")
        line_delimited_data = "\n".join([json.dumps(record) for record in data])

        # Define S3 object key
        file_key = f"{today}/nba_player_data.jsonl"

        # Upload JSON data to S3
        s3.put_object(
            Bucket=transform_bucket_name,
            Key=file_key,
            Body=line_delimited_data
        )
        print(f"Uploaded data to S3: {file_key}")
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
              