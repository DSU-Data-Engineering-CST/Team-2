import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_coin_data():
    """Fetch Worldcoin (WLD/USDT) market data from Binance API"""
    try:
        # Binance API parameters
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": "WLDUSDT",
            "interval": "15m",  # Match 15-minute collection interval
            "limit": 1000       # Get enough data for meaningful analysis
        }

        # API request
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Create DataFrame from response
        columns = [
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ]
        
        df = pd.DataFrame(response.json(), columns=columns)
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Select and convert numeric columns
        numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        # Filter recent data (last 24 hours)
        df = df[df['timestamp'] > datetime.now() - timedelta(hours=24)]
        
        return df.dropna().reset_index(drop=True)

    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Extraction Error: {str(e)}")
        return pd.DataFrame()