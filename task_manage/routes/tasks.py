from flask import Blueprint, request, jsonify
from models import Task
from database import db

# Create a Blueprint for task-related routes
tasks_bp = Blueprint('tasks', __name__)

# Route to create a task
@tasks_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()

    if not data.get('title') or not data.get('description') or not data.get('due_date'):
        return jsonify({"error": "Missing required fields"}), 400

    task = Task(
        title=data['title'],
        description=data['description'],
        due_date=data['due_date'],
        priority=data['priority']
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task created successfully", "task": task.to_dict()}), 201

# Route to get task by ID
@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task.to_dict())

# Route to list tasks with pagination
@tasks_bp.route('/', methods=['GET'])
def list_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    tasks = Task.query.paginate(page, per_page, False)
    tasks_list = [task.to_dict() for task in tasks.items]

    return jsonify({"tasks": tasks_list, "total": tasks.total, "page": page, "per_page": per_page})
