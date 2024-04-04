from datetime import datetime
from dotenv import load_dotenv
import os

from extract import connect_to_s3, download_relevant_files_from_s3
from transform import combine_files_into_dataframe, clean_dataframe
from load import connect_to_database, convert_csv_to_list, upload_transaction_data

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
ACCESS_KEY_ID = os.getenv("ACCESS_ID")
SECRET_ACCESS_KEY = os.getenv("ACCESS_KEY")
PATH = "data/recent_transactions.csv"


if __name__ == "__main__":
    s3_client = connect_to_s3(ACCESS_KEY_ID, SECRET_ACCESS_KEY)

    downloaded_s3_files = download_relevant_files_from_s3(s3_client, BUCKET_NAME, 'data', datetime.today())

    if downloaded_s3_files:
        combine_files_into_dataframe('recent_transactions', 'data')
        clean_dataframe(PATH)

        connection = connect_to_database()
        data_to_upload = convert_csv_to_list(PATH)
        upload_transaction_data(connection, data_to_upload)
    else:
        print()