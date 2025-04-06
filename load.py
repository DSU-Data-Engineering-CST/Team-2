import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

load_dotenv("config.env")

def create_connection():
    #Create and return MySQL connection
    try:
        return mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            auth_plugin=('mysql_native_password')
        )
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        return None

def initialize_database():
    #Create table if not exists
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS worldcoin_metrics (
                    timestamp DATETIME PRIMARY KEY,
                    price DECIMAL(18,8),
                    high_24h DECIMAL(18,8),
                    low_24h DECIMAL(18,8),
                    volume_24h DECIMAL(18,2),
                    market_cap DECIMAL(18,2),
                    collection_time DATETIME,
                    data_freshness INT
                )
            """)
            conn.commit()
        finally:
            conn.close()

def load_to_database(clean_data):
    #Directly load cleaned data to MySQL
    if not clean_data:
        return

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO worldcoin_metrics
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    price=VALUES(price),
                    high_24h=VALUES(high_24h),
                    low_24h=VALUES(low_24h),
                    volume_24h=VALUES(volume_24h),
                    market_cap=VALUES(market_cap),
                    collection_time=VALUES(collection_time),
                    data_freshness=VALUES(data_freshness)
            """
            cursor.execute(insert_query, (
                clean_data['timestamp'].to_pydatetime(),
                clean_data['price'],
                clean_data['high_24h'],
                clean_data['low_24h'],
                clean_data['volume_24h'],
                clean_data['market_cap'],
                clean_data['collection_time'].to_pydatetime(),
                clean_data['data_freshness']
            ))
            conn.commit()
            print(f"Successfully loaded data for {clean_data['timestamp']}")
        except Exception as e:
            print(f"Loading error: {str(e)}")
            conn.rollback()
        finally:
            conn.close()