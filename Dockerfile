FROM python:3.9-slim

# Use a Linux-style working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Make sure the shell script is executable
RUN chmod +x run_etl.sh

# Run the ETL pipeline using the shell script
CMD ["bash", "run_etl.sh"]
