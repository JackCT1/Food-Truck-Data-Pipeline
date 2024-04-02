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