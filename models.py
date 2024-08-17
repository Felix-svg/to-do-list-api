from config import db
from sqlalchemy_serializer import SerializerMixin


class Todo(db.Model, SerializerMixin):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __str__(self) -> str:
        return f"<Todo {self.id}: {self.task} - Completed: {self.completed}>"

