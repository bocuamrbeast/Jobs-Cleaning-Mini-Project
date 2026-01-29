import os
from dotenv import load_dotenv

load_dotenv()

TEMP_DB = {
    "host": os.getenv("TEMP_DB_HOST"),
    "port": os.getenv("TEMP_DB_PORT"),
    "dbname": os.getenv("TEMP_DB_NAME"),
    "user": os.getenv("TEMP_DB_USER"),
    "password": os.getenv("TEMP_DB_PASSWORD"),
}