from etl.extract import extract_data

DATA_PATH = "data/data.csv"

def run_pipeline():
    print("Running ETL pipeline...")

    extract_data(DATA_PATH)

    print("Finished ETL pipeline")

if __name__ == "__main__":
    run_pipeline()