import logging
import os
import sys

from dotenv import load_dotenv
from psycopg2 import connect

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

log = logging.getLogger("transform")
API_URL = "https://jsonplaceholder.typicode.com/posts"


def DB_URL() -> str:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_NAME", "vk_db")
    user = os.getenv("DB_USER", "vk_user")
    password = os.getenv("DB_PASSWORD", "vk_password")

    URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return URL


def init_db():
    connection = connect(DB_URL())
    cursor = connection.cursor()
    try:
        with open("init.sql", "r") as f:
            cursor.execute(f.read())
        connection.commit()
        log.info("Database initialized successfully.")
    except Exception as e:
        log.error(f"Error initializing DB: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


def transform_data():
    connection = connect(DB_URL())
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO top_users_by_posts (user_id, posts_cnt, calculated_at)
            SELECT user_id, COUNT(*) AS posts_cnt, now() AS calculated_at
            FROM raw_users_by_posts
            GROUP BY user_id
            ORDER BY posts_cnt DESC
            ON CONFLICT (user_id) DO UPDATE
            SET posts_cnt = EXCLUDED.posts_cnt,
                calculated_at = EXCLUDED.calculated_at;
            """
        )
        connection.commit()
        log.info("Data transformation completed successfully.")
    except Exception as e:
        log.error(f"Error during data transformation: {e}")
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    init_db()
    transform_data()
