import altair as alt
import os
import numpy
import pandas as pd
from redshift_connector import Connection
import streamlit as st

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

def get_dataframe(conn: redshift_connector.Connection, schema_name: str, table_name: str):
    with conn.cursor() as cur:
        cur.execute("SET SEARCH_PATH = {schema_name};")
        cur.execute(f"SELECT * FROM {table_name};")
        dataframe = cur.get_dataframe()
    
    return dataframe

if __name__ == "__main__":
    ''