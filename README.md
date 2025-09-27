# Project Setup Guide

This project involves setting up two Docker containers: one for a PostgreSQL database and the other for cron tasks that handle ETL (Extract, Transform, Load) operations. The setup also includes a simple FastAPI endpoint to retrieve post counts for each user.

## Getting Started

Follow the steps below to set up and run the project.

### 1. Set up Environment Variables

First, create the environment variables configuration file by copying the example file:

```bash
cp .env.example .env
````

### 2. Modify Cron Task Schedule

Next, update the cron task schedule as needed by editing the appropriate configuration files.

### 3. Start Database and ETL Scripts

To run the ETL scripts and start the database, follow these steps:

1. Ensure the `run.sh` script is executable:

   ```bash
   chmod +x run.sh
   ```

2. Run the script to build, configure the Docker containers, and start the FastAPI server:

   ```bash
   ./run.sh
   ```

### 4. Access ETL Logs

If you want to check the logs for the ETL scripts, you can connect to the cron container and view the cron logs by running:

```bash
docker exec -it <cron-container-name> cat /var/log/cron.log
```

### 5. FastAPI Endpoint

A simple FastAPI endpoint is provided to retrieve the post count for each user. You can access it after the containers are running.

To access it go to : [http://localhost:8000/top](http://localhost:8000/top)

## Project Architecture

* **PostgreSQL Database Container**: Holds the database where the posts data is stored.
* **Cron Container**: Runs cron tasks to handle ETL operations. There are two ETL scripts for extracting and transforming data.
* **FastAPI Endpoint**: Provides an API to retrieve the post count for each user.

### ETL Scripts

The ETL scripts are responsible for extracting and transforming data. They are configured to run periodically via cron tasks.

* **Data Deduplication**: Duplicates are detected using a unique ID. If a conflict occurs, the row with the duplicate post ID will not be affected (i.e., no update will be made).

### Cron Jobs

We use Linux's default cron tasks to handle the scheduling. This choice was made for simplicity, as using Airflow would be overkill for this system.

## Configuration

* **DB Connection Credentials**: These can be updated in the `.env` configuration file.
* **Cron Schedule**: Modify the cron configuration as needed to adjust the schedule for running the ETL scripts.

