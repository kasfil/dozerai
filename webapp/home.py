from flask import Blueprint, render_template

from config import DEBUG

bp = Blueprint("home", __name__, url_prefix="")


@bp.route("/", methods=("GET",))
def index():
    return render_template("dashboard.html.jinja", DEBUG_MODE=DEBUG)


@bp.route("/image/<image_id>", methods=("GET",))
def image(image_id):
    return render_template("image-detail.html.jinja", image_id=image_id)
