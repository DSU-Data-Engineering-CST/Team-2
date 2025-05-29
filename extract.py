import requests
import pandas as pd
from datetime import datetime

def fetch_coin_data():
    try:
        url = "https://api.binance.com/api/v3/klines"
        all_data = []

        # Worldcoin launch date
        start_time = int(datetime(2023, 7, 24).timestamp() * 1000)
        end_time = int(datetime.now().timestamp() * 1000)

        params = {
            "symbol": "WLDUSDT",
            "interval": "5m",
            "limit": 1000,
            "startTime": start_time
        }

        print("⏳ Fetching all available 5-minute WLD data since launch...")

        while True:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                break

            all_data.extend(data)

            # Set next start time to 1ms after last candle's close time
            params['startTime'] = int(data[-1][6]) + 1

            if params['startTime'] > end_time:
                break

            # Optional: Show progress every 10,000 rows
            if len(all_data) % 10000 == 0:
                print(f"✓ Retrieved {len(all_data)} rows...")

        columns = [
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ]

        df = pd.DataFrame(all_data, columns=columns)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['year'] = df['timestamp'].dt.year
        df['month'] = df['timestamp'].dt.month

        # Convert numeric columns
        numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'quote_volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

        print(f"✅ Successfully retrieved {len(df)} rows of 5-minute data since launch.")
        return df.dropna().reset_index(drop=True)

    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Extraction Error: {str(e)}")
        return pd.DataFrame()
