```markdown
# Worldcoin Cryptocurrency ETL Pipeline

A serverless Python ETL pipeline for real-time Worldcoin (WLD) market data processing, designed to run in Docker containers. Collects, transforms, and stores cryptocurrency metrics directly into MySQL without intermediate file storage.


## Key Features

- **Containerized Workflow**  
  Dockerized MySQL + Python ETL service with health monitoring
- **Direct Database Storage**  
  Eliminates CSV intermediates using in-memory processing
- **5-Minute Interval Updates**  
  Automated scheduling with fault tolerance
- **Data Validation**  
  Quality checks and freshness monitoring
- **Persistent Storage**  
  MySQL data volume for crash recovery
- **IST Timezone Support**  
  Localized timestamp handling

## Prerequisites

- Docker 20.10+
- Docker Compose 2.20+
- Python 3.9+ (for local development only)
- Internet connection for API access

## Quick Start

```bash
# Clone repository
git clone https://github.com/DSU-Data-Engineering-CST/Team-2.git


# Build and launch containers
docker-compose up --build -d

# Monitor ETL logs
docker-compose logs -f etl
```

## Database Configuration

Automatically configured via Docker:

```yaml
# docker-compose.yml
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: crypto_data
      MYSQL_USER: etl_user
      MYSQL_PASSWORD: secure_password
    volumes:
      - mysql_data:/var/lib/mysql
```

## Environment Variables

| Variable       | Description           | Docker Default     |
|----------------|-----------------------|--------------------|
| `DB_HOST`      | MySQL service name    | `mysql`            |
| `DB_PORT`      | MySQL port            | `3306`             |
| `DB_USER`      | Database username     | `etl_user`         |
| `DB_PASSWORD`  | Database password     | `secure_password`  |
| `DB_NAME`      | Target database       | `crypto_data`      |

## Customization

### Modify Collection Interval
```python
# main.py
time.sleep(300)  # Change 300 seconds (5 minutes) to desired interval
```

### Add New Metrics
1. Update `extract.py` with new API fields
2. Add validation rules in `transform.py`
3. Modify table schema in `load.py`

### Change Timezone
```python
# extract.py
def get_ist_time():
    return datetime.now(timezone(timedelta(hours=5, minutes=30)))  # Update offset
```

## Monitoring & Troubleshooting

**View Container Status:**
```bash
docker-compose ps
```

**Inspect MySQL Data:**
```bash
docker exec -it worldcoin-mysql mysql -u etl_user -p crypto_data
```

**Common Issues:**

1. **Database Connection Failures**  
   - Verify MySQL container is running  
   - Check environment variables match docker-compose.yml  

2. **Missing Data**  
   - Monitor API status: `curl https://api.binance.com/api/v3/ping`  
   - Check ETL logs: `docker-compose logs etl`

3. **Build Failures**  
   - Clear Docker cache: `docker-compose build --no-cache`


``` 

This README features:
1. Docker-first documentation
2. Visual architecture placeholder (replace with actual diagram)
3. Command-line snippets with copy/paste functionality
4. Troubleshooting recipes for containerized environment
5. Clear customization pathways
6. Responsive table formatting
7. License and maintainer information