from flask import Flask
from routes.tasks import tasks_bp
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

# Register Blueprint
app.register_blueprint(tasks_bp, url_prefix="/api/tasks")

@app.route('/')
def home():
    return {"message": "Task Manager API is running 🚀"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
