import json
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import mapped_column, relationship
from db import db


class Question(db.Model):
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String(50), nullable=False)
    difficulty = mapped_column(String(10), nullable=False)
    question = mapped_column(String(200), nullable=False)
    correct_answer = mapped_column(String(200), nullable=False)
    incorrect_answers_string = mapped_column(String(600), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "difficulty": self.difficulty,
            "question": self.question,
            "correct_answer": self.correct_answer,
            "incorrect_answers": json.loads(self.incorrect_answers_string),
        }

#user class
class User(db.Model):
    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(50), nullable=False, unique=True)
    username = mapped_column(String(50), nullable=False, unique=True)
    password = mapped_column(String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "password": self.password
        }