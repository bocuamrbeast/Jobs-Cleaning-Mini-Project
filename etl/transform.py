import psycopg2
from config import TEMP_DB

TRANSFORM_PATH = "sql/transform"

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
