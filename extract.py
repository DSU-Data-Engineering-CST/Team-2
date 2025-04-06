import requests
from datetime import datetime, timezone, timedelta

def get_ist_time():
    #Get current IST time (UTC+5:30)
    return datetime.now(timezone.utc).astimezone(
        timezone(timedelta(hours=5, minutes=30))
    )

def fetch_worldcoin_data():
    #Fetch Worldcoin data from CoinGecko API
    url = "https://api.coingecko.com/api/v3/coins/worldcoin-wld"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            'timestamp': data['last_updated'],
            'price': data['market_data']['current_price']['usd'],
            'high_24h': data['market_data']['high_24h']['usd'],
            'low_24h': data['market_data']['low_24h']['usd'],
            'volume_24h': data['market_data']['total_volume']['usd'],
            'market_cap': data['market_data']['market_cap']['usd'],
            'collection_time': get_ist_time().strftime('%Y-%m-%d %H:%M:%S')
        }
        
    except Exception as e:
        print(f"Extraction error: {str(e)}")
        return None