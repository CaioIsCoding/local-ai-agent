import boto3
from botocore.exceptions import ClientError
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_ENDPOINT_URL
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file_path: str, object_name: str = None) -> str:
        """
        Uploads a file to an S3 bucket and returns the public URL or object name.
        """
        if object_name is None:
            object_name = file_path.split('/')[-1]

        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            
            # Construct the URL
            if settings.AWS_ENDPOINT_URL:
                url = f"{settings.AWS_ENDPOINT_URL}/{self.bucket_name}/{object_name}"
            else:
                url = f"https://{self.bucket_name}.s3.amazonaws.com/{object_name}"
            
            logger.info(f"File {file_path} uploaded to {url}")
            return url
        except ClientError as e:
            logger.error(f"Error uploading to S3: {e}")
            raise e

    def upload_binary(self, binary_data: bytes, object_name: str) -> str:
        """
        Uploads binary data to an S3 bucket and returns the URL.
        """
        try:
            self.s3_client.put_object(Body=binary_data, Bucket=self.bucket_name, Key=object_name)
            
            if settings.AWS_ENDPOINT_URL:
                url = f"{settings.AWS_ENDPOINT_URL}/{self.bucket_name}/{object_name}"
            else:
                url = f"https://{self.bucket_name}.s3.amazonaws.com/{object_name}"
                
            return url
        except ClientError as e:
            logger.error(f"Error uploading binary to S3: {e}")
            raise e

storage_service = StorageService()
