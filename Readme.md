# Real-Time Worldcoin Cryptocurrency ETL Pipeline

A serverless Python pipeline that collects, processes, and stores Worldcoin (WLD) market data directly into MySQL without intermediate file storage. The data is sourced from the CoinGecko API, ensuring real-time and reliable market information.

## Key Features
- **Direct-to-Database Storage** - Eliminates CSV files, stores data directly in MySQL
- **In-Memory Processing** - No disk I/O operations between ETL stages
- **5-Minute Interval Updates** - Automated data collection schedule
- **Data Validation** - Quality checks and freshness monitoring
- **Transaction Safety** - ACID-compliant database operations
- **IST Timezone Support** - Localized timestamp handling

## Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- `.env` file with database credentials
- Internet connection for API access

## Installation
```bash
# Clone repository
git clone https://github.com/DSU-Data-Engineering-CST/Team-2.git

# Install dependencies
pip install -r requirements.txt

# Create environment file
echo "DB_HOST=localhost
DB_USER=etl_user
DB_PASSWORD=secure_password
DB_NAME=crypto_data
auth_plugin=mysql_native_password" > .env
```

## Database Configuration
1. Create MySQL database and user:
```sql
CREATE DATABASE crypto_data;
CREATE USER 'etl_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON crypto_data.* TO 'etl_user'@'localhost';
```

2. Initialize database tables:
```bash
python main.py --init
```

## Usage
```bash
# Start the ETL pipeline
python main.py
```

**Expected Output:**
```
----------------------------------------
ETL Cycle Started: 2024-03-15 18:00:00
Successfully loaded data for 2024-03-15 12:30:00+05:30
----------------------------------------
```

## Environment Variables
| Variable       | Description           | Example           |
|----------------|-----------------------|-------------------|
| `DB_HOST`      | MySQL server address  | `localhost`       |
| `DB_USER`      | Database username     | `etl_user`        |
| `DB_PASSWORD`  | Database password     | `secure_password` |
| `DB_NAME`      | Target database name  | `crypto_data`     |
| `auth_plugin`  | Database password     | `secure_password` |


## Error Handling & Monitoring
- Automatic retry on API failures
- Duplicate entry prevention using `ON DUPLICATE KEY UPDATE`
- Transaction rollback on database errors
- Data freshness threshold (1 hour)

## Customization
1. **Modify Collection Interval**  
   Edit `time.sleep(300)` in `main.py`

2. **Add New Data Points**  
   Update:
   - `extract.py`: Add new API fields
   - `transform.py`: Include validation rules
   - `load.py`: Modify table schema and queries

3. **Change Timezone**  
   Modify `get_ist_time()` in `extract.py`

## Troubleshooting
**Common Issues:**
1. **Database Connection Failed**  
   - Verify MySQL service status
   - Check `.env` file permissions
   - Test credentials using MySQL Workbench

2. **No Data Received**  
   - Check CoinGecko API status
   - Verify internet connectivity
   - Monitor API response with:
     ```bash
     curl https://api.coingecko.com/api/v3/ping
     ```

**Logging:**  
All errors are printed to stdout with timestamps


