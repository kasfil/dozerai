from pathlib import Path

import aiosqlite

from config import BASE_PATH


class DB:
    def __init__(self, db_path: Path) -> None:
        self.db_uri = db_path

    async def save_rating(
        self,
        user_id: int,
        photo_path: Path,
        caption: str | None,
        rating: float,
        comments: str | None,
    ) -> int:
        async with aiosqlite.connect(self.db_uri) as con:
            # cut out path from photo_path so it start from BASE_DIR
            photo_path = photo_path.relative_to(Path.joinpath(BASE_PATH, "static"))

            res = await con.execute(
                """INSERT INTO user_photos (user_id, photo_path, caption, rating, comments)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT (user_id, photo_path)
                DO UPDATE SET caption = excluded.caption, rating = excluded.rating,
                comments = excluded.comments;""",
                (user_id, str(photo_path), caption, rating, comments),
            )
            await con.commit()
            return res.lastrowid or 0

    async def add_user_token(self, user_id: int, token: int) -> None:
        async with aiosqlite.connect(self.db_uri) as con:
            await con.execute(
                """INSERT INTO user_tokens (user_id, token)
                VALUES (?, ?)
                ON CONFLICT (user_id)
                DO UPDATE SET token = token + excluded.token;""",
                (user_id, token),
            )
            await con.commit()

    async def get_user_profile(self, user_id: int) -> tuple[int, float]:
        """Get total photos and average rating for given user_id."""

        async with aiosqlite.connect(self.db_uri) as con:
            res = await con.execute(
                """SELECT COUNT(id) as total_photos, COALESCE(AVG(rating), 0) as avg_rating
                FROM user_photos
                WHERE user_id = ?""",
                (user_id,),
            )
            res = await res.fetchone()

            total_photos = res[0] if res else 0
            avg_rating = res[1] if res else 0.0

            return total_photos, avg_rating

    async def get_user_token(self, user_id: int) -> int:
        async with aiosqlite.connect(self.db_uri) as con:
            res = await con.execute(
                """SELECT token
                FROM user_tokens
                WHERE user_id = ?""",
                (user_id,),
            )
            res = await res.fetchone()

            return res[0] if res else 0

    async def get_image_path(self, image_id: int) -> Path | None:
        async with aiosqlite.connect(self.db_uri) as con:
            res = await con.execute(
                """SELECT photo_path
                FROM user_photos
                WHERE id = ?""",
                (image_id,),
            )
            res = await res.fetchone()

            return Path.joinpath(BASE_PATH, "static", res[0]) if res else None
