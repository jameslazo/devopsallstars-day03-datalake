from moto import mock_aws # https://docs.getmoto.org/en/latest/docs/getting_started.html
from moto.core import DEFAULT_ACCOUNT_ID
from moto.sns import sns_backends # https://docs.getmoto.org/en/latest/docs/services/sns.html
import boto3
import pytest
from src.main import lambda_handler
import os
from dotenv import load_dotenv

load_dotenv()

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