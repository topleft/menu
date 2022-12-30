from enum import Enum
import boto3
from botocore.errorfactory import ClientError
from pathlib import Path


class ContentType(Enum):
    PDF = "application/pdf"
    PNG = "image/png"
    JPG = "image/jpg"
    JPEG = "image/jpg"
    WEBP = "image/webp"


def get_content_type(file_path: Path) -> ContentType:
    try:
        suffix = file_path.suffix[1:].upper()
        return ContentType[suffix].value
    except Exception as e:
        print(f"Error parsing file_path: {file_path}")
        print(e)
        return None


def file_exists(s3_client: boto3.client, bucket: str, key: str) -> bool:
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
    except ClientError:
        return False
    return True


def upload_image(
    bucket, object_key: str, image_path: Path, slug: str, content_type: str
) -> bool:
    s3_client = boto3.client("s3")

    s3_client.upload_file(
        image_path, bucket, object_key, ExtraArgs={"ContentType": content_type}
    )
    return True
