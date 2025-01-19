# Pytest unit tests for the extract Lambda function.
# Pytest global fixtures located in conftest.py.

def test_lambda_extract_and_upload(create_raw_s3_bucket, create_extract_s3_bucket, s3_event):
    s3_raw, bucket_name_raw, today1 = create_raw_s3_bucket
    s3_extract, bucket_name_extract, today = create_extract_s3_bucket
    objects = s3_raw.list_objects_v2(Bucket=bucket_name_raw)
    # assert False, objects # Uncomment to inspect objects
    
    from src.extract_lambda.main import lambda_handler

    # Run the Lambda handler with empty event and context (required arguments)
    response = lambda_handler(s3_event, {})
    assert response["statusCode"] == 200
    # assert False, s3_extract.list_objects_v2(Bucket=bucket_name_extract) # Uncomment to inspect objects

    data = s3_extract.get_object(Bucket=bucket_name_extract, Key=f"{today}/nba_player_data.jsonl")
    json_data = data["Body"].read().decode("utf-8")
    assert "PlayerID" in json_data



