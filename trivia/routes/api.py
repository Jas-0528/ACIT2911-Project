from flask import Blueprint, jsonify
from trivia.db import db
from trivia.models import Question

api_bp = Blueprint("api", __name__)


# Return list of question jsons
@api_bp.route("/", methods=["GET"])
def question_list():
    stmt = db.select(Question).order_by(Question.id)
    questions = db.session.execute(stmt).scalars()
    api_dict_list = []

    for question in questions:
        api_dict_list.append(question.to_api_dict())

    return jsonify(api_dict_list)
