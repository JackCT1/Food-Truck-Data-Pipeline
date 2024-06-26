from datetime import datetime
from dotenv import load_dotenv
import logging
import os

from boto3 import client
import botocore.exceptions

def connect_to_s3(access_key: str, secret_access_key: str)-> client:
    return client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)

def download_relevant_files_from_s3(client: client, bucket: str, folder: str, today: datetime) -> bool:
    """
    Accesses relevant s3 bucket, downloads contents and puts into specified directory
    """
    contents = client.list_objects(Bucket=bucket)["Contents"]
    file_names = [list_object["Key"] for list_object in contents]

    current_year = today.year
    current_month = today.month
    current_day = today.day
    current_hour = today.hour
    
    files_downloaded = 0
    for file in file_names:
        if f"/{current_year}-{current_month}/{current_day}/{current_hour}" in file:
            client.download_file(bucket, file, f"{folder}/{file}")
        files_downloaded += 1
    if files_downloaded > 0:
        return True
    return False