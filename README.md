# Cloud Data Ingestion & Anonymization Pipeline

An end-to-end Python pipeline demonstrating automated data sanitization and streaming ingestion into AWS S3 using `boto3`.

## Architecture & Features
* **Data Transformation:** Strips PII and creates anonymized hash identifiers using `pandas` and `hashlib`.
* **Cloud Integration:** Programmatically streams transformed data into AWS S3 buckets without writing temporary files to local disk.
* **Testing & Verification:** Includes unit tests using `pytest` and `moto` to mock AWS S3 services locally for offline execution.

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run unit tests offline: `pytest`
3. Execute pipeline: `python pipeline.py`
