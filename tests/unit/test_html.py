import pytest
from unittest.mock import patch, MagicMock
from flask import session
from trivia.routes import html
from trivia import app
from sqlalchemy.sql.elements import UnaryExpression
from trivia.models import User, Question, Quiz, QuizQuestion
from trivia.db import db    
    
#test get_categories 
def test_get_categories():
     with app.app_context():
        categories = html.get_categories()
        assert categories[0] == "Animals"
        
#test fetch_questions, based on category, difficulty and length
def test_fetch_questions_category():
    with app.app_context():
        questions = html.fetch_questions(category="Animals", difficulty="all", length=5)
        for question in questions:
            assert question.category == "Animals"
        
def test_fetch_questions_difficulty():
    with app.app_context():
        questions = html.fetch_questions(category="all", difficulty="easy", length=5)
        for question in questions:
            assert question.difficulty == "easy"
            
def test_fetch_questions_length():
    with app.app_context():
        questions = html.fetch_questions(category="all", difficulty="all", length=5)
        assert len(questions) == 5
        
def test_fetch_questions_random():
    with app.app_context():
        questions = html.fetch_questions(category="all", difficulty="all", length=5)
        #make sure the questions are random
        compare = questions[0]
        for question in range(1, len(questions)):
            assert compare != questions[question]
            compare = questions[question]

def test_create_quiz_new():
    with app.app_context():
        user = User(username='test12334', email="somethin@gmail.com", password="password")
        db.session.add(user)
        db.session.commit()

        result = html.create_quiz(user, 'Animals', 'easy', 5)
        assert isinstance(result, Quiz)
        assert result.user == user

        # Cleanup
        for question in result.questions:
            db.session.delete(question)
        db.session.delete(result)
        db.session.delete(user)
        db.session.commit()
        
def test_create_quiz_existing():
    with app.app_context():
        # Create a User and Quiz object
        user = User(username='test134', email="something@gmail.com", password="password")
        existing_quiz = Quiz(user=user)
        db.session.add(user)
        db.session.add(existing_quiz)
        db.session.commit()

        result = html.create_quiz(user, 'Animals', 'easy', 5)
        assert result == existing_quiz
        
        db.session.delete(existing_quiz)
        db.session.delete(user)
        db.session.commit()

        