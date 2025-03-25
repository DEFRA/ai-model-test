from logging import getLogger
from typing import Optional

import boto3

from app.config import config

logger = getLogger(__name__)

class S3Client:
    _instance = None

    def __new__(cls, bucket_name: Optional[str] = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.bucket_name = bucket_name or config.S3_BUCKET
            cls._instance.s3 = boto3.client(
                "s3",
                endpoint_url=config.S3_ENDPOINT
            )
        return cls._instance

    def check_connection(self):
        """Checks if the connection to the S3 bucket is working."""
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Connected to S3 bucket: {self.bucket_name}")
            return True
        except Exception as e:
            logger.info(f"Failed to connect to S3 bucket: {e}")
        return False

    def upload_file(self, file_name, object_name=None):
        """Uploads a file to the S3 bucket."""
        if object_name is None:
            object_name = file_name
        try:
            self.s3.upload_file(file_name, self.bucket_name, object_name)
            logger.info(f"File {file_name} uploaded as {object_name}")
        except Exception as e:
            logger.info(f"Upload failed: {e}")

    def download_file(self, object_name, file_name):
        """Downloads a file from the S3 bucket."""
        try:
            self.s3.download_file(self.bucket_name, object_name, file_name)
            logger.info(f"File {object_name} downloaded as {file_name}")
        except Exception as e:
            logger.info(f"Download failed: {e}")

    def close_connection(self):
        """Closes the S3 client connection."""
        self.s3 = None
        S3Client._instance = None
        print("S3 client connection closed.")
