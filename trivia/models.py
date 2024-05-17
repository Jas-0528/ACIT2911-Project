import json
import random
from flask_login import UserMixin
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import mapped_column, relationship
from werkzeug.security import generate_password_hash
from trivia.db import db


class User(UserMixin, db.Model):
    id = mapped_column(Integer, primary_key=True)
    role = mapped_column(String(20), nullable=False, default="user")
    email = mapped_column(String(50), nullable=False, unique=True)
    username = mapped_column(String(50), nullable=False, unique=True)
    password_hashed = mapped_column(String(50), nullable=False)
    quiz = relationship("Quiz", uselist=False, cascade="all, delete-orphan")

    def __init__(self, email, username, password, role="user"):
        self.role = role
        self.email = email
        self.username = username
        self.password_hashed = generate_password_hash(password, method="pbkdf2:sha256")


class Quiz(db.Model):
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    user = relationship("User", back_populates="quiz")
    questions = relationship("QuizQuestion", cascade="all, delete-orphan")


class Question(db.Model):
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String(50), nullable=False)
    difficulty = mapped_column(String(10), nullable=False)
    question = mapped_column(String(200), nullable=False)
    correct_answer = mapped_column(String(200), nullable=False)
    incorrect_answers_string = mapped_column(String(600), nullable=False)
    quizzes = relationship("QuizQuestion", cascade="all, delete-orphan")

    def to_api_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "difficulty": self.difficulty,
            "question": self.question,
            "correct_answer": self.correct_answer,
            "incorrect_answers": json.loads(self.incorrect_answers_string),
        }

    def to_play_dict(self):
        answers = json.loads(self.incorrect_answers_string) + [self.correct_answer]
        random.shuffle(answers)
        return {
            "id": self.id,
            "category": self.category,
            "difficulty": self.difficulty,
            "question": self.question,
            "correct_answer": self.correct_answer,
            "answers": answers,
        }


class QuizQuestion(db.Model):
    id = mapped_column(Integer, primary_key=True)
    quiz_id = mapped_column(Integer, ForeignKey(Quiz.id), nullable=False)
    question_id = mapped_column(Integer, ForeignKey(Question.id), nullable=False)
    answered = mapped_column(db.Boolean, default=False)
    quiz = relationship("Quiz", back_populates="questions")
    question = relationship("Question", back_populates="quizzes")
