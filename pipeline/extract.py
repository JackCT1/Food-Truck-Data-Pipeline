from datetime import datetime
from dotenv import load_dotenv
import logging
import os

from boto3 import client
import botocore.exceptions

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
ACCESS_KEY_ID = os.getenv("ACCESS_ID")
SECRET_ACCESS_KEY = os.getenv("ACCESS_KEY")

s3 = client('s3', aws_access_key_id = ACCESS_KEY_ID, aws_secret_access_key = SECRET_ACCESS_KEY)

def download_relevant_files_from_s3(client: client, bucket: str, folder: str) -> bool:
    """
    Accesses relevant s3 bucket, downloads contents and puts into specified directory
    """
    contents = s3.list_objects(Bucket=bucket)["Contents"]
    file_names = [list_object["Key"] for list_object in contents]
    files_downloaded = 0
    if files_downloaded > 0:
        return True
    return False