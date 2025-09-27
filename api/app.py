from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os
from typing import List
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def DB_URL() -> str:
    host = "localhost"
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_NAME", "vk_db")
    user = os.getenv("DB_USER", "vk_user")
    password = os.getenv("DB_PASSWORD", "vk_password")

    URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return URL

app = FastAPI()

class UserPostStats(BaseModel):
    user_id: int
    posts_cnt: int
    calculated_at: str

def get_db_connection():
    conn = psycopg2.connect(DB_URL())
    return conn

@app.get("/top_users_by_posts", response_model=List[UserPostStats])
def get_top_users():
    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT user_id, posts_cnt, calculated_at FROM top_users_by_posts ORDER BY posts_cnt DESC"
    cur.execute(query)
    
    rows = cur.fetchall()
    
    
    cur.close()
    conn.close()
    
    
    result = [
        UserPostStats(
            user_id=row[0],
            posts_cnt=row[1],
            calculated_at=row[2].strftime("%Y-%m-%d %H:%M:%S")
        ) 
        for row in rows
    ]
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
