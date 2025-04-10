import time
from datetime import datetime
from extract import fetch_coin_data
from transform import clean_wld_data
from load import save_worldcoin_data

def run_etl_pipeline():
    """Execute complete in-memory ETL pipeline"""
    start_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    print(f"\n{'-' * 40}")
    print(f" ETL Cycle Started: {start_time}")
    
    try:
        # Extract phase
        print("\n⚡ Extracting Worldcoin data...")
        raw_data = fetch_coin_data()
        if raw_data.empty:
            print("❌ No data extracted")
            return
        print("✅ Extraction completed")

        # Transform phase
        print("\n🔄 Transforming data...")
        clean_data = clean_wld_data(raw_data)
        if clean_data.empty:
            print("❌ Invalid data transformation")
            return
        print("✅ Transformation completed")

        # Load phase
        print("\n📦 Loading to database...")
        save_worldcoin_data(clean_data.iloc[0].to_dict())
        print("✅ Loading completed")

    except Exception as e:
        print(f"\n‼️ Pipeline error: {str(e)}")
    finally:
        end_time = datetime.now().strftime('%H:%M:%S')
        print(f"\n{'-' * 40}")
        print(f" ETL Cycle Completed: {end_time}")
        print("Next run in 15 minutes...")

if __name__ == "__main__":
    print("\n" + "=" * 40)
    print(" Initializing Worldcoin ETL Pipeline")
    print("=" * 40)
    
    while True:
        run_etl_pipeline()
        time.sleep(1200)  # 5-minute interval