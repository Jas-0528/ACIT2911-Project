import pytest
from app import app


@pytest.fixture(autouse=True)
def enable_testing_mode():
    app.config["TESTING"] = True
