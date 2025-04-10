import pandas as pd

def clean_wld_data(raw_df):
    # Worldcoin-specific data cleaning
    try:
        df = raw_df.copy()
        numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        # Worldcoin-specific filters
        df = df[df['volume'] > 1000]  # Filter low-volume noise
        df['price_change'] = df['close'] - df['open']
        df['symbol'] = 'WLD/USDT'  # Add trading pair
        
        return df.dropna().reset_index(drop=True)
    except Exception as e:
        print(f"WLD Cleaning Error: {str(e)}")
        return pd.DataFrame()