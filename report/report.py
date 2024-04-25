import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import redshift_connector
from redshift_connector import Connection


load_dotenv()


def get_db_connection() -> Connection:
    """Gets a connection to the database."""
    return redshift_connector.connect(
     host=os.getenv["DB_HOST"],
     database=os.getenv["DB_NAME"],
     port=os.getenv["DB_PORT"],
     user=os.getenv["DB_USERNAME"],
     password=os.getenv["DB_PASSWORD"]
     )
     


def get_overall_transaction_total(conn: Connection, date: datetime) -> float:
    """Returns a float of the total transaction value for the previous day."""

    comparison_date = date - timedelta(days=1)
    comparison_date = datetime.combine(comparison_date, datetime.min.time())

    with conn.cursor() as cur:
        cur.execute("SET SEARCH_PATH = {SCHEMA_NAME};")
        cur.execute(f"SELECT SUM(total) FROM transaction WHERE timestamp > '{comparison_date}';")
        result = float(cur.fetchall()[0][0])
    return result


def get_overall_transaction_avg(conn: Connection, date: datetime) -> float:
    """Returns a float of the average transaction value for the previous day."""

    comparison_date = date - timedelta(days=1)
    comparison_date = datetime.combine(comparison_date, datetime.min.time())

    with conn.cursor() as cur:
        cur.execute("SET SEARCH_PATH = {SCHEMA_NAME};")
        cur.execute(f"SELECT AVG(total) FROM transaction WHERE timestamp > '{comparison_date}';")
        result = float(cur.fetchall()[0][0])
    return result


def get_overall_transaction_total_per_truck(conn: Connection, date: datetime) -> list:
    """Returns a list of the total transaction value for each truck for the previous day."""

    comparison_date = date - timedelta(days=1)
    comparison_date = datetime.combine(comparison_date, datetime.min.time())

    with conn.cursor() as cur:
        cur.execute("SET SEARCH_PATH = {SCHEMA_NAME};")
        cur.execute(f"""
                    SELECT truck_id, SUM(total)
                    FROM transaction
                    WHERE timestamp > '{comparison_date}'
                    GROUP BY truck_id
                    ORDER BY truck_id;
                    """)
        result = list(cur.fetchall())

    dictionary_list = []
    for row in result:
        dict_row = {}
        dict_row["truck_id"] = row[0]
        dict_row["total"] = float(row[1])
        dictionary_list.append(dict_row)

    return dictionary_list


def get_avg_transaction_val_per_truck(conn: Connection, date: datetime) -> list:
    """Returns a list of the avg transaction value for each truck."""
    comparison_date = date - timedelta(days=1)
    comparison_date = datetime.combine(comparison_date, datetime.min.time())

    with conn.cursor() as cur:
        cur.execute("SET SEARCH_PATH = {SCHEMA_NAME};")
        cur.execute(f"""
                    SELECT truck_id, AVG(total)
                    FROM transaction
                    WHERE timestamp > '{comparison_date}'
                    GROUP BY truck_id
                    ORDER BY truck_id;
                    """)
        result = list(cur.fetchall())

    dictionary_list = []
    for row in result:
        dict_row = {}
        dict_row["truck_id"] = row[0]
        dict_row["avg"] = float(row[1])
        dictionary_list.append(dict_row)

    return dictionary_list


def get_no_of_transactions_per_truck(conn: Connection, date: datetime) -> list:
    """Returns a list of the number of transactions for each truck."""
    comparison_date = date - timedelta(days=1)
    comparison_date = datetime.combine(comparison_date, datetime.min.time())

    with conn.cursor() as cur:
        cur.execute("SET SEARCH_PATH = {SCHEMA_NAME};")
        cur.execute(f"""
                    SELECT truck_id, COUNT(total)
                    FROM transaction
                    WHERE timestamp > '{comparison_date}'
                    GROUP BY truck_id
                    ORDER BY truck_id;
                    """)
        result = list(cur.fetchall())

    dictionary_list = []
    for row in result:
        dict_row = {}
        dict_row["truck_id"] = row[0]
        dict_row["count"] = int(row[1])
        dictionary_list.append(dict_row)

    return dictionary_list


def create_total_transaction_table(transaction_totals_specific: list) -> str:
    """Generates a table from transaction totals."""
    html_str = """<h3>Total transaction value for each truck</h3>
                    <table border=1>
                        <tr>
                            <th>Truck ID</th>
                            <th>Total Transaction Value</th>
                        </tr>"""
    for truck in transaction_totals_specific:
        html_str += f"""<tr>
                            <td ALIGN=RIGHT>{truck['truck_id']}</td>"
                            <td ALIGN=CENTER>£{truck['total']}</td>
                        </tr>"""

    html_str += "</table>"
    return html_str


def create_avg_transaction_table(avg_transaction_val: list) -> str:
    """Creates a html string that represents a table of avg. transaction values."""
    html_str = """<h3>Avg. transaction value for each truck</h3>
                    <table border=1>
                        <tr>
                            <th>Truck ID</th>
                            <th>Avg. Transaction Value</th>
                        </tr>"""
    for truck in avg_transaction_val:
        html_str += f"""<tr>
                            <td ALIGN=RIGHT>{truck['truck_id']}</td>"
                            <td ALIGN=CENTER>£{truck['avg']}</td>
                        </tr>"""

    html_str += "</table>"
    return html_str


def create_transaction_count_table(transaction_count: list) -> str:
    """Produces a string representation of a transaction count html table."""
    html_str = """<h3>Transaction count for each truck</h3>
                    <table border=1>
                        <tr>
                            <th>Truck ID</th>
                            <th>Transaction Count</th>
                        </tr>"""
    for truck in transaction_count:
        html_str += f"""<tr>
                            <td ALIGN=RIGHT>{truck['truck_id']}</td>"
                            <td ALIGN=CENTER>{truck['count']}</td>
                        </tr>"""

    html_str += "</table>"
    return html_str


def handler(event, context):
    """Main function that compiles the data as a html string."""

    conn = get_db_connection()
    transaction_total_all = get_overall_transaction_total(conn, datetime.today())
    transaction_avg_all = get_overall_transaction_avg(conn, datetime.today())
    transaction_totals_specific = get_overall_transaction_total_per_truck(conn, datetime.today())
    avg_transaction_val = get_avg_transaction_val_per_truck(conn, datetime.today())
    transaction_count = get_no_of_transactions_per_truck(conn, datetime.today())
    conn.close()

    file_date = datetime.today() - timedelta(days=1)
    html_str = """<h1>&#128202; T3 Food Trucks Daily Report</h1>"""
    html_str += f"<h2>{file_date.strftime('%A %d %B %Y')}</h2>"
    html_str += "<h3>Metrics for all trucks</h3>"
    html_str += f"Total transaction value for all trucks: <b>£{transaction_total_all}</b> <br />"
    html_str += f"Average transaction value across all trucks: <b>£{transaction_avg_all}</b> <br />"

    html_str += create_total_transaction_table(transaction_totals_specific)

    html_str += create_avg_transaction_table(avg_transaction_val)

    html_str += create_transaction_count_table(transaction_count)

    return {"html": html_str}