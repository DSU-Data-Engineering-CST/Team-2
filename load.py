import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "auth_plugin": 'mysql_native_password'
}

def save_worldcoin_data(data):
    """Save transformed Worldcoin metrics into MySQL database."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS worldcoin_metrics (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    symbol VARCHAR(10) NOT NULL,
                    timestamp DATETIME NOT NULL,
                    open DECIMAL(12,6) NOT NULL,
                    high DECIMAL(12,6) NOT NULL,
                    low DECIMAL(12,6) NOT NULL,
                    close DECIMAL(12,6) NOT NULL,
                    volume DECIMAL(16,4) NOT NULL,
                    quote_volume DECIMAL(20,8) NOT NULL,
                    collection_time DATETIME NOT NULL,
                    UNIQUE KEY unique_timestamp (timestamp)
                );
            """)
            
            # Insert data with duplicate handling
            insert_query = """
                INSERT INTO worldcoin_metrics 
                (symbol, timestamp, open, high, low, close, volume, quote_volume, collection_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    open = VALUES(open),
                    high = VALUES(high),
                    low = VALUES(low),
                    close = VALUES(close),
                    volume = VALUES(volume),
                    quote_volume = VALUES(quote_volume),
                    collection_time = VALUES(collection_time)
            """
            
            values = (
                data['symbol'],
                data['timestamp'],
                data['open'],
                data['high'],
                data['low'],
                data['close'],
                data['volume'],
                data['quote_volume'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            cursor.execute(insert_query, values)
            connection.commit()
            print("✅ Worldcoin data inserted/updated successfully.")

    except Error as e:
        print(f"❌ Database error: {e}")
        if connection:
            connection.rollback()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()