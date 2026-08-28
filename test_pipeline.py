import boto3
import pandas as pd
from moto import mock_aws
from pipeline import anonymize_data, upload_to_s3

def test_anonymize_data():
    raw_data = {"patient_id": [1], "name": ["Jane Doe"], "val": [10]}
    df = pd.DataFrame(raw_data)
    cleaned = anonymize_data(df)
    
    assert "name" not in cleaned.columns
    assert "patient_id" not in cleaned.columns
    assert "patient_hash" in cleaned.columns

@mock_aws
def test_upload_to_s3():
    bucket_name = "test-bucket"
    s3 = boto3.client("s3", region_name="us-west-2")
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
    )

    df = pd.DataFrame({"colA": [1, 2], "colB": [3, 4]})
    result = upload_to_s3(df, bucket_name, "test.csv", s3_client=s3)
    
    assert result is True
    response = s3.get_object(Bucket=bucket_name, Key="test.csv")
    content = response["Body"].read().decode("utf-8")
    assert "colA,colB" in content
