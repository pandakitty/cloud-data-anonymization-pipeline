import os
import io
import hashlib
import pandas as pd
import boto3
from dotenv import load_dotenv

# Load local environment variables safely
load_dotenv()

def anonymize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Removes PII and hashes identifier columns."""
    df_clean = df.copy()
    if "name" in df_clean.columns:
        df_clean = df_clean.drop(columns=["name"])
    if "patient_id" in df_clean.columns:
        df_clean["patient_hash"] = df_clean["patient_id"].apply(
            lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:12]
        )
        df_clean = df_clean.drop(columns=["patient_id"])
    return df_clean

def upload_to_s3(df: pd.DataFrame, bucket_name: str, file_key: str, s3_client=None) -> bool:
    """Streams a DataFrame directly into an AWS S3 bucket as CSV."""
    if s3_client is None:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "mock_key"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "mock_secret"),
            region_name=os.getenv("AWS_REGION", "us-west-2")
        )

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    
    s3_client.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=csv_buffer.getvalue()
    )
    return True

if __name__ == "__main__":
    # Sample incoming dataset
    raw_data = {
        "patient_id": [101, 102, 103],
        "name": ["Alice Smith", "Bob Jones", "Charlie Brown"],
        "metric_value": [120.5, 98.2, 115.0],
        "status": ["Normal", "Elevated", "Normal"]
    }
    
    raw_df = pd.DataFrame(raw_data)
    processed_df = anonymize_data(raw_df)
    
    target_bucket = os.getenv("S3_BUCKET_NAME", "my-demo-bucket")
    upload_to_s3(processed_df, target_bucket, "processed/metrics.csv")
    print("Pipeline executed successfully.")
