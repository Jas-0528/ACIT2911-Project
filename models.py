from sqlalchemy.sql import functions as func
from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import mapped_column
from db import db


class Question(db.Model):
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String(50), nullable=False)
    difficulty = mapped_column(String(10), nullable=False)
    question = mapped_column(String(200), nullable=False)
    correct_answer = mapped_column(String(200), nullable=False)
    incorrect_answer_1 = mapped_column(String(200), nullable=False)
    incorrect_answer_2 = mapped_column(String(200), nullable=False)
    incorrect_answer_3 = mapped_column(String(200), nullable=False)

    def to_dict(self):
        pass
