import pandas as pd

def clean_data(raw_data):
    #Clean and validate raw data in memory
    if not raw_data:
        return None

    try:
        # Convert to DataFrame
        df = pd.DataFrame([raw_data])
        
        # Convert timestamps
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_convert('Asia/Kolkata')
        df['collection_time'] = pd.to_datetime(df['collection_time']).dt.tz_localize('Asia/Kolkata')
        
        
        # Numeric validation
        numeric_cols = ['price', 'high_24h', 'low_24h', 'volume_24h', 'market_cap']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        # Data quality checks
        df = df[
            (df['price'] > 0) &
            (df['volume_24h'] >= 0) &
            (df['timestamp'].notnull())
        ]
        
        # Add freshness metric
        df['data_freshness'] = (df['collection_time'] - df['timestamp']).dt.total_seconds()
        df = df[df['data_freshness'] < 3600]  # 1 hour threshold
        
        return df.iloc[0].to_dict() if not df.empty else None
        
    except Exception as e:
        print(f"Transformation error: {str(e)}")
        return None