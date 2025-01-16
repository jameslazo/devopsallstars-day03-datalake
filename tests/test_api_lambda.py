# Pytest unit tests for the API call Lambda function.
# Pytest global fixtures located in conftest.py.

def test_lambda_handler_s3_upload(create_raw_s3_bucket):
    s3, bucket_name = create_raw_s3_bucket
    
    # Test Lambda.
    from src.api_lambda.main import lambda_handler
    # Run the Lambda handler with empty event and context (required arguments)
    response = lambda_handler({}, {})
    assert response["statusCode"] == 200

    # Verify that the data was uploaded to the bucket
    objects = s3.list_objects_v2(Bucket=bucket_name)
    assert objects["KeyCount"] == 1
    assert "Contents" in objects

