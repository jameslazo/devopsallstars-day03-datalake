from moto import mock_aws # https://docs.getmoto.org/en/latest/docs/getting_started.html
from moto.core import DEFAULT_ACCOUNT_ID
import boto3
import pytest
from dotenv import load_dotenv
import os
from datetime import datetime as dt

today = dt.today().strftime("%Y-%m-%d")

dotenv_path=os.path.join(os.path.dirname(__file__), "../src", ".env")
if not load_dotenv(dotenv_path):
    raise FileNotFoundError(f"Could not find .env file at {dotenv_path}")


@pytest.fixture(scope="session")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="session")
def mocked_aws(aws_credentials):
    """
    Mock all AWS interactions
    Requires you to create your own boto3 clients
    """
    with mock_aws():
        yield


@pytest.fixture(scope="session")
def create_raw_s3_bucket(mocked_aws):
    bucket_name_raw = os.getenv("DEVOPS_PREFIX") + os.getenv("RAW_BUCKET")
    s3_raw = boto3.client("s3", region_name="us-east-1")
    s3_raw.create_bucket(Bucket=bucket_name_raw)
    yield s3_raw, bucket_name_raw


@pytest.fixture(scope="session")
def create_transform_s3_bucket(mocked_aws):
    s3_transform = boto3.client("s3", region_name="us-east-1")
    bucket_name_transform = os.getenv("DEVOPS_PREFIX") + os.getenv("TRANSFORMED_BUCKET")
    s3_transform.create_bucket(Bucket=bucket_name_transform)
    yield s3_transform, bucket_name_transform


@pytest.fixture
def s3_event():
    bucket_name_raw = os.getenv("DEVOPS_PREFIX") + os.getenv("RAW_BUCKET")
    # Mock S3 event trigger | https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-content-structure.html
    return {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": bucket_name_raw},
                    "object": {"key": f"{today}/nba_player_data.json"}
                }
            }
        ]
    }