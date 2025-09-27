CREATE TABLE IF NOT EXISTS raw_users_by_posts (
    post_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    ingested_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS top_users_by_posts (
    user_id INT PRIMARY KEY,
    posts_cnt INT NOT NULL,
    calculated_at TIMESTAMP NOT NULL DEFAULT now()
);