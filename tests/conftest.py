from moto import mock_aws # https://docs.getmoto.org/en/latest/docs/getting_started.html
from moto.core import DEFAULT_ACCOUNT_ID
import boto3
import pytest
import os

os.environ["DEVOPS_PREFIX"] = "test-prefix"
os.environ["RAWDATA_BUCKET_NAME"] = "test-rawdata-bucket"
os.environ["TRANSFORMED_BUCKET_NAME"] = "test-transformed-bucket"

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope="function")
def mocked_aws(aws_credentials):
    """
    Mock all AWS interactions
    Requires you to create your own boto3 clients
    """
    with mock_aws():
        yield

@pytest.fixture
def create_raw_s3_bucket(mocked_aws):
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket_name = os.getenv("DEVOPS_PREFIX") + os.getenv("RAWDATA_BUCKET_NAME")
    s3.create_bucket(Bucket=bucket_name)
    yield s3, bucket_name


@pytest.fixture
def create_transform_s3_bucket(mocked_aws):
    s3 = boto3.client("s3", region_name="us-east-1")
    bucket_name = os.getenv("DEVOPS_PREFIX") + os.getenv("TRANSFORMED_BUCKET_NAME")
    s3.create_bucket(Bucket=bucket_name)
    yield s3, bucket_name