# Pytest unit tests for the API call Lambda function.
# Pytest global fixtures located in conftest.py.

import json


def test_lambda_handler_s3_upload(create_raw_s3_bucket):
    # Import functions
    from src.api_lambda.main import fetch_nba_data, upload_data_to_s3, lambda_handler
    
    # Fetch NBA data
    data = fetch_nba_data()

    # Upload data to mocked S3
    s3_raw, bucket_name, today = create_raw_s3_bucket
    upload_data_to_s3(data)
    
    # Run the Lambda handler with empty event and context (required arguments)
    response = lambda_handler({}, {})
    assert response["statusCode"] == 200

    # Verify that the data was uploaded to the bucket
    objects = s3_raw.list_objects_v2(Bucket=bucket_name)
    # assert False, objects # Uncomment to inspect objects
    assert objects["KeyCount"] == 1
    assert "Contents" in objects
    json_data = s3_raw.get_object(Bucket=bucket_name, Key=f"{today}/nba_player_data.json")["Body"].read().decode("utf-8")
    parsed_json = json.loads(json_data)
    assert "BirthCity" in parsed_json[0], parsed_json

