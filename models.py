from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from flask_jwt_extended import create_access_token


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # relationship to related todo
    todos = db.relationship("Todo", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def get_token(self, expires_in=3600):
        return create_access_token(identity=self.id, expires_delta=expires_in)

    def __str__(self) -> str:
        return f"<{self.name} - {self.email}>"


class Todo(db.Model, SerializerMixin):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # relationship to related users
    user = db.relationship("User", back_populates="todos")

    def __str__(self) -> str:
        return f"<Todo {self.id}: {self.task} - Completed: {self.completed}>"


class Tokenblocklist(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
