from flask import Blueprint, jsonify
from db import db
from models import Question

api_questions_bp = Blueprint("api_questions", __name__)


# Return list of question jsons
@api_questions_bp.route("/", methods=["GET"])
def api_question_list():
    question_stmt = db.select(Question).order_by(Question.id)
    question_objs = db.session.execute(question_stmt).scalars()
    questions = []

    for question_obj in question_objs:
        questions.append(question_obj.to_dict())

    return jsonify(questions)
