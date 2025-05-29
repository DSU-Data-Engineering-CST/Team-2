# 📈 Worldcoin Historical Data ETL Pipeline

A scalable, container-friendly ETL pipeline to fetch, transform, and store historical 5-minute interval data for Worldcoin (WLD/USDT) from Binance into a MySQL database.

---

## 🚀 Project Overview

This project automates the full ETL (Extract, Transform, Load) process for Worldcoin cryptocurrency data:

- **Extraction**: Fetches historical WLD/USDT data from Binance since its launch.
- **Transformation**: Cleans data, computes technical indicators (SMA, EMA, TMA), and enriches it with time features.
- **Loading**: Saves processed records to a MySQL database with schema validation and deduplication.

---

## 📂 Folder Structure

```

.
├── extract.py        # Data extraction from Binance API
├── transform.py      # Data transformation and feature engineering
├── load.py           # Database and table creation, and data loading
├── main.py           # ETL orchestration script
├── .env              # Environment variables (MySQL credentials)
├── requirements.txt  # Python dependencies

````

---

## 🧪 Features

- ⏱ Retrieves 5-minute candles since WLD's launch.
- 🧼 Cleans, filters, and enriches data with technical and temporal indicators.
- 🛢 Automatically creates MySQL database and table if absent.
- 🔄 Avoids duplicate records using timestamp-based uniqueness.
- 📊 Supports SMA, EMA, and TMA calculation on closing price.

---

## ⚙️ Requirements

- Python 3.8+
- MySQL Server
- Internet access (to call Binance API)

Install dependencies with:

```bash
pip install -r requirements.txt
````

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=worldcoin_metrics
```

---

## 💡 How It Works

Run the pipeline with:

```bash
python main.py
```

This executes:

1. `fetch_coin_data()` → Binance API (from `extract.py`)
2. `clean_wld_data()` → cleans and computes features (from `transform.py`)
3. `save_worldcoin_data()` → loads into DB (from `load.py`)

Each row is enriched with:

* `typical_price`, `weighted_price`
* Time-based fields: year, month, week, iso\_week, etc.
* Technical indicators: `SMA_7`, `EMA_7`, `TMA_7`

---

## 🛠 Schema Details (`worldcoin_metrics`)

| Column                                         | Type          | Description                |
| ---------------------------------------------- | ------------- | -------------------------- |
| id                                             | INT           | Auto-increment primary key |
| symbol                                         | VARCHAR(10)   | "WLD/USDT"                 |
| timestamp                                      | DATETIME      | Start time of candle       |
| open, high, low, close                         | DECIMAL       | OHLC price data            |
| volume                                         | DECIMAL       | Trade volume               |
| quote\_volume                                  | DECIMAL       | Quote asset volume         |
| trades                                         | INT           | Number of trades           |
| collection\_time                               | DATETIME      | Data fetch timestamp       |
| typical\_price                                 | DECIMAL       | Avg of (high+low+close)/3  |
| weighted\_price                                | DECIMAL       | quote\_volume / volume     |
| SMA\_7, EMA\_7, TMA\_7                         | DECIMAL       | Technical indicators       |
| year, month, week, iso\_week, year\_month, day | Time features |                            |

---

## ⚠️ Error Handling

* Gracefully retries on API or DB failure.
* Logs messages for failed inserts.
* Uses deduplication via `ON DUPLICATE KEY UPDATE`.

---

## 📌 Future Improvements

* Add containerization via Docker Compose
* Schedule recurring ETL with cron
* Include more symbols from Binance

---

## 👨‍💻 Authors

* Team 2 — Data Engineering, Dept. of CST, DSU

---

## 📜 License

This project is for academic purposes only.

```
