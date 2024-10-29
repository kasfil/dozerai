import sqlite3
from datetime import datetime

from flask import Blueprint, jsonify, request, url_for

from config import DB_PATH
from webapp.helper.auth import validate_token

bp = Blueprint("images", __name__, url_prefix="/api/images")


@bp.route("/", methods=("GET",))
def index():
    # Check request header auth
    auth_token = request.headers.get("Authorization", "")
    is_valid, user = validate_token(auth_token)
    if not is_valid or not user:
        return jsonify({"error": "Invalid authentication token"}), 401

    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 5, type=int)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, photo_path, caption, rating, comments, created_at
        FROM user_photos WHERE user_id = ? ORDER BY id DESC LIMIT ? OFFSET ?""",
        (user.id, limit, (page - 1) * limit),
    )
    rows = cursor.fetchall()
    imgs = [
        {
            "id": row[0],
            "path": url_for("static", filename=row[1]),
            "caption": row[2],
            "rating": row[3],
            "comments": row[4],
            "created_at": datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S"),
        }
        for row in rows
    ]

    cursor.execute("SELECT COUNT(id) FROM user_photos WHERE user_id = ?", (user.id,))
    total_imgs = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    response = {
        "page": page,
        "total_img": total_imgs,
        "next_page": page + 1 if page * limit < total_imgs else None,
        "prev_page": page - 1 if page > 1 else None,
        "imgs": imgs,
    }

    return jsonify(response)


@bp.route("/<int:image_id>", methods=("GET", "DELETE"))
def image_detail_ops(image_id):
    # Check request header auth
    auth_token = request.headers.get("Authorization", "")
    is_valid, user = validate_token(auth_token)
    if not is_valid or not user:
        return jsonify({"error": "Invalid authentication token"}), 401

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute(
            """SELECT id, photo_path, caption, rating, comments, created_at
            FROM user_photos WHERE user_id = ? AND id = ?""",
            (user.id, image_id),
        )
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Image not found"}), 404

        img = {
            "id": row[0],
            "path": url_for("static", filename=row[1]),
            "caption": row[2],
            "rating": row[3],
            "comments": row[4],
            "created_at": datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S"),
        }

        cursor.close()
        conn.close()

        return jsonify(img)

    else:
        cursor.execute(
            """SELECT COUNT(*) FROM user_photos WHERE user_id = ? AND id = ?""",
            (user.id, image_id),
        )
        if cursor.fetchone() is None:
            return jsonify({"error": "Image not found"}), 404

        cursor.execute(
            """DELETE FROM user_photos WHERE user_id = ? AND id = ?""",
            (user.id, image_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

        return "", 204
