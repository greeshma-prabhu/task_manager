import json
import pytest
from app import app, db
from models import Task

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables before each test
        yield client
        with app.app_context():
            db.drop_all()  # Drop tables after each test

# Test creating a task
def test_create_task(client):
    response = client.post('/api/tasks/', json={
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": "2025-05-14",
        "priority": "High"
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == "Task created successfully"

# Test getting a task by ID
def test_get_task(client):
    # First, create a task
    task = Task(title="Get Task", description="Fetch this task", due_date="2025-05-14", priority="Low")
    db.session.add(task)
    db.session.commit()

    # Fetch the task by ID
    response = client.get(f'/api/tasks/{task.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == "Get Task"

# Test listing tasks with pagination
def test_list_tasks(client):
    # Create a task
    task1 = Task(title="Task 1", description="First task", due_date="2025-05-14", priority="Medium")
    task2 = Task(title="Task 2", description="Second task", due_date="2025-05-15", priority="Low")
    db.session.add(task1)
    db.session.add(task2)
    db.session.commit()

    # List tasks with pagination
    response = client.get('/api/tasks/?page=1&per_page=2')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['tasks']) == 2  # Should return 2 tasks
