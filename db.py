import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    driver = os.getenv("DB_DRIVER")
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")

    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "TrustServerCertificate=yes;"
    )

    if os.getenv("DB_TRUSTED", "yes").lower() == "yes":
        conn_str += "Trusted_Connection=yes;"
    else:
        conn_str += f"UID={os.getenv('DB_USER')};PWD={os.getenv('DB_PASSWORD')};"

    return pyodbc.connect(conn_str)