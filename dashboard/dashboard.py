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

alt.data_transformers.disable_max_rows()

def get_avg_transaction_chart(dataframe: pd.DataFrame, selected: [list]) -> alt.Chart:
    """Creates a bar chart that displays the average transaction value in selected trucks."""

    dataframe = dataframe[dataframe["truck_id"].isin(selected)]
    dataframe["total"] = dataframe["total"].astype("float")

    alt.data_transformers.disable_max_rows()

    return alt.Chart(dataframe).mark_bar(
                    ).encode(x='truck_id:N', y='mean(total):Q', color=alt.Color(
                        'truck_id:N',
                        scale={"scheme": "magma"}).legend(title="Truck ID"))


def get_daily_income_chart(dataframe: pd.DataFrame, selected: [list]) -> alt.Chart:
    """Creates a line chart showing the average daily income for selected trucks."""

    dataframe = dataframe[dataframe["truck_id"].isin(selected)]
    dataframe["total"] = dataframe["total"].astype("float")

    return alt.Chart(dataframe).mark_line().encode(
            x="day(timestamp):T",
            y="sum(total):Q",
            color=alt.Color(
                "truck_id:N",
                scale={"scheme": "magma"}).legend(
                    title="Truck ID"))


def get_type_pie_chart(dataframe: pd.DataFrame, selected: [list]) -> alt.Chart:
    """Creates a pie chart showing the proportion of cash & card transactions in selected trucks."""

    dataframe = dataframe[dataframe["truck_id"].isin(selected)]

    types = dataframe.groupby(["name"]).count().reset_index()
    types = types.rename(columns={"total": "count"})
    types = types[["name","count"]]

    return alt.Chart(types).mark_arc(
                     ).encode(theta='count',
                              color=alt.Color('name:N',
                                              scale={"scheme": "magma"}).legend(title="Type"))


def get_transaction_count_chart(dataframe: pd.DataFrame, selected: [list]) -> alt.Chart:
    """Creates a bar chart showing the total amount of transactions for selected trucks."""

    dataframe = dataframe[dataframe["truck_id"].isin(selected)]

    count = dataframe.groupby(["truck_id"]).count().reset_index()
    count = count.rename(columns={"total": "count"})
    count = count[["truck_id", "count"]]

    return alt.Chart(count).mark_bar(
    ).encode(x="truck_id:N", y="count:Q", color=alt.Color("truck_id:N",
                                                      scale={"scheme": "magma"}).legend(title="Truck ID"))

if __name__ == "__main__":
    conn = get_db_connection()

    transaction_df = fetch_dataframe(conn, "transaction")
    truck_df = fetch_dataframe(conn, "truck")
    type_df = fetch_dataframe(conn, "type")

    transaction_type_df = pd.merge(transaction_df,
                                type_df,
                                how="inner",
                                on=None,
                                left_on="type_id",
                                right_on="id")

    st. set_page_config(page_title="Food Truck Analytics",
                        page_icon=":bar_chart:",
                        layout="wide")

    st.title("T3 Food Truck Analytics")
    st.subheader("A dashboard with financial analytics for T3 food trucks.")
    st.sidebar.write(truck_df[["id","name"]])

    selected_trucks = st.sidebar.multiselect("Truck Selection",
                                            transaction_df["truck_id"].unique(),
                                            default=transaction_df["truck_id"].unique())

    col1, col2 = st.columns(2, gap="large")

    with col1:

        avg_value = transaction_df["total"].mean()
        avg_value = numpy.round(avg_value, 2)
        st.metric("Avg. Transaction Value", f"£{avg_value}")

        if selected_trucks:
            st.markdown("#### Avg. transaction value for each truck")
            avg_transaction_value = get_avg_transaction_chart(transaction_df, selected_trucks)
            st.altair_chart(avg_transaction_value, use_container_width=True)

            st.markdown("#### Proportion of transaction types")
            type_pie_chart = get_type_pie_chart(transaction_type_df, selected_trucks)
            st.altair_chart(type_pie_chart, use_container_width=True)

        cash_percent = transaction_type_df[transaction_type_df["name"] == "cash"]["name"].count() / transaction_type_df["name"].count()
        cash_percent = numpy.round(cash_percent, 3)*100
        st.metric("Overall % of cash transactions", f"{cash_percent}%")


    with col2:

        if selected_trucks:
            st.markdown("#### Daily income trends for each truck")
            daily_sum_total = get_daily_income_chart(transaction_df, selected_trucks)
            st.altair_chart(daily_sum_total, use_container_width=True)

            st.markdown("#### Transaction count per truck")
            transaction_count = get_transaction_count_chart(transaction_df, selected_trucks)
            st.altair_chart(transaction_count, use_container_width=True)