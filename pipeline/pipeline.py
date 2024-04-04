from datetime import datetime
from dotenv import load_dotenv
import os

from extract import download_relevant_files_from_s3
from transform import combine_files_into_dataframe, clean_dataframe
from load import connect_to_database, convert_csv_to_list, upload_transaction_data

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
ACCESS_KEY_ID = os.getenv("ACCESS_ID")
SECRET_ACCESS_KEY = os.getenv("ACCESS_KEY")

if __name__ == "__main__":
    ''