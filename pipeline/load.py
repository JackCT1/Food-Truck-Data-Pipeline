import os
import csv
from dotenv import load_dotenv
import redshift_connector
from redshift_connector import Connection

load_dotenv()

def connect_to_database() -> Connection:
    """
    Connects tp relevant database
    """

    return redshift_connector.connect(
     host=os.getenv["DB_HOST"],
     database=os.getenv["DB_NAME"],
     port=os.getenv["DB_PORT"],
     user=os.getenv["DB_USERNAME"],
     password=os.getenv["DB_PASSWORD"]
     )

def convert_csv_to_list(filepath: str) -> list:
    """
    Opens csv file and produces list of rows for database upload
    """

    with open(filepath, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        data = list(reader)

    return data[1:]