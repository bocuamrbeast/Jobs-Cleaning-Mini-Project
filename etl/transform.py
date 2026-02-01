import psycopg2
import os
from config import TEMP_DB

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BASE_DIR)
TRANSFORM_PATH = os.path.join(BASE_DIR, "sql", "transform")

def transform_data():
    print("Transforming data...")

    conn = psycopg2.connect(**TEMP_DB)
    cur = conn.cursor()

    with open(TRANSFORM_PATH, "r", encoding="utf-8") as f:
        sql = f.read()

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()

    print("Transform completed.")
