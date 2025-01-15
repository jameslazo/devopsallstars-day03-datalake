from moto import mock_aws # https://docs.getmoto.org/en/latest/docs/getting_started.html
from moto.core import DEFAULT_ACCOUNT_ID
from moto.sns import sns_backends # https://docs.getmoto.org/en/latest/docs/services/sns.html
import boto3
import pytest
import os
# from dotenv import load_dotenv

os.environ["DEVOPS_PREFIX"] = "test-prefix"
os.environ["RAWDATA_BUCKET_NAME"] = "test-rawdata-bucket"

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

"""
@pytest.fixture(scope="function")
def set_bucket_env_vars():
    # Set the required environment variables before testing
"""


@pytest.fixture(scope="function")
def mocked_aws(aws_credentials):
    """
    Mock all AWS interactions
    Requires you to create your own boto3 clients
    """
    with mock_aws():
        yield

@pytest.fixture
def create_s3_bucket(mocked_aws):
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket_name = os.getenv("DEVOPS_PREFIX") + os.getenv("RAWDATA_BUCKET_NAME")
    s3.create_bucket(Bucket=bucket_name)
    yield bucket_name

def test_lambda_handler(create_s3_bucket):
    """Test Lambda."""
    from src.main import lambda_handler
    # Run the Lambda handler with empty event and context (required arguments)
    response = lambda_handler({}, {})
    assert response["statusCode"] == 200


