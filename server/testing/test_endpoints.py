
from server.app import app
from server.models import *
import pytest


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def app_with_db():
    """Create a Flask app with a test database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_workout_endpoints(client):

    response = client.get('/workouts')
    assert response.status_code == 200
    data = response.get_json()
    assert 'workouts' in data

    # Test creating a workout
    response = client.post('/workouts', json={
        'date': '2024-07-01',
        'duration_minutes': 60,
        'notes': 'Morning workout'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['date'] == '2024-07-01'
    assert data['duration_minutes'] == 60
    assert data['notes'] == 'Morning workout'

    workout_id = data['id']

    # Test retrieving the created workout
    response = client.get(f'/workouts/{workout_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == workout_id

    # Test deleting the workout
    response = client.delete(f'/workouts/{workout_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Workout deleted'

    # Verify the workout is deleted
    response = client.get(f'/workouts/{workout_id}')
    assert response.status_code == 404

def test_exercise_endpoints(client):

    response = client.get('/exercises')
    assert response.status_code == 200
    data = response.get_json()
    assert 'exercises' in data

    # Test creating an exercise
    response = client.post('/exercises', json={
        'name': 'Push-ups',
        'category': 'Strength',
        'equipment_needed': False
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Push-ups'
    assert data['category'] == 'Strength'
    assert data['equipment_needed'] is False

    exercise_id = data['id']

    # Test retrieving the created exercise
    response = client.get(f'/exercises/{exercise_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == exercise_id

    # Test deleting the exercise
    response = client.delete(f'/exercises/{exercise_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Exercise deleted'    