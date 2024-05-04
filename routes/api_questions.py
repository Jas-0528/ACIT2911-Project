from flask import Blueprint
from db import db
from models import Question

api_questions_bp = Blueprint("api_questions", __name__)


# Return list of question jsons
@api_questions_bp.route("/", methods=["GET"])
def api_question_list():
    pass
