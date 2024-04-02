import os
import csv
from dotenv import load_dotenv
import redshift_connector
from redshift_connector import Connection

load_dotenv()

def connect_to_database() -> Connection:
    """
    Connects to relevant database
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

def upload_transaction_data(conn: Connection, schema: str, transactions: list) -> None:
    """
    Uploads transaction data to the database
    """

    sql = "INSERT INTO transaction (timestamp, type_id, total, truck_id) VALUES (%s,%s,%s,%s)"

    with conn.cursor() as cur:
        cur.execute(f"SET SEARCH_PATH = {schema};")
        cur.executemany(sql, transactions)
        conn.commit()