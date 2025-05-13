from database import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    due_date = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.String(10), default='Medium')
    status = db.Column(db.String(20), default='Pending')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }
