import psycopg2
from config import TEMP_DB, WAREHOUSE_DB

def load_data():
    print("Loading data to warehouse...")

    temp_conn = psycopg2.connect(**TEMP_DB)
    temp_cur = temp_conn.cursor()

    wh_conn = psycopg2.connect(**WAREHOUSE_DB)
    wh_cur = wh_conn.cursor()

    temp_cur.execute("""
        SELECT 
            created_date,
            job_title,
            company,
            job_group,
            min_salary,
            max_salary,
            salary_unit,
            city,
            district,
            time,
            link_description
        FROM jobs_transformed
    """)

    rows = temp_cur.fetchall()

    insert_sql = """
        INSERT INTO jobs_cleaned (
            created_date, job_title, company, job_group,
            min_salary, max_salary, salary_unit,
            city, district, time, link_description
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    wh_cur.executemany(insert_sql, rows)

    wh_conn.commit()

    wh_cur.close()
    wh_conn.close()

    print("Load completed.")

    temp_cur.execute("""
    TRUNCATE TABLE jobs_raw;
    DROP TABLE jobs_transformed;
    """)

    temp_conn.commit()
    temp_cur.close()
    temp_conn.close()

    print("Cleared temp data.")
