import json
from flask_login import UserMixin
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import mapped_column, relationship
from db import db


class User(UserMixin, db.Model):
    id = mapped_column(Integer, primary_key=True)
    role = mapped_column(String(20), nullable=False, default="user")
    email = mapped_column(String(50), nullable=False, unique=True)
    username = mapped_column(String(50), nullable=False, unique=True)
    password = mapped_column(String(50), nullable=False)
    game = relationship("Game", uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "email": self.email,
            "username": self.username,
            "password": self.password,
        }


class Game(db.Model):
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(User.id), nullable=False, unique=True)
    user = relationship("User", back_populates="game")
    questions = relationship("GameQuestion", cascade="all, delete-orphan")


class Question(db.Model):
    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String(50), nullable=False)
    difficulty = mapped_column(String(10), nullable=False)
    question = mapped_column(String(200), nullable=False)
    correct_answer = mapped_column(String(200), nullable=False)
    incorrect_answers_string = mapped_column(String(600), nullable=False)
    games = relationship("GameQuestion", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "difficulty": self.difficulty,
            "question": self.question,
            "correct_answer": self.correct_answer,
            "incorrect_answers": json.loads(self.incorrect_answers_string),
        }


class GameQuestion(db.Model):
    id = mapped_column(Integer, primary_key=True)
    game_id = mapped_column(Integer, ForeignKey(Game.id), nullable=False)
    question_id = mapped_column(Integer, ForeignKey(Question.id), nullable=False)
    answered = mapped_column(db.Boolean, default=False)
    game = relationship("Game", back_populates="questions")
    question = relationship("Question", back_populates="games")
