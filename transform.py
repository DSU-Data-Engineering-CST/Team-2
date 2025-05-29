import pandas as pd
from datetime import datetime

def clean_wld_data(raw_df):
    """Clean and transform Worldcoin 5-minute data for ETL pipeline"""
    try:
        df = raw_df.copy()

        # Convert numeric columns
        numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_volume', 'trades']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

        # Filter low-volume records
        df = df[df['volume'] > 1000]

        # Add constant and calculated fields
        df['symbol'] = 'WLD/USDT'
        df['collection_time'] = pd.Timestamp.now()
        df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
        df['weighted_price'] = df['quote_volume'] / df['volume']

        # Parse and sort timestamps
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp')

        # Time features
        df['year'] = df['timestamp'].dt.year
        df['month'] = df['timestamp'].dt.month
        df['week'] = df['timestamp'].dt.isocalendar().week
        df['iso_week'] = df['timestamp'].dt.strftime('%G-W%V')
        df['year_month'] = df['timestamp'].dt.strftime('%Y-%m')
        df['day'] = df['timestamp'].dt.weekday + 1  # Monday=1, Sunday=7

        # Technical indicators
        df['SMA_7'] = df['close'].rolling(window=7).mean()
        df['EMA_7'] = df['close'].ewm(span=7, adjust=False).mean()
        df['TMA_7'] = df['close'].rolling(window=7).mean().rolling(window=7).mean()

        # Generate ID
        df.reset_index(drop=True, inplace=True)
        df['id'] = df.index + 1

        # Final column order
        final_columns = [
            'id', 'symbol', 'timestamp', 'open', 'high', 'low', 'close',
            'volume', 'quote_volume', 'trades', 'collection_time',
            'typical_price', 'weighted_price', 'year', 'month', 'week',
            'year_month', 'iso_week', 'SMA_7', 'EMA_7', 'TMA_7', 'day'
        ]

        return df[final_columns].dropna().reset_index(drop=True)

    except Exception as e:
        print(f"Cleaning Error: {str(e)}")
        return pd.DataFrame()
