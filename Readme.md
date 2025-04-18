# Worldcoin Cryptocurrency ETL Pipeline

A serverless Python ETL pipeline for real-time Worldcoin (WLD) market data processing, designed to run in Docker containers. Collects, transforms, and stores cryptocurrency metrics directly into MySQL without intermediate file storage.


## Project Objectives

This project aims to:

- **Analyze Market Trends**  
  By collecting and storing historical price and volume data, the system supports the identification of key trends and market patterns for Worldcoin.

- **Enable Quantitative Research**  
  The pipeline enables structured access to clean, time-series data, facilitating quantitative analysis and strategy development for crypto trading and investment.

- **Build a Scalable Crypto Analytics Platform**  
  The modular and containerized setup lays the foundation for a broader system capable of ingesting, transforming, and storing data for multiple cryptocurrencies.

- **Support Machine Learning Models**  
  Clean, labeled historical data can be used to train ML models for price prediction, anomaly detection, or volatility forecasting.

- **Preserve Data for Academic Use**  
  Enables reproducibility and long-term study by storing consistent historical records, useful in academic research, statistical modeling, and capstone projects.

---

## Key Features

- **Containerized Workflow**  
  Dockerized MySQL + Python ETL service with health monitoring
- **Direct Database Storage**  
  Eliminates CSV intermediates using in-memory processing
- **Data Validation**  
  Quality checks and freshness monitoring
- **Persistent Storage**  
  MySQL data volume for crash recovery
- **IST Timezone Support**  
  Localized timestamp handling


## Prerequisites

- Docker 20.10+
- Python 3.9+ (for local development only)
- Internet connection for API access

## Installation

```bash
# Clone repository

git clone https://github.com/DSU-Data-Engineering-CST/Team-2[World-Coin].git

# Install dependencies
pip install -r requirements.txt

```

## Quick Start

```bash
# Build and launch containers
docker-compose up --build -d

# Monitor ETL logs
docker-compose logs -f etl
```

## Database Configuration

Automatically configured via Docker:


```

## Environment Variables

| Variable        | Description            | Docker Default      |
|------------------|------------------------|----------------------|
| `DB_HOST`        | MySQL service name     | `mysql`              |
| `DB_PORT`        | MySQL port             | `3306`               |
| `DB_USER`        | Database username      | `etl_user`           |
| `DB_PASSWORD`    | Database password      | `secure_password`    |
| `DB_NAME`        | Target database name   | `crypto_data`        |
| `auth_plugin`    | MySQL auth plugin      | `mysql_native_password` |

## Customization

```

### Add New Metrics
1. Update `extract.py` with new API fields
2. Add validation rules in `transform.py`
3. Modify table schema in `load.py`

### Change Timezone
```python
# extract.py
def get_ist_time():
    return datetime.now(timezone(timedelta(hours=5, minutes=30)))  # IST
```

## Monitoring & Troubleshooting

**Inspect MySQL Data:**
```bash
docker exec -it worldcoin-mysql mysql -u etl_user -p crypto_data
```

## Error Handling & Monitoring

- Automatic retry on API failures
- Logs for every pipeline execution
- Alerts for connection issues or data validation failures

## Maintainers

- Team 2 – Data Engineering @ DSU CST
```

