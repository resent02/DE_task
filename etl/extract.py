import logging
import os
import sys

import requests
from dotenv import load_dotenv
from psycopg2 import connect

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


log = logging.getLogger("Extract")
API_URL = "https://jsonplaceholder.typicode.com/posts"


def DB_URL() -> str:
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_NAME", "vk_db")
    user = os.getenv("DB_USER", "vk_user")
    password = os.getenv("DB_PASSWORD", "vk_password")

    URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return URL


class Post:
    def __init__(self, userId, id, title, body):
        self.userId = userId
        self.id = id
        self.title = title
        self.body = body


def get_posts() -> list[Post] | None:
    try:
        req = requests.get(API_URL, timeout=20)
        if req.status_code != 200:
            raise Exception()

        data = [Post(**item) for item in req.json()]
        log.info("Posts fetched successfully.")
        return data

    except Exception as e:
        log.error(f"Error fetching posts: {e}")
        return None


def import_to_db(data: list[Post]):
    connection = connect(DB_URL())
    cursor = connection.cursor()
    try:
        for post in data:
            cursor.execute(
                """
                INSERT INTO raw_users_by_posts (post_id, user_id, title, body)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (post_id) DO NOTHING;
                """,
                (post.id, post.userId, post.title, post.body),
            )
        connection.commit()
        log.info("Posts inserted successfully.")
    except Exception as e:
        log.error(f"Error inserting posts into DB: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


def init_db():
    connection = connect(DB_URL())
    cursor = connection.cursor()
    try:
        with open("init.sql", "r") as f:
            cursor.execute(f.read())
        connection.commit()
    except Exception as e:
        log.error(f"Error initializing DB: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    init_db()
    posts = get_posts()
    if posts:
        import_to_db(posts)
