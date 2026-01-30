import psycopg2
from config import TEMP_DB

def extract_data(data_path: str):
    print("Extracting data...")
    print("Connecting to temp database...")
    conn = psycopg2.connect(**TEMP_DB)
    cur = conn.cursor()

    print("Loading data into temp...")
    with open(data_path, "r", encoding="utf-8") as f:
        cur.copy_expert(
            """
            COPY jobs_raw
            FROM STDIN
            WITH CSV HEADER
            DELIMITER ','
            """,
            f
        )

    conn.commit()
    cur.close()
    conn.close()
    
    print("Extract completed.")
