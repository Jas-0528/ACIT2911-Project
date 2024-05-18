import pytest
from unittest.mock import MagicMock, patch
from trivia.db import db
from trivia.models import Question
from trivia.routes.html import (
    get_user,
    get_question,
    get_categories
)

class MockDB:
    def get_or_404(self, model, id, description):
        pass

@pytest.fixture
def mock_db(monkeypatch):
    mock_db_instance = MagicMock()
    monkeypatch.setattr('trivia.db', mock_db_instance)
    return mock_db_instance

db = MockDB()

def test_retrieval_functions():
    with pytest.raises(Exception):  
        get_user(123)  
    with pytest.raises(Exception):  
        
        get_question(456) 

@pytest.fixture
def test_get_categories(mock_db):
    expected_categories = ['category1', 'category2']
    mock_db.select.return_value = MagicMock(
        execute = MagicMock(return_value=MagicMock(
            scalars = MagicMock(return_value=expected_categories)
        ))
    )
    assert get_categories() == expected_categories
    mock_db.select.assert_called_once()
    mock_db.select().distinct.assert_called_once_with(Question.category)



