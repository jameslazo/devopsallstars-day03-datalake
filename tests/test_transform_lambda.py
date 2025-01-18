# Pytest unit tests for the Transform Lambda function.
# Pytest global fixtures located in conftest.py.

def test_lambda_transform_and_upload(create_raw_s3_bucket, create_transform_s3_bucket, s3_event):
    s3_raw, bucket_name_raw = create_raw_s3_bucket
    s3_transform, bucket_name_transform = create_transform_s3_bucket
    objects = s3_raw.list_objects_v2(Bucket=bucket_name_raw)
    # assert False, objects # Uncomment to inspect objects
    
    from src.transform_lambda.main import lambda_handler

    # Run the Lambda handler with empty event and context (required arguments)
    response = lambda_handler(s3_event, {})
    assert response["statusCode"] == 200
    # assert False, s3_transform.list_objects_v2(Bucket=bucket_name_transform) # Uncomment to inspect objects

    today = "2025-01-18"
    data = s3_transform.get_object(Bucket=bucket_name_transform, Key=f"{today}/nba_player_data.jsonl")
    json_data = data["Body"].read().decode("utf-8")
    assert "PlayerID" in json_data



