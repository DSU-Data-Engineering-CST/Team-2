from extract import fetch_coin_data
from transform import clean_wld_data
from load import save_worldcoin_data
import time

def run_pipeline():
    start_time = time.time()
    print("\n" + "="*50)
    print(" WORLDCOIN HISTORICAL DATA PIPELINE ")
    print("="*50)
    
    try:
        # Extract
        print("\n[1/3] EXTRACTING WLD data since launch...")
        raw_data = fetch_coin_data()
        if raw_data.empty:
            raise ValueError("No data extracted")

        # Transform
        print("\n[2/3] CLEANING AND TRANSFORMING DATA...")
        clean_data = clean_wld_data(raw_data)
        if clean_data.empty:
            raise ValueError("No data after cleaning")

        # Load
        print("\n[3/3] SAVING TO DATABASE...")

        total_rows = len(clean_data)
        for idx, row in clean_data.iterrows():
            success = save_worldcoin_data(row.to_dict())
            if not success:
                print(f"⚠️ Warning: Failed to save row id {row['id']} at index {idx}")
            
            # Progress every 500 rows
            if (idx + 1) % 500 == 0 or (idx + 1) == total_rows:
                print(f"✓ Saved {idx + 1}/{total_rows} rows...")

        print(f"\n✅ Pipeline completed in {time.time() - start_time:.2f} seconds")
        print(f"➤ Total rows processed: {total_rows}")

    except Exception as e:
        print(f"\n❌ Pipeline failed: {str(e)}")

if __name__ == "__main__":
    run_pipeline()
