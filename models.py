import random
from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import JSON
from db import db


class Question(db.Model):
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String(50), nullable=False)
    difficulty = mapped_column(String(10), nullable=False)
    question = mapped_column(String(200), nullable=False)
    correct_answer = mapped_column(String(200), nullable=False)
    incorrect_answers = mapped_column(JSON, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "difficulty": self.difficulty,
            "question": self.question,
            "correct_answer": self.correct_answer,
            "incorrect_answers": self.incorrect_answers,
        }
