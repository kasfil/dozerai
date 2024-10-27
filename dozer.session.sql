DROP TABLE IF EXISTS user_photos;
CREATE TABLE IF NOT EXISTS user_photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    photo_path TEXT NOT NULL,
    caption TEXT,
    rating REAL NOT NULL CHECK(rating >= 0 AND rating <= 10),
    comments TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, photo_path)
);

CREATE TABLE IF NOT EXISTS user_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    token INTEGER NOT NULL CHECK(token >= 0)
)