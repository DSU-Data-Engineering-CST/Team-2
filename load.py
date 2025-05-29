import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Load environment variables
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "worldcoin_metrics"),
    "auth_plugin": 'mysql_native_password'
}

def ensure_database_exists():
    """Ensure the database exists, create if it doesn't"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            auth_plugin=DB_CONFIG["auth_plugin"],
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"✅ Verified database '{DB_CONFIG['database']}' exists or created.")
    except Error as e:
        print(f"❌ Database verification failed: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def ensure_table_exists():
    """Creates the table if it doesn't exist"""
    connection = None
    try:
        ensure_database_exists()  # Ensure DB exists before table creation

        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        create_table_query = """
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
                trades INT NOT NULL,
                collection_time DATETIME NOT NULL,
                typical_price DECIMAL(12,6) NOT NULL,
                weighted_price DECIMAL(12,6) NOT NULL,
                `year` INT NOT NULL,
                month INT NOT NULL,
                week INT NOT NULL,
                `year_month` VARCHAR(7) NOT NULL,
                `iso_week` VARCHAR(10) NOT NULL,
                SMA_7 DECIMAL(12,6),
                EMA_7 DECIMAL(12,6),
                TMA_7 DECIMAL(12,6),
                day INT NOT NULL,
                UNIQUE KEY unique_timestamp (timestamp)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        print("✅ Verified table exists")
        
    except Error as e:
        print(f"❌ Table verification failed: {e}")
        raise
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def save_worldcoin_data(data):
    """Saves data with automatic table verification"""
    try:
        ensure_table_exists()
    except Error as e:
        print(f"❌ Cannot proceed with save: {e}")
        return False
    
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO worldcoin_metrics 
        (symbol, timestamp, open, high, low, close, volume, quote_volume, trades, collection_time, typical_price, weighted_price,
        `year`, month, week, `year_month`, `iso_week`, SMA_7, EMA_7, TMA_7, day)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            open = VALUES(open),
            high = VALUES(high),
            low = VALUES(low),
            close = VALUES(close),
            volume = VALUES(volume),
            quote_volume = VALUES(quote_volume),
            trades = VALUES(trades),
            collection_time = VALUES(collection_time),
            typical_price = VALUES(typical_price),
            weighted_price = VALUES(weighted_price),
            `year` = VALUES(`year`),
            month = VALUES(month),
            week = VALUES(week),
            `year_month` = VALUES(`year_month`),
            `iso_week` = VALUES(`iso_week`),
            SMA_7 = VALUES(SMA_7),
            EMA_7 = VALUES(EMA_7),
            TMA_7 = VALUES(TMA_7),
            day = VALUES(day)
        """
        
        values = (
            str(data['symbol']),
            data['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
            float(data['open']),
            float(data['high']),
            float(data['low']),
            float(data['close']),
            float(data['volume']),
            float(data['quote_volume']),
            int(data['trades']),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            float(data['typical_price']),
            float(data['weighted_price']),
            int(data['year']),
            int(data['month']),
            int(data['week']),
            str(data['year_month']),
            str(data['iso_week']),
            float(data['SMA_7']) if data['SMA_7'] is not None else None,
            float(data['EMA_7']) if data['EMA_7'] is not None else None,
            float(data['TMA_7']) if data['TMA_7'] is not None else None,
            int(data['day'])
        )
        
        cursor.execute(insert_query, values)
        connection.commit()
        print("✅ Data saved successfully")
        return True
        
    except Error as e:
        print(f"❌ Save error: {e}")
        if connection:
            connection.rollback()
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def initialize_database():
    """Full database initialization"""
    try:
        test_conn = mysql.connector.connect(**DB_CONFIG)
        test_conn.close()
        
        ensure_table_exists()
        print("\n✅ Database is ready")
        return True
        
    except Error as e:
        print(f"\n❌ Initialization failed: {e}")
        if "Unknown database" in str(e):
            print("Please run the database setup first")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print(" WORLDCOIN DATABASE VERIFICATION ".center(50, "="))
    print("="*50)
    
    if initialize_database():
        print("\nDatabase structure is ready for use")
    else:
        print("\nDatabase setup required. Please check:")
        print("1. MySQL server is running")
        print("2. User has proper privileges")
        print(f"3. Database '{DB_CONFIG['database']}' exists")
