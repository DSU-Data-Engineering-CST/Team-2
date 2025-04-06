import time
from datetime import datetime
from extract import fetch_worldcoin_data
from transform import clean_data
from load import load_to_database, initialize_database

def run_etl_pipeline():
    #Execute complete in-memory ETL pipeline
    print(f"\n{'-'*40}")
    print(f"ETL Cycle Started: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    
    try:
        # Extract
        raw_data = fetch_worldcoin_data()
        if not raw_data:
            print("No data extracted")
            return

        # Transform
        clean_record = clean_data(raw_data)
        if not clean_record:
            print("Invalid data transformation")
            return

        # Load
        load_to_database(clean_record)
        
    except Exception as e:
        print(f"Pipeline error: {str(e)}")
    finally:
        print(f"{'-'*40}\n")

if __name__ == "__main__":
    # Initialize database
    initialize_database()
    
    # Run pipeline every 5 minutes
    while True:
        run_etl_pipeline()
        time.sleep(300)