from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

DATA_PATH = "data/data.csv"

def run_pipeline():
    print("Running ETL pipeline...")

    extract_data(DATA_PATH)
    transform_data()
    load_data()

    print("Finished ETL pipeline")

if __name__ == "__main__":
    run_pipeline()