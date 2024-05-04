from flask import Blueprint, render_template

html_bp = Blueprint("html", __name__)


# Home page
@html_bp.route("/", methods=["GET"])
def home():
    return render_template("home.html")
