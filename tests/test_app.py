import pytest
from app import app, db  # Import Flask app and database
from flask import url_for

@pytest.fixture
def client():
    """Set up test client and database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables
        yield client  # Provide client for tests
        with app.app_context():
            db.drop_all()  # Clean up after tests

def test_homepage(client):
    """Check if homepage loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Task Manager" in response.data  # Check if title appears

def test_add_task(client):
    """Ensure a new task can be added successfully."""
    response = client.post('/add', data={'task': 'Test Task'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Task" in response.data  # Check if task appears on the page
