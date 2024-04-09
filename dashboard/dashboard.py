import altair as alt
import numpy
import pandas as pd
import redshift_connector
import streamlit as st

from load import connect_to_database

def get_dataframe(conn: redshift_connector.Connection, schema_name: str, db_name: str):
    with conn.cursor() as cur:
        cur.execute("SET SEARCH_PATH = {schema_name};")
        cur.execute(f"SELECT * FROM {db_name};")
        transaction_df = cur.get_dataframe()
    
    return transaction_df