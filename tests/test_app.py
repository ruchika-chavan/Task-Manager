import pytest
from app import app, db  # Import Flask app and database

@pytest.fixture
def client():
    """Set up the test client and database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create test database
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after test

def test_home_page(client):
    """Test if the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200  # Ensure successful response
    assert b"Task Manager" in response.data  # Check if expected text is in response

def test_add_task(client):
    """Test adding a new task."""
    response = client.post('/add', data={'task': 'Test Task'}, follow_redirects=True)
    assert response.status_code == 200  # Ensure success
    assert b"Test Task" in response.data  # Check if the task appears on the page
